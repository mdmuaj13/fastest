from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db.database import init_db
from src.api.v1.routes import register_v1_routes
# Import models so they are registered with Base before init_db()
from src.api.v1.test.service import TestModel  # noqa: F401
from src.api.v1.auth.service import UserModel  # noqa: F401
from src.utils.exceptions import (
    BadRequestException,
    ConflictException,
    ForbiddenException,
    InternalServerErrorException,
    NotFoundException,
    RequestValidationError,
    UnauthorizedException,
    bad_request_exception_handler,
    conflict_exception_handler,
    forbidden_exception_handler,
    internal_server_error_exception_handler,
    not_found_exception_handler,
    unauthorized_exception_handler,
    validation_exception_handler,
)

def register_routes(server: FastAPI):
    register_v1_routes(server)

def register_exceptions(server: FastAPI):
    server.add_exception_handler(BadRequestException, bad_request_exception_handler)
    server.add_exception_handler(ConflictException, conflict_exception_handler)
    server.add_exception_handler(ForbiddenException, forbidden_exception_handler)
    server.add_exception_handler(InternalServerErrorException, internal_server_error_exception_handler)
    server.add_exception_handler(NotFoundException, not_found_exception_handler)
    server.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
    server.add_exception_handler(RequestValidationError, validation_exception_handler)

def register_middleware(server: FastAPI):
    pass

def create_app():
    # Initialize database tables at startup
    init_db()
    
    server = FastAPI(
      title="Registro API",
      description="Registro API",
      version="1.0.0",
      docs_url="/docs"
    )

    # Add CORS middleware
    server.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    # Include routers
    register_routes(server)
    @server.get("/")
    def root():
        return {"message": "Ok. Registro API running."}

    # Include exceptions
    register_exceptions(server)

    # Include middleware
    register_middleware(server)

    print("Server started")

    return server



app = create_app()
