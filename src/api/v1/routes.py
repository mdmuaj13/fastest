from fastapi import FastAPI
from .test.route import router as test_router
from .auth.route import router as auth_router

def register_v1_routes(app: FastAPI):
    @app.get("/v1/health")
    def health():
        return {"status": "ok"}

    # app.include_router(test_router, prefix="/v1")
    app.include_router(auth_router, prefix="/v1")
