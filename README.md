# Fastest - FastAPI Backend Service

This project is a modern backend service built with FastAPI, SQLAlchemy, and Docker. It provides a robust foundation for building scalable web applications with built-in authentication, database migrations, and containerization support.

## Features

- **FastAPI Framework**: High performance, easy to learn, fast, and ready for production.
- **Authentication**: Secure user authentication using JWT (JSON Web Tokens) and bcrypt for password hashing.
- **Google OAuth**: Integration with Google APIs for authentication and services.
- **Database ORM**: SQLAlchemy for database interactions with Alembic for migrations.
- **Validation**: Pydantic models for data validation and serialization.
- **Containerization**: Docker and Docker Compose support for easy deployment and development.
- **NanoID**: Generates URL-friendly unique string IDs.

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional, for containerized deployment)

## Installation

### Method 1: Docker (Recommended)

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd fastest
   ```

2. **Configure Environment Variables:**
   Copy the example environment file and update it with your credentials.

   ```bash
   cp .env.example .env
   ```

3. **Build and Run:**
   ```bash
   docker-compose up --build
   ```
   The API will be available at `http://localhost:8000`.

### Method 2: Local Development

1. **Create a Virtual Environment:**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**

   ```bash
   cp .env.example .env
   # Edit .env with your database and API keys
   ```

4. **Run the Server:**
   ```bash
   uvicorn src.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

```
.
├── docker-compose.yml   # Docker services configuration
├── Dockerfile           # App container definition
├── requirements.txt     # Python dependencies
├── src/
│   ├── api/             # API routes and controllers
│   │   └── v1/          # Version 1 API
│   │       ├── auth/    # Authentication module
│   │           ├── route.py
│   │           ├── schema.py
│   │           └── service.py
│   ├── db/              # Database configuration and models
│   ├── models/          # SQLAlchemy models
│   ├── utils/           # Utility functions (e.g., email, security)
│   ├── config.py        # App configuration
│   └── main.py          # Application entry point
└── ...
```
