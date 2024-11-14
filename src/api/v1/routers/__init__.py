__all__ = [
    "v1_company_router",
    "v1_company_router",
    "router1",
    "auth_router",
    "v1_task_router",
    "v1_user_router",
]

from .company import router as v1_company_router
from .user import router as v1_user_router
from .structure import router1
from .auth import router as auth_router
from .task import router as v1_task_router
