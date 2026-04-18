import uuid
from app.repositories.user_repository import UserRepository
from app.schemas.requests.user import UserUpdateRequest
from app.models.user import User
from app.exceptions.app_exceptions import NotFoundException


class UserUsecase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_me(self, user_id: uuid.UUID) -> User:
        user = await self.repository.find_by_id(user_id)
        if not user:
            raise NotFoundException("ユーザーが見つかりません")
        return user

    async def update_me(self, user_id: uuid.UUID, request: UserUpdateRequest) -> User:
        user = await self.repository.find_by_id(user_id)
        if not user:
            raise NotFoundException("ユーザーが見つかりません")
        return await self.repository.update(user, request)
