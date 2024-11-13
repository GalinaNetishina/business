from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse

from fastapi import APIRouter
import src.api.v1.routers as routs
from .schemas.response import ErrorResponse

router = APIRouter()
# router.include_router(routs.v1_user_router, prefix="/v1", tags=["User | v1"])
# router.include_router(routs.v1_company_router, prefix="/v1", tags=["Company | v1"])
router.include_router(routs.auth_router, prefix="/v1", tags=["Auth | v1"])
# router.include_router(routs.router1, tags=["Structure | v1"])
router.include_router(routs.v1_task_router, prefix="/v1", tags=["Task | v1"])

app = FastAPI(title="Business Management System")
app.include_router(router, prefix="/api")


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(status=exc.status_code, payload=exc.detail).model_dump(),
    )
