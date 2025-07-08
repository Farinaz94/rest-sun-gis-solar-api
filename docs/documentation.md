### Enable Solar Radiation Module in Actinia
### Goal
Install the GRASS GIS extension r.sun.hourly inside the Actinia container to enable hourly solar radiation analysis.
### Implementation
The Actinia Dockerfile was modified to include installation commands for the r.sun.hourly module. This is done using g.extension with a temporary GRASS location (EPSG:4326). After modifying the Dockerfile, the image was rebuilt to apply the changes.
### Dockerfile Modification
At approximately line 24 in ./docker/actinia-core-alpine/Dockerfile, the following lines were added:
```
RUN grass --tmp-location EPSG:4326 --exec g.extension -s extension=r.sun.hourly
RUN grass --tmp-location EPSG:4326 --exec g.extension extension=r.sun.hourly
```
These commands download and compile the solar module during the build process.

Building the Image
From the root directory of the project, run:
```
docker build -f ./docker/actinia-core-alpine/Dockerfile --tag actinia:local .
```
This command creates a new Docker image tagged actinia:local, which includes the installed solar extension.

### Docker-Based Service Configuration for Actinia
### Goal
Set up a fully containerized environment to run Actinia, PostgreSQL (with PostGIS), and Valkey using Docker Compose. This setup allows for scalable, isolated, and reproducible service orchestration during development and testing.
### Implementation
The services were defined in a docker-compose.yml file and configured via a local .env file. These two files together control the execution of all backend components (Actinia, Valkey, Postgres) required by the system.
### Docker Compose File
A new file named docker-compose.yml was created in the project root with the following contents:
```
services:
  actinia:
    image: actinia:local
    ports:
      - "8088:8088"
    environment:
      - ACTINIA_CUSTOM_TEST_SERVER=true
      - ACTINIA_API_LOG_LEVEL=debug       
    volumes:
      - ./data/actinia-data/grassdb:/actinia_core/grassdb
      - ./data/actinia-data/resources:/actinia_core/resources
      - ./data/actinia-data/userdata:/actinia_core/userdata
      - ./data/actinia-data/workspace/temp_db:/actinia_core/workspace/temp_db
      - ./data/actinia-data/workspace/tmp:/actinia_core/workspace/tmp
    restart: unless-stopped
    depends_on:
      valkey:
        condition: service_started
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8088/api/v3/version"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s

  valkey: 
    image: valkey/valkey:8.1-alpine
    volumes:
      - ./data/valkey_data:/data
    environment:
      - VALKEY_PASS_FILE=/data/config/.valkey
    command: [
      "sh", "-c",
      "docker-entrypoint.sh /data/config/valkey.conf --requirepass \"$$(cat $$VALKEY_PASS_FILE)\""
    ]
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "valkey-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  postgres:
    image: postgis/postgis:14-3.2
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=actinia
      - POSTGRES_PASSWORD=actinia
      - POSTGRES_DB=actinia
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U actinia"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```
This configuration defines all containers and volumes required to run Actinia in a local, reproducible development environment.
### Environment Configuration
A .env file was also created in the project root to store configuration variables used across services and backend code:
```
# Actinia Configuration
ACTINIA_URL=http://localhost:8088
ACTINIA_USER=actinia-gdi
ACTINIA_PASSWORD=actinia-gdi

# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=actinia
POSTGRES_PASSWORD=actinia
POSTGRES_DB=actinia
DATABASE_URL=postgresql://actinia:actinia@localhost:5432/actinia

# Valkey Configuration
VALKEY_HOST=localhost
VALKEY_PORT=6379
VALKEY_PASSWORD=your_secure_valkey_password_here

# Development Settings
DEBUG=true
LOG_LEVEL=INFO
```

