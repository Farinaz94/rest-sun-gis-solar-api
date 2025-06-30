Urban Solar GIS Backend with Actinia and FastAPI
---
A RESTful API system for solar energy scenario creation, developed as part of the thesis **“Design and Implementation of a Modular Backend for Urban Solar Co-Simulation”** at *Politecnico di Torino*. This backend enables seamless interaction with [Actinia](https://actinia.mundialis.de/) for geospatial processing and simulation-ready data preparation through a secure, modular architecture.

 Overview
---
The growing demand for sustainable energy systems in urban environments requires scalable and interoperable platforms for spatial analysis. This backend addresses key challenges in accessing, processing, and managing geospatial data, specifically for **rooftop photovoltaic (PV) simulation**. The system combines the power of **FastAPI**, **Actinia**, and a **JWT-based authentication layer** to support user management, secure sessions, and solar GIS services.

 Key Contributions
---
- **Hybrid Authentication**: Combines FastAPI’s JWT system with Actinia’s native user credentials for dual-layer verification.
- **Role-Based Access Control**: Differentiates users and admins, including integration of an Actinia-based superuser.
- **Session Logging**: Tracks user IP addresses, device information, and session metadata for auditability.
- **GIS Job Management**: Provides endpoints for managing solar analysis tasks (under development).
- **Actinia Integration**: Sends authenticated REST requests to Actinia for GIS operations, such as mapset creation and raster uploads.

System Architecture
---
The backend follows a clean modular architecture, allowing future expansion. Key components include:
- **User & Auth API** (`/auth`, `/profile/me`)
- **Session Tracker** (records login info)
- **Actinia Service Layer**: Handles communication with Actinia API
- **Job Management API** (coming soon): Will support job creation, monitoring, and result retrieval

Technology Stack
---
| Layer            | Tool / Technology        |
|------------------|--------------------------|
| Web Framework    | FastAPI                  |
| GIS Engine       | Actinia + GRASS GIS      |
| DBMS             | PostgreSQL + PostGIS     |
| Auth System      | JWT (JSON Web Token)     |
| Containerization | Docker / Docker Compose  |

Installation
---
1. Clone the repository:
git clone https://github.com/Farinaz94/rest-sun-gis-solar-api.git
cd rest-sun-gis-solar-api

2. Setup backend environment:
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

3. Configure environment variables:
Create a .env file and add:
env
ACTINIA_USER=actinia-gdi
ACTINIA_PASS=actinia-gdi
ACTINIA_URL=http://localhost:8088
SECRET_KEY=your_jwt_secret_key

Docker Setup (Optional)
---
Start Actinia and database with Docker:
docker compose up --build

API Usage
---
Access the API docs at: http://localhost:8000/docs

1. Auth & User
POST /auth/login → Login with Actinia credentials and receive JWT token
GET /auth/me → Get current authenticated user info
POST /users/sync-user/{username} → Sync Actinia user into system
PUT /profile/me/settings → Update user settings

2. Session Logs
Automatically logs each login with IP and timestamp in the database

Database Schema
---
The backend uses a PostgreSQL database to persist:
users → Basic info + roles
sessions → User login history (IP, timestamp)
(More models planned for solar jobs and results)

Admin & Role Design
---
A super admin account (actinia-gdi) is configured in .env
Other users are synced from Actinia or created via the API
Role-based permissions are enforced on protected endpoints

Contact
---
If you have questions, feel free to open an issue or contact me via [LinkedIn](https://www.linkedin.com/in/farinazgoli/) or [GitHub](https://github.com/Farinaz94).
