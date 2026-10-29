# Spaced Repetition Vocabulary Trainer

A full-stack vocabulary learning application that helps users learn new words, review them at scheduled intervals, and track learning progress using a spaced-repetition algorithm.

## Features

- Add vocabulary words with definitions and language.
- Retrieve words that are due for review.
- Submit review scores from 0 to 5.
- Schedule future reviews using an SM-2-inspired algorithm.
- View learning history and review accuracy.
- Track consecutive-day learning streaks.
- View upcoming reviews and difficult words.
- Delete vocabulary words and their associated reviews.
- Access interactive API documentation.
- Use a React frontend connected to a FastAPI backend.
- Use a generated Python SDK based on the OpenAPI specification.

## Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Pydantic

### Frontend

- React
- Vite
- Axios

### SDK

- OpenAPI Generator CLI
- Generated Python client

### Testing

- pytest
- FastAPI test client

## Project Structure

```text
vocabulary-trainer/
├── main.py
├── models.py
├── database.py
├── requirements.txt
├── alembic.ini
├── migrations/
│   ├── env.py
│   └── versions/
├── tests/
│   ├── conftest.py
│   └── test_main.py
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── sdk/
│   └── python-client/
├── seed_data.sql
├── setupdev.bat
├── runapplication.bat
└── README.md
```

## Prerequisites

Install the following software:

- Python 3.10 or newer
- Node.js and npm
- Java, if you need to run the OpenAPI Generator CLI workflow

## Installation

### Option 1: Windows setup script

From the project root directory, run:

```powershell
.\setupdev.bat
```

The script creates the Python virtual environment if needed and installs the backend and frontend dependencies.

Wait for the script to finish before starting the application.

### Option 2: Manual setup

#### 1. Create and activate the Python environment

Run these commands from the project root:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

If PowerShell blocks script execution, you can temporarily allow activation scripts in the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\env\Scripts\Activate.ps1
```

#### 2. Install backend dependencies

```powershell
python -m pip install -r requirements.txt
```

#### 3. Install frontend dependencies

```powershell
cd frontend
npm install
cd ..
```

## Database

The application uses SQLite by default.

```text
sqlite:///./vocabulary.db
```

The database file is created in the project root when the application initializes the database.

It stores vocabulary words and their review records.

### Database migrations

Alembic manages database schema migrations.

To inspect the current migration revision:

```powershell
alembic current
```

To list the available migration heads:

```powershell
alembic heads
```

For a new or appropriately prepared database, apply migrations with:

```powershell
alembic upgrade head
```

**Important:** Back up an existing database before applying migrations or changing its schema. Do not stamp, reset, or recreate an existing database without understanding its current migration state.

## Running the Application

### Option 1: Windows launch script

From the project root, run:

```powershell
.\runapplication.bat
```

The script opens separate terminal windows for the backend and frontend.

Keep both terminal windows running while using the application.

### Option 2: Run manually

#### 1. Start the backend

From the project root:

```powershell
.\env\Scripts\Activate.ps1
python -m uvicorn main:app --reload
```

The backend should be available at:

```text
http://127.0.0.1:8000
```

#### 2. Start the frontend

Open a second terminal and run:

```powershell
cd frontend
npm run dev
```

Open the frontend URL displayed by Vite in the terminal. Vite may use port `5173` or another available port, such as `5174`.

## Application URLs

When the backend is running on the default port:

| Service | URL |
|---|---|
| Frontend | Use the URL displayed by Vite |
| Backend | http://127.0.0.1:8000 |
| Interactive API documentation | http://127.0.0.1:8000/docs |
| OpenAPI specification | http://127.0.0.1:8000/openapi.json |
| Health check | http://127.0.0.1:8000/health |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns the API welcome message |
| GET | `/health` | Checks backend health |
| POST | `/words/` | Adds a vocabulary word |
| GET | `/words/due/` | Retrieves words due for review |
| POST | `/words/{word_id}/review/` | Submits a review score |
| GET | `/words/history/` | Retrieves learning history and review accuracy |
| GET | `/words/insights/` | Retrieves learning streak, upcoming reviews, and difficult words |
| DELETE | `/words/{word_id}` | Deletes a vocabulary word and its review records |

For request schemas, response formats, and interactive testing, open the FastAPI documentation at `/docs`.

## Review Scheduling

Review scores range from 0 to 5.

The scheduling algorithm updates the following values based on the submitted score and previous review:

- Repetition count
- Easiness factor
- Review interval
- Next review date

Lower scores generally cause the repetition count to reset and schedule an earlier review. Higher scores generally allow longer intervals between reviews.

The algorithm is inspired by the SM-2 spaced-repetition method.

## Generating the Python SDK

The Python SDK is generated from the running FastAPI application's OpenAPI specification.

The generated client is located in:

```text
sdk/python-client/
```

### Generate the SDK

First, ensure Java and Node.js are installed. Install the generator development dependency from the project root if it is not already installed:

```powershell
npm install @openapitools/openapi-generator-cli -D
```

Start the backend, then run the following command from the project root:

```powershell
npx openapi-generator-cli generate `
  -i http://127.0.0.1:8000/openapi.json `
  -g python `
  -o .\sdk\python-client `
  --additional-properties=packageName=vocabulary_trainer_client
