from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status as s
from typing import Any


class ApiResponse(JSONResponse):
    def __init__(
        self,
        data: Any = None,
        message: str = None,
        status_code: int = s.HTTP_200_OK,
        meta: Any = None,
    ) -> None:
        super().__init__(
            {
                "status_code": status_code,
                "message": message if message else "Data retrieved successfully",
                "data": jsonable_encoder(data),
                **({"meta": jsonable_encoder(meta)} if meta else {}),
            },
            status_code=status_code if status_code else s.HTTP_200_OK,
            headers={"Content-Type": "application/json"},
        )