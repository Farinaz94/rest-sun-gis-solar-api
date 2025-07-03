from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlmodel import Session
from app.models.session import Session as SessionModel
from sqlmodel import select
import shutil
import time
from pathlib import Path
import zipfile
from uuid import uuid4
from fastapi import Security


from app.services.auth.jwt import verify_token
from app.database import get_db
from app.models.file import File as FileModel

from app.utils.geospatial import get_epsg_from_raster, get_epsg_from_vector, create_location_and_mapset

router = APIRouter()

SUPPORTED_EXT = ["tif", "tiff", "asc", "geojson", "shp", "zip", "gpkg"]

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user: dict = Security(verify_token),
    db: Session = Depends(get_db)
):

    user_id = user.get("user_id")
    username = user.get("username")
    if not user_id or not username:
        raise HTTPException(status_code=400, detail="Missing user_id or username in token")


    # File validation
    filename = file.filename
    ext = filename.split(".")[-1].lower()
    if ext not in SUPPORTED_EXT:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: .{ext}")

    # Save temp file
    base_dir = Path(__file__).resolve().parents[3]
    temp_dir = base_dir / "data" / "actinia-data" / "userdata" / "tmp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / filename

    if temp_path.exists():
        raise HTTPException(status_code=400, detail="File already exists")

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    time.sleep(1)

    # Detect EPSG
    epsg = None
    vector_path = temp_path
    if ext == "zip":
        try:
            with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                for name in zip_ref.namelist():
                    if name.endswith(".shp"):
                        vector_path = temp_dir / name
                        break
                else:
                    raise HTTPException(status_code=400, detail="No .shp file found in ZIP archive")
        except zipfile.BadZipFile:
            raise HTTPException(status_code=400, detail="Uploaded ZIP is not a valid archive")

    try:
        if ext in ["tif", "tiff", "asc"]:
            epsg = get_epsg_from_raster(str(temp_path))
        elif ext in ["geojson", "gpkg", "shp", "zip"]:
            epsg = get_epsg_from_vector(str(vector_path))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"GDAL/OGR validation failed: {e}")

    # Create GRASS location/mapset
    location = f"location_epsg_{epsg}"
    timestamp = int(time.time())
    mapset = f"mapset_{username}_{timestamp}"
    try:
        if epsg:
            create_location_and_mapset(location, mapset, epsg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Actinia error: {str(e)}")

    # Final upload path includes username  no superadmin fallback)
    upload_dir = base_dir / "data" / "actinia-data" / "userdata" / username / location / mapset
    upload_dir.mkdir(parents=True, exist_ok=True)

    final_path = upload_dir / filename
    shutil.move(str(temp_path), final_path)

    # Session fetch
    latest_session = (
        db.query(SessionModel)
        .filter(SessionModel.user_id == user_id)
        .first()
    )

    # Save file metadata to DB
    file_type = "raster" if ext in ["tif", "tiff", "asc"] else "vector"
    file_record = FileModel(
        user_id=user_id,
        file_name=file.filename,
        file_type=file_type,
        format=ext,
        epsg=epsg,
        valid=True,
        location=location,
        mapset=mapset,
        session_id=latest_session.id if latest_session else None
    )
    db.add(file_record)
    db.commit()
    db.refresh(file_record)

    return {
        "message": "File uploaded and location/mapset created automatically",
        "file": file.filename,
        "location": location,
        "mapset": mapset,
        "epsg": epsg,
        "session_id": file_record.session_id
    }