## Valkey Configuration Setup
### Goal  
Prepare and configure Valkey for use in the local Actinia environment by copying the required configuration files and correcting the password file to avoid authentication errors.
### Implementation  
The `valkey_data` directory was copied from the Actinia source repository into the project's `data/` directory. After copying, the `.valkey` password file was manually cleaned to ensure it contained only the raw password value.
### Copying Configuration Files
```
# Copy the entire valkey_data folder from actinia repository
Copy-Item -Path .\actinia-core\docker\valkey_data -Destination .\data\ -Recurse
```
This ensures that the required Valkey configuration files are placed in the correct location expected by the Docker container.
### Fixing the Password File
```
# The copied password file may contain extra lines that cause authentication errors
# Edit the .valkey file to contain only the password
notepad .\data\valkey_data\config\.valkey

# Ensure the file contains ONLY the password, no extra lines or characters
# Save and close the file
```
The `.valkey` file must contain **only** the password with no trailing spaces, newlines, or hidden characters. Incorrect formatting will result in Valkey authentication failure at container startup.

## Creating and Verifying Initial Actinia Users
### Goal  
Set up initial user accounts in Actinia to enable authenticated API access and role-based control for development, admin, and testing purposes.
### Implementation  
Users were created using the built-in `actinia-user` CLI tool via Docker. Each user was assigned specific roles, groups, and process limits according to their intended usage. 
### User Creation Commands
```
# Create admin user
docker-compose exec actinia actinia-user create -u admin -w admin123 -r admin -g admin -c 1000000000 -n 10000 -t 60000
# Create development user
docker-compose exec actinia actinia-user create -u dev_user -w dev123 -r user -g solar_team -c 100000000 -n 1000 -t 6000
# Create test user for API testing
docker-compose exec actinia actinia-user create -u test_user -w test123 -r user -g solar_team -c 100000000 -n 1000 -t 6000
```
## Installing Development Dependencies
### Goal  
Install all required Python packages for backend development, including FastAPI, database integration, authentication, and testing tools.
### Implementation  
A `requirements.txt` file was created in the root of the `backend/` directory. This file lists all development dependencies needed to run and test the FastAPI application.
### requirements.txt Content
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
alembic==1.13.0
psycopg2-binary==2.9.9
httpx==0.25.2
python-dotenv==1.0.0
pytest==7.4.3
pytest-asyncio==0.21.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```
This file allows for consistent dependency installation using:
```bash
pip install -r requirements.txt
```

## Actinia Validation Service
### Goal  
Enable the backend to verify user credentials against the Actinia API. This service ensures only valid users can authenticate and interact with Actinia-based operations.
### Implementation  
A service function named `validate_actinia_user()` was created inside the `backend/app/services/actinia/validation.py` module. This function uses HTTP Basic Authentication to send a GET request to the Actinia `/api/v3/locations` endpoint.
It handles:
- Successful authentication (status code `200`)
- Invalid credentials (`401`)
- Connection issues or timeouts
- Logging for both success and failure events
### Behavior Summary
- Successful Auth → returns `True`
- Invalid credentials (401) → logs warning and returns `False`
- Other errors → returns `False` and logs message
### Logging  
The function uses Python’s `logging` module to track request outcomes using `info`, `debug`, `warning`, and `error` levels. This improves visibility for debugging and monitoring. This function is used within the authentication flow, specifically during the `/login` route execution.

## JWT Token Service and Authentication Routes
### Goal  
Develop secure and configurable JWT-based authentication, including token generation, validation, refresh, and logout. The system must be compatible with Actinia credentials and include user session tracking.
### Implementation  
Two core components were developed:
- A **JWT service module** (`app/services/auth/jwt.py`)
- An **authentication route module** (`app/api/auth/routes.py`)
These modules integrate Actinia validation with FastAPI security mechanisms to provide stateless authentication and session persistence via a database-backed token system.
### JWT Token Service (`jwt.py`)
The `jwt.py` service handles:
- `create_access_token()`: Generates JWT tokens with user metadata and timezone-aware expiration.
- `verify_token()`: Decodes and validates JWTs, ensuring they are not expired or malformed.
- `get_current_user()`: Extracts the user from a token and confirms that the corresponding session is active in the database.
- `refresh_token()`: Verifies a token and issues a new one with refreshed expiration.
The token includes custom claims:
- `user_id`, `username`, `role`, `groups`
- `iat` (issued at) and `exp` (expiration time)
- Timezone-aware expiration using Python's `zoneinfo`
Session tokens are stored in the database and validated on every request.
### Authentication Routes (`routes.py`)
The `/login` route performs:
- Validation against the Actinia server via `validate_actinia_user()`
- Database check for the user
- Timezone extraction from the client IP
- Token generation via `create_access_token()`
- Session creation and database storage
The `/refresh` route:
- Accepts an existing token
- Validates and refreshes it via `refresh_token()`
- Returns a new token with updated expiration
The `/logout` route:
- Locates the session by token
- Marks it as inactive
- Logs the logout event with timestamp
The `/me` route:
- Validates the JWT and retrieves user info
- Queries the database for the user's profile
- Returns the user's username, role, and groups
All routes are secured using `HTTPBearer` and FastAPI’s `Depends()` mechanism.
### Logging  
Logging is included at all critical points, including:
- Token creation, refresh, and expiration
- Login success or failure
- Logout and session invalidation
This ensures observability and ease of debugging throughout the authentication flow.
### Notes  
- The JWT secret key and algorithm are configured via the `settings` module.
- Session control enables revoking tokens without needing token blacklisting.
- This authentication layer serves as the foundation for securing all API routes.

## Timezone Detection Utility
### Goal  
Automatically detect and apply the user’s local timezone based on their IP address to improve logging clarity and user experience.
### Implementation  
A utility module was created at `app/utils/timezone.py`. It includes two functions:
- `get_timezone_from_ip(ip: str)`:  
  Sends a request to the public API [`https://ipwho.is/{ip}`](https://ipwho.is) to determine the user's timezone based on their IP address. If the request fails or no timezone is returned, it falls back to `'UTC'`.
