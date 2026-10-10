
# Bulk Certificate Generator

A REST API built using FastAPI, PostgreSQL, SQLAlchemy, and ReportLab
to generate certificates in bulk.

## Features

- Create bulk certificate generation jobs.
- Validate recipient details and email addresses.
- Generate PDF certificates using one predefined template.
- Track job status, progress, and recipient-level failures.
- Continue processing when an individual certificate fails.
- List and download generated certificates.
- Run automated API and service tests.

## Technology Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- ReportLab
- Pytest

## Prerequisites

- Python 3.10 or later
- PostgreSQL 18
- pgAdmin 4 (optional, for database management)

## Installation on Windows

### 1. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Create the PostgreSQL database

In pgAdmin, right-click Databases, select Create > Database,
and name the database:

certificate_db

### 4. Configure environment variables

Create a `.env` file in the project root:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/certificate_db
CERTIFICATE_DIR=generated
```

Replace YOUR_PASSWORD with your PostgreSQL password.

### 5. Run the application

From the project root:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API welcome message |
| GET | /health | Health check |
| POST | /api/jobs | Create a bulk generation job |
| GET | /api/jobs/{job_id} | Get status and progress |
| GET | /api/jobs/{job_id}/certificates | List generated certificates |
| GET | /api/certificates/{certificate_id} | Download a PDF |

## Example Request

POST /api/jobs

```json
{
  "course_name": "Python Programming",
  "certificate_date": "2026-10-10",
  "recipients": [
    {
      "name": "Aditya Kumar",
      "email": "aditya@example.com"
    },
    {
      "name": "Priya Sharma",
      "email": "priya@example.com"
    }
  ]
}
```

Example response:

```json
{
  "id": 1,
  "status": "queued",
  "total_count": 2
}
```

## Check Job Status

GET /api/jobs/1

The response includes:

- Job status
- Total recipients
- Successful and failed counts
- Progress percentage
- Individual recipient statuses and error messages

## Retrieve Certificates

List certificates:

GET /api/jobs/1/certificates

Download a certificate:

GET /api/certificates/1

## Run Tests

```powershell
python -m pytest -v
```

The tests use SQLite and do not require a connection to the
PostgreSQL database configured for the application.

## Design Decisions

- FastAPI provides request validation and REST endpoints.
- SQLAlchemy manages database models and sessions.
- PostgreSQL stores jobs, recipients, and certificate metadata.
- ReportLab generates PDF files from a single predefined template.
- BackgroundTasks separates job submission from processing.
- Each recipient is processed independently to prevent one
  generation failure from stopping the entire batch.

## Limitations and Future Improvements

FastAPI BackgroundTasks are suitable for this starter project but
are not a durable job queue. For production, consider Celery or
another persistent queue, database migrations, authentication,
file-storage management, retry policies, and monitoring.