```

Refer to `sdk/python-client/README.md` for generated-client installation and usage instructions.

Regenerating the SDK may update generated files. Review those changes before committing or distributing the project.

## Running Tests

Activate the Python virtual environment and run the tests from the project root:

```powershell
python -m pytest -v
```

### Verified results

The project has been tested locally with the following results:

- **Backend and generated SDK tests:** 28 passed.
- **Frontend production build:** successful.
- **Adding vocabulary words:** verified.
- **Submitting reviews and viewing learning history:** verified.
- **Dashboard statistics:** verified.
- **Database persistence after restarting the backend:** verified.

The test run reported one Starlette deprecation warning related to the HTTPX test client. It did not cause any tests to fail.

## Frontend Production Build

To create a production build, run:

```powershell
cd frontend
npm run build
```

Vite generates the production files in `frontend/dist/`.

The build output is generated and does not need to be committed when distributing the source code.

## Seed Data

The repository includes `seed_data.sql` for sample data.

Before importing seed data:

1. Back up the database.
2. Confirm that the database schema exists.
3. Review the SQL statements to understand what they insert or modify.
4. Avoid running the script repeatedly if it can create duplicate records.

Use sample data only when needed for development or demonstration.

## Troubleshooting

### Backend does not start

Confirm that the Python virtual environment is activated and dependencies are installed:

```powershell
python -m pip install -r requirements.txt
```

Check that port `8000` is available and inspect the terminal for the exact error message.

### Frontend cannot connect to the backend

Confirm that the backend is running at:

```text
http://127.0.0.1:8000
```

Open the frontend using the URL displayed by Vite. Check the CORS configuration in `main.py` if the browser reports CORS errors. The frontend origin must match an allowed origin in the backend configuration.

### SDK generation fails

Confirm that Java is installed, the backend is running, and the OpenAPI specification is accessible:

```text
http://127.0.0.1:8000/openapi.json
```

Check the terminal output for generator errors.

### Migration errors

Inspect the current revision and available heads:

```powershell
alembic current
alembic heads
```

Back up the database before making changes to migration history or applying schema changes. Avoid stamping or recreating an existing database merely to bypass a migration error.

### Tests fail

Run the tests from the project root with the intended virtual environment activated:

```powershell
python -m pytest -v
```

Read the first failure and its traceback before changing application code.

## Version Control and Generated Files

The root `.gitignore` should exclude generated files and local-only artifacts such as:

- Python cache directories
- Virtual environments
- `frontend/node_modules/`
- `frontend/dist/`
- Local database files, if they are not intended for distribution
- Temporary migration-test files
- Environment files containing secrets

Keep the source code, migration files, tests, setup scripts, and any required generated SDK files.

If a sample database is required for evaluation, provide a sanitized copy rather than a database containing private or unintended data.

## License

Add the project's chosen license before distributing it publicly.
