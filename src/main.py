from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse

from fastapi import APIRouter
from .api.v1.routers.company import router as v1_company_router
from .api.v1.routers.user import router as v1_user_router
from src.api.auth.auth import router as auth_router

router = APIRouter()
router.include_router(v1_user_router, prefix='/v1', tags=['User | v1'])
router.include_router(v1_company_router, prefix='/v1', tags=['Company | v1'])
router.include_router(auth_router)

app = FastAPI(title="Business Management System")
app.include_router(router, prefix='/api')


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )