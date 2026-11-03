# Task Manager API

A RESTful API for managing tasks, built with Python, FastAPI, SQLAlchemy, and PostgreSQL.

This project is designed to practice backend development, REST API design, database integration, and working with Docker.

## Technologies

- **Python** — main programming language
- **FastAPI** — web framework
- **SQLAlchemy** — ORM for database operations
- **PostgreSQL** — relational database
- **Pydantic** — request validation and response serialization
- **Docker Compose** — PostgreSQL container management
- **Pytest** — automated testing

## Features

- Retrieve all tasks
- Retrieve a task by ID
- Create a new task
- Validate incoming request data
- Handle missing tasks with HTTP 404 responses
- Store tasks in PostgreSQL

## Project Structure

```text
task-manager/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── routers/
│   └── schemas/
├── tests/
├── .env.example
├── .gitignore
├── docker-compose.yaml
├── requirements.txt
└── seed.py
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/UraN9/task-manager.git
cd task-manager
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create your local `.env` file from the example:

```bash
cp .env.example .env
```

Update the values if necessary.

Example configuration:

```env
POSTGRES_USER=task_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=task_manager

DATABASE_URL=postgresql+psycopg://task_user:your_password@localhost:5434/task_manager
```

### 5. Start PostgreSQL

Make sure Docker is running, then execute:

```bash
docker compose up -d
```

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

## API Documentation

FastAPI automatically generates interactive API documentation.

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description | Success |
|---|---|---|---|
| GET | `/tasks/` | Retrieve all tasks | 200 |
| GET | `/tasks/{task_id}` | Retrieve a task by ID | 200 |
| POST | `/tasks/` | Create a new task | 201 |

### Create a Task

**POST** `/tasks/`

Request body:

```json
{
  "title": "Learn FastAPI",
  "completed": false
}
```

Response:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "completed": false
}
```

### Retrieve a Task

**GET** `/tasks/1`

Response:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "completed": false
}
```

If the task does not exist, the API returns `404 Not Found`.

## Running Tests

Run the test suite with:

```bash
pytest
```

To generate a coverage report:

```bash
pytest --cov=app
```

## License

This project is intended for educational and portfolio purposes.