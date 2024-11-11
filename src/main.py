from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse

from fastapi import APIRouter
from .api.v1.routers.company import router as v1_company_router
from .api.v1.routers.user import router as v1_user_router
from .api.v1.routers.structure import router1
from src.api.v1.routers.auth import router as auth_router
from .schemas.response import ErrorResponse

router = APIRouter()
router.include_router(v1_user_router, prefix="/v1", tags=["User | v1"])
router.include_router(v1_company_router, prefix="/v1", tags=["Company | v1"])
router.include_router(auth_router)
router.include_router(router1, tags=["Structure | v1"])

app = FastAPI(title="Business Management System")
app.include_router(router, prefix="/api")


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(status=exc.status_code, payload=exc.detail).model_dump()
    )
