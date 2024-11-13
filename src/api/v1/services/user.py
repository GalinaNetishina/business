from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from src.models.user import UserModel
from src.schemas.user import UserRequest
from src.utils.auth import hash_password
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class UserService(BaseService):
    base_repository: str = "user"

    @transaction_mode
    async def create_user(self, user_data: UserRequest) -> UserModel:
        """Create user."""
        user = await self.get_user_by_email(user_data.email)
        if user:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail="user exists")
        db_user = user_data.model_copy()
        db_user.password = hash_password(user_data.password)
        return await self.uow.user.add_one_and_get_obj(
            **db_user.model_dump(exclude_none=True)
        )

    @transaction_mode
    async def get_user_by_id(self, user_id: int) -> UserModel:
        """Get user by ID."""
        user: UserModel | None = await self.uow.user.get_by_query_one_or_none(
            id=user_id
        )
        self._check_user_exists(user)
        return user

    @transaction_mode
    async def get_user_by_phone(self, phone_number: str) -> UserModel:
        """Get user by phone."""
        user: UserModel | None = await self.uow.user.get_by_query_one_or_none(
            phone_number=phone_number
        )
        return user

    @transaction_mode
    async def get_user_by_email(self, email: str) -> UserModel:
        """Get user by email."""
        user: UserModel | None = await self.uow.user.get_by_query_one_or_none(
            email=email
        )
        print(user)
        return user

    @transaction_mode
    async def update_user(self, user_id: int, user: UserRequest) -> UserModel:
        """Update user by ID."""
        user: UserModel | None = await self.uow.user.update_one_by_id(
            obj_id=user_id, **user.model_dump(exclude=set(["password"]))
        )
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
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
