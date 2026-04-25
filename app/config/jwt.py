import uuid
from dataclasses import dataclass
import jwt
from jwt import PyJWKClient
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.env import settings
from app.exceptions.app_exceptions import UnauthorizedException

#APIのAuhthorizationHeaderにBearerトークンを要求するオブジェクト
#これをするだけでSwaggerに Authorize ボタンが自動で表示される
# リクエストが来たときに Authorization: Bearer <token> ヘッダーを取り出す役割も担う
_bearer = HTTPBearer()
#Supabaseの公開鍵一覧を取得・キャッシュ（モジュール読み込み時に1回のみ作成される）
_jwks_client = PyJWKClient(f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json")


# JWTから取り出したユーザー情報を型安全に運ぶ内部DTO
# dictだとキー名ミスが実行時まで気づけないため、型付きのdataclassを使う
# Pydantic BaseModelはAPI境界のバリデーション用なので内部受け渡しには使わない
@dataclass
class UserTokenInfo:
    id: uuid.UUID
    email: str
    name: str
    avatar_url: str | None


def _decode_payload(token: str) -> dict:
    # JWTのkid（Key ID）でSupabaseの公開鍵を特定し、署名を検証してpayloadを返す
    signing_key = _jwks_client.get_signing_key_from_jwt(token)
    return jwt.decode(
        token,
        signing_key.key,
        algorithms=["ES256"],
        audience="authenticated",
        issuer=f"{settings.SUPABASE_URL}/auth/v1",
    )


async def get_current_user_id(
    #_bearer を使ってAuthorizationヘッダーからトークンを取り出す
    #credentials.credentials が実際のJWT文字列
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> uuid.UUID:
    # 認証のみ必要なエンドポイント用（ユーザーIDだけ返す）
    try:
        payload = _decode_payload(credentials.credentials)
        #sub（subject）がSupabaseのユーザーIDを返す
        return uuid.UUID(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise UnauthorizedException()


async def get_current_user_info(
    #_bearer を使ってAuthorizationヘッダーからトークンを取り出す
    #credentials.credentials が実際のJWT文字列
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> UserTokenInfo:
    # ユーザー情報のupsertが必要なエンドポイント用（GET /users/me）
    try:
        payload = _decode_payload(credentials.credentials)
        meta = payload.get("user_metadata", {})
        email = payload["email"]
        # Google認証: user_metadata.full_name / Email認証: nameがないのでemailの@前を使う
        name = meta.get("full_name") or email.split("@")[0]
        # Google認証: Googleのプロフィール画像URL / Email認証: None
        avatar_url = meta.get("avatar_url")
        return UserTokenInfo(
            id=uuid.UUID(payload["sub"]),
            email=email,
            name=name,
            avatar_url=avatar_url,
        )
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise UnauthorizedException()
