from fastapi import Depends
from fastapi.security import HTTPBearer

import src.api.v1.services as serv
from src.utils.auth_validation import get_current_user_from_token
from src.utils.service import BaseService

http_bearer = HTTPBearer()


def get_service_dep(service_name: str):
    return Depends(services.get(service_name, BaseService))


token_dep = Depends(http_bearer)


async def get_user_from_token(token=token_dep):
    user = await get_current_user_from_token(token)
    return user


async def get_company_from_token(
    token=token_dep,
):
    user = await get_current_user_from_token(token)
    return user.company


services = {
    "company": serv.CompanyService,
    "user": serv.UserService,
    "task": serv.TaskService,
    "position": serv.PositionService,
}
