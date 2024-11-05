from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from src.models.user import UserModel
from src.schemas.user import UserRequest
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class UserService(BaseService):
    base_repository: str = 'user'

    @transaction_mode
    async def create_user(self, user: UserRequest) -> UserModel:
        """Create user."""
        return await self.uow.user.add_one_and_get_obj(**user.model_dump(exclude_none=True))

    @transaction_mode
    async def get_user_by_id(self, user_id: int) -> UserModel:
        """Get user by ID."""
        user: UserModel | None = await self.uow.user.get_by_query_one_or_none(id=user_id)
        self._check_user_exists(user)
        return user

    @transaction_mode
    async def update_user(self, user_id: int, user: UserRequest) -> UserModel:
        """Update user by ID."""
        user: UserModel | None = await self.uow.user.update_one_by_id(obj_id=user_id, **user.model_dump())
        self._check_user_exists(user)
        return user

    @transaction_mode
    async def delete_user(self, user_id: int) -> None:
        """..."""
        await self.uow.user.delete_by_query(id=user_id)


    @staticmethod
    def _check_user_exists(user: UserModel | None) -> None:
        """..."""
        if not user:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='User not found')