- `convert_to_user_time(utc_dt: datetime, timezone_id: str)`:  
  Converts a UTC datetime to a localized time using the standard `zoneinfo` library.
### Use Cases  
- During login, the user's IP is extracted and used to detect their timezone.
- Token expiration timestamps are converted and shown in the user's local time.
- Log entries reflect the actual time from the user's perspective, not just the server time.
### Fallback Strategy  
If:
- The IP is `127.0.0.1` (local)
- The API is unreachable
- No timezone is returned
Then the system defaults to `'UTC'` to ensure consistent behavior without errors.
### Example Behavior  
```python
# Get timezone from IP
tz = get_timezone_from_ip("2.42.12.123")  # → "Europe/Rome"
# Convert UTC datetime to user time
localized = convert_to_user_time(datetime.utcnow(), tz)
```
### Notes  
- This logic is currently used in the `/login` route to localize the `expires_at` field.

## User and Resource Management Models
### Goal  
Define SQL-based models for managing users, sessions, uploaded files, jobs, and results. These models enable secure, per-user data storage and relationships required for personalized processing and access control.
### Implementation  
All models are implemented using `SQLModel` and stored in `app/models/`. They include proper foreign key relationships and indexing for performance and consistency. Models are registered in `app/models/__init__.py` to support centralized imports.
### `User`  
The `User` model stores Actinia-linked profile data and preferences:
- `username`: unique Actinia-linked ID  
- `role`: user or admin  or superadmin
- `preferences` and `groups`: stored as JSON using PostgreSQL  
### `Session`  
Tracks individual login sessions:
- `session_token`: JWT used in authentication  
- `login_time`, `logout_time`  
- `ip_address`, `user_agent`, `location`  
- Linked to `user_id`  
- Flags for `is_active` and `invalidated_by_admin`
### `File`  
Represents user-uploaded geospatial files:
- `file_name`, `file_type`, `format`, `epsg`  
- Validation status via `valid`  
- GRASS metadata: `location`, `mapset`  
- Linked to both `user_id` and `session_id`
### `Job`  
Stores user-triggered processing jobs:
- `job_name`, `status`  
- Linked to `user_id`  
### `Result`  
Captures the output of completed jobs:
- `file_name`, `created_at`  
- `sharing_permission`: `private` by default  
- Linked to both `user_id` and `job_id`
### Notes  
- All models use `SQLModel` with full SQLAlchemy compatibility  
- Foreign key constraints enforce secure user-data ownership  
- JSON fields provide flexibility in storing user-specific configurations  
- Consistent UTC timestamps ensure accurate time tracking across components






