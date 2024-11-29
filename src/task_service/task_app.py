from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse

from fastapi import APIRouter
from .task_routs import router as task_router
from src.schemas.response import ErrorResponse


router = APIRouter()
router.include_router(task_router, prefix="/v1", tags=["Task | v1"])

app = FastAPI(title="Business Management System")
app.include_router(router, prefix="/api")


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(status=exc.status_code, payload=exc.detail).model_dump(),
    )
