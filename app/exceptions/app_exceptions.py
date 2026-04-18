from dataclasses import dataclass, field


@dataclass
class AppException(Exception):
    message: str
    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"
    details: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__init__(self.message)


@dataclass
class NotFoundException(AppException):
    message: str = "リソースが見つかりません"
    status_code: int = 404
    error_code: str = "NOT_FOUND"


@dataclass
class ForbiddenException(AppException):
    message: str = "この操作を行う権限がありません"
    status_code: int = 403
    error_code: str = "FORBIDDEN"


@dataclass
class UnauthorizedException(AppException):
    message: str = "認証が必要です"
    status_code: int = 401
    error_code: str = "UNAUTHORIZED"


@dataclass
class ConflictException(AppException):
    message: str = "既に存在しています"
    status_code: int = 409
    error_code: str = "CONFLICT"


@dataclass
class AlreadyMemberException(AppException):
    message: str = "すでにこの旅行のメンバーです"
    status_code: int = 409
    error_code: str = "ALREADY_MEMBER"


@dataclass
class InvalidInviteCodeException(AppException):
    message: str = "招待コードが無効です"
    status_code: int = 422
    error_code: str = "INVALID_INVITE_CODE"


@dataclass
class InvalidDateRangeException(AppException):
    message: str = "出発日は帰宅日より前である必要があります"
    status_code: int = 400
    error_code: str = "INVALID_DATE_RANGE"
