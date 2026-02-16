from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status as s
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status_code: int
    message: str


class NotFoundException(HTTPException):
    def __init__(self, message="Data not found!") -> None:
        super().__init__(status_code=s.HTTP_404_NOT_FOUND, detail=message)


class BadRequestException(HTTPException):
    def __init__(self, message="Bad Request.") -> None:
        super().__init__(status_code=s.HTTP_400_BAD_REQUEST, detail=message)


class UnauthorizedException(HTTPException):
    def __init__(self, message="Unauthorized") -> None:
        super().__init__(status_code=s.HTTP_401_UNAUTHORIZED, detail=message)


class ForbiddenException(HTTPException):
    def __init__(self, message="Forbidden request.") -> None:
        super().__init__(status_code=s.HTTP_403_FORBIDDEN, detail=message)


class ConflictException(HTTPException):
    def __init__(self, message="Conflict occurred") -> None:
        super().__init__(status_code=s.HTTP_409_CONFLICT, detail=message)


class InternalServerErrorException(HTTPException):
    def __init__(self, message="Internal Server Error") -> None:
        super().__init__(status_code=s.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)


class PaymentFailureException(HTTPException):
    def __init__(self, message="Payment failure", meta_data=None) -> None:
        super().__init__(status_code=s.HTTP_402_PAYMENT_REQUIRED, detail=message)
        self.meta_data = meta_data


async def payment_failure_exception_handler(
    request, exc: PaymentFailureException
) -> JSONResponse:
    res = ErrorResponse(status_code=exc.status_code, message=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=res.model_dump())


async def not_found_exception_handler(request, exc: NotFoundException) -> JSONResponse:
    res = ErrorResponse(status_code=exc.status_code, message=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=res.model_dump())


async def bad_request_exception_handler(
    request, exc: BadRequestException
) -> JSONResponse:
    res = ErrorResponse(status_code=exc.status_code, message=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=res.model_dump())


async def unauthorized_exception_handler(
    request, exc: UnauthorizedException
) -> JSONResponse:
    res = ErrorResponse(status_code=exc.status_code, message=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=res.model_dump())


async def forbidden_exception_handler(request, exc: ForbiddenException) -> JSONResponse:
    res = ErrorResponse(status_code=exc.status_code, message=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=res.model_dump())


async def conflict_exception_handler(request, exc: ConflictException) -> JSONResponse:
    res = ErrorResponse(status_code=exc.status_code, message=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=res.model_dump())


async def internal_server_error_exception_handler(
    request, exc: InternalServerErrorException
) -> JSONResponse:
    res = ErrorResponse(status_code=exc.status_code, message=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=res.model_dump())


async def validation_exception_handler(
    request, exc: RequestValidationError
) -> JSONResponse:
    first_error = exc.errors()[0]  # Get the first validation error
    field = first_error.get("loc")[-1]
    message = first_error.get("msg")

    content = {
        "message": f"{field} {message}",
        "status_code": s.HTTP_422_UNPROCESSABLE_ENTITY,
    }

    return JSONResponse(
        status_code=s.HTTP_422_UNPROCESSABLE_ENTITY,
        content=content,
    )