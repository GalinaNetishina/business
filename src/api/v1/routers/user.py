"""The module contains base routes for working with user."""

from fastapi import APIRouter
from pydantic import UUID4
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.schemas.user import (
    UserRequest,
    CreateUserResponse,
    UserResponse,
    UserDB, UserUpdateRequest,
)
from src.utils.dependencies import get_service_dep


router = APIRouter(prefix="/user")


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
)
async def create_user(
    user: UserRequest,
    service=get_service_dep('user'),
) -> CreateUserResponse:
    """Create user."""
    created_user = await service.create_user(user)
    return CreateUserResponse(payload=UserDB.model_validate(created_user))


@router.get(
    path="/{user_id}",
    status_code=HTTP_200_OK,
)
async def get_user(
    user_id: UUID4,
    service=get_service_dep('user'),
) -> UserResponse:
    """Get user by ID."""
    user = await service.get_user_by_id(user_id)
    return UserResponse(payload=UserDB.model_validate(user))


@router.put(
    path="/{user_id}",
    status_code=HTTP_200_OK,
)
async def update_user(
    user_id: UUID4,
    user: UserUpdateRequest,
    service=get_service_dep('user'),
) -> UserResponse:
    """Update user."""
    updated_user = await service.update_user(user_id, user)
    return UserResponse(payload=UserDB.model_validate(updated_user))


@router.delete(
    "/{user_id}",
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: UUID4,
    service=get_service_dep('user'),
) -> None:
    """Delete user."""
    await service.delete_user(user_id)
