import uuid
from app.repositories.user_repository import UserRepository
from app.schemas.requests.user import UserUpdateRequest
from app.models.user import User
from app.config.jwt import UserTokenInfo
from app.exceptions.app_exceptions import NotFoundException


class UserUsecase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_me(self, user_info: UserTokenInfo) -> User:
        user = await self.repository.find_by_id(user_info.id)
        if not user:
            # 初回ログイン時にJWTの情報からユーザーを自動作成する
            user = await self.repository.create(
                id=user_info.id,
                email=user_info.email,
                name=user_info.name,
                avatar_url=user_info.avatar_url,
            )
        return user

    async def update_me(self, user_id: uuid.UUID, request: UserUpdateRequest) -> User:
        user = await self.repository.find_by_id(user_id)
        if not user:
            raise NotFoundException("ユーザーが見つかりません")
        return await self.repository.update(user, request)
