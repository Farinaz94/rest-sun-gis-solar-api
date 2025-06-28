from fastapi import APIRouter  
from . import sync_test  # Import the sync_test module

router = APIRouter()
router.include_router(sync_test.router)
