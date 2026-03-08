# 旅行予定管理アプリ バックエンド ディレクトリ構成書

> **Version:** 1.0
> **最終更新日:** 2026-03-08
> **フレームワーク:** FastAPI
> **アーキテクチャ:** Clean Architecture
> **対応API仕様書:** v1.0
> **対応DB設計書:** v3.1

---

## 1. 概要

本ドキュメントでは、旅行予定管理アプリのバックエンドを FastAPI + Clean Architecture で構築する際のディレクトリ構成を定義します。

Clean Architecture の原則に従い、依存関係を常に内側（ビジネスロジック）に向けることで、フレームワークやDBの変更がコアロジックに影響しない設計を実現します。

---

## 2. アーキテクチャとレイヤー対応

```
┌─────────────────────────────────────────────────┐
│         Frameworks & Drivers（最外層）            │
│   infrastructure/ , config/                      │
│   DB接続, Google OAuth, Google Places, Slack等    │
├─────────────────────────────────────────────────┤
│         Interface Adapters                       │
│   routers/ , schemas/                            │
│   APIエンドポイント定義, リクエスト/レスポンスDTO  │
├─────────────────────────────────────────────────┤
│         Use Cases                                │
│   usecases/                                      │
│   アプリケーション固有のビジネスロジック           │
├─────────────────────────────────────────────────┤
│         Entities（最内層）                        │
│   models/ , repositories/                        │
│   ドメインモデル, データアクセスの抽象化           │
└─────────────────────────────────────────────────┘
          ※ 依存方向: 外側 → 内側（一方向のみ）
```

| レイヤー | 対応フォルダ | 役割 |
|---|---|---|
| Entities | `models/`, `repositories/` | ドメインモデル（SQLAlchemy ORM）とデータアクセス操作の定義 |
| Use Cases | `usecases/` | ビジネスロジックの集約。Repository を依存注入で受け取り、ドメイン操作を組み立てる |
| Interface Adapters | `routers/`, `schemas/` | APIエンドポイント（Controller相当）と、リクエスト/レスポンスのDTO（Pydantic） |
| Frameworks & Drivers | `infrastructure/`, `config/` | DB接続、外部API連携、JWT処理、環境変数管理など技術依存の実装 |

---

## 3. ディレクトリ構成

```
.
├── application/
│   ├── main.py                          # FastAPI アプリケーションエントリポイント
│   │
│   ├── config/                          # 設定・依存注入
│   │   ├── __init__.py
│   │   ├── dependency.py                # DI定義（Usecase・Repository の注入）
│   │   ├── env.py                       # 環境変数の読み込み
│   │   └── jwt.py                       # JWT エンコード・デコード
│   │
│   ├── infrastructure/                  # 外部技術依存の実装
│   │   ├── __init__.py
│   │   ├── database.py                  # SQLAlchemy エンジン・セッション管理
│   │   ├── google_oauth.py              # Google OAuth トークン検証
│   │   └── google_places.py             # Google Places API クライアント
│   │
│   ├── models/                          # ドメインモデル（SQLAlchemy ORM）
│   │   ├── __init__.py
│   │   ├── user.py                      # Users モデル
│   │   ├── trip.py                      # Trips モデル
│   │   ├── trip_member.py               # TripMembers モデル
│   │   ├── spot.py                      # Spots モデル
│   │   ├── candidate_spot.py            # CandidateSpots モデル
│   │   ├── candidate_reaction.py        # CandidateReactions モデル
│   │   └── itinerary_activity.py        # ItineraryActivities モデル
│   │
│   ├── repositories/                    # データアクセス層
│   │   ├── __init__.py
│   │   ├── user_repository.py           # ユーザーの CRUD
│   │   ├── trip_repository.py           # 旅行プロジェクトの CRUD
│   │   ├── trip_member_repository.py    # メンバー管理
│   │   ├── spot_repository.py           # スポットキャッシュの検索・登録
│   │   ├── candidate_spot_repository.py # 候補スポットの CRUD
│   │   ├── candidate_reaction_repository.py # リアクションの CRUD
│   │   └── itinerary_activity_repository.py # タイムラインの CRUD・並べ替え
│   │
│   ├── usecases/                        # ビジネスロジック層
│   │   ├── __init__.py
│   │   ├── auth_usecase.py              # Google OAuth 認証・トークン発行
│   │   ├── user_usecase.py              # プロフィール取得・更新
│   │   ├── trip_usecase.py              # 旅行の作成・更新・削除
│   │   ├── trip_member_usecase.py       # 招待・参加・ロール変更・退出
│   │   ├── candidate_spot_usecase.py    # 候補追加・ステータス変更・削除
│   │   ├── candidate_reaction_usecase.py # リアクション登録・削除
│   │   ├── itinerary_usecase.py         # タイムライン取得・追加・更新・並べ替え
│   │   └── spot_search_usecase.py       # Google Places 検索 → キャッシュ保存
│   │
│   ├── routers/                         # APIエンドポイント定義
│   │   ├── __init__.py
│   │   ├── auth.py                      # POST /auth/google, /auth/refresh
│   │   ├── users.py                     # GET/PATCH /users/me
│   │   ├── trips.py                     # CRUD /trips, /trips/:tripId
│   │   ├── trip_members.py              # /trips/:tripId/join, /members
│   │   ├── candidates.py               # /trips/:tripId/candidates
│   │   ├── reactions.py                 # /trips/:tripId/candidates/:id/reactions
│   │   ├── itinerary.py                 # /trips/:tripId/itinerary
│   │   └── spots.py                     # GET /spots/search
│   │
│   ├── schemas/                         # リクエスト/レスポンス DTO
│   │   ├── __init__.py
│   │   ├── requests/
│   │   │   ├── __init__.py
│   │   │   ├── auth_request.py          # GoogleAuthRequest, RefreshRequest
│   │   │   ├── trip_request.py          # TripCreate, TripUpdate
│   │   │   ├── member_request.py        # JoinRequest, RoleUpdate
│   │   │   ├── candidate_request.py     # CandidateCreate, CandidateStatusUpdate
│   │   │   ├── reaction_request.py      # ReactionRequest
│   │   │   └── itinerary_request.py     # ActivityCreate, ActivityUpdate, ReorderRequest
│   │   └── responses/
│   │       ├── __init__.py
│   │       ├── auth_response.py         # AuthResponse, TokenResponse
│   │       ├── user_response.py         # UserResponse
│   │       ├── trip_response.py         # TripResponse, TripListItem
│   │       ├── member_response.py       # MemberResponse, MemberSummary
│   │       ├── candidate_response.py    # CandidateSpotResponse
│   │       ├── reaction_response.py     # ReactionResponse
│   │       ├── itinerary_response.py    # ItineraryResponse, ActivityResponse
│   │       ├── spot_response.py         # SpotResponse
│   │       ├── error_response.py        # ErrorResponse（共通エラー形式）
│   │       └── pagination_response.py   # PaginationResponse（共通ページネーション）
│   │
│   └── exceptions/                      # カスタム例外・ハンドラ
│       ├── __init__.py
│       ├── app_exceptions.py            # ビジネスロジック例外クラス定義
│       └── exception_handlers.py        # FastAPI 例外ハンドラ登録
│
├── tests/                               # テスト
│   ├── __init__.py
│   ├── conftest.py                      # pytest フィクスチャ（テストDB、モックDI）
│   ├── unit/
│   │   ├── usecases/
│   │   │   ├── test_auth_usecase.py
│   │   │   ├── test_trip_usecase.py
│   │   │   ├── test_candidate_spot_usecase.py
│   │   │   └── ...
│   │   └── repositories/
│   │       ├── test_trip_repository.py
│   │       └── ...
│   └── integration/
│       ├── test_auth_router.py
│       ├── test_trips_router.py
│       ├── test_candidates_router.py
│       └── ...
│
├── alembic/                             # DBマイグレーション
│   ├── alembic.ini
│   ├── env.py
│   └── versions/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 4. 各フォルダ詳細

### 4.1 `config/` — 設定・依存注入

| ファイル | 内容 |
|---|---|
| `dependency.py` | FastAPI の `Depends` を使った DI 定義。Repository → Usecase の注入チェーンを構築 |
| `env.py` | `pydantic-settings` による環境変数の型付き読み込み（DB URL、Google Client ID 等） |
| `jwt.py` | JWT の生成（`access_token`, `refresh_token`）とデコード・検証ロジック |

`dependency.py` の設計イメージ:

```python
from fastapi import Depends
from infrastructure.database import get_db
from repositories.trip_repository import TripRepository
from usecases.trip_usecase import TripUsecase
from sqlalchemy.ext.asyncio import AsyncSession


def get_trip_usecase(db: AsyncSession = Depends(get_db)) -> TripUsecase:
    trip_repository = TripRepository(db)
    return TripUsecase(trip_repository)
```

### 4.2 `infrastructure/` — 外部技術依存

| ファイル | 内容 |
|---|---|
| `database.py` | SQLAlchemy AsyncEngine / AsyncSession の生成、`get_db` ジェネレータ |
| `google_oauth.py` | Google の authorization code を検証し、ユーザー情報（sub, email, name, picture）を取得 |
| `google_places.py` | Google Places API への HTTP リクエストラッパー。検索結果を `Spot` 形式に変換 |

### 4.3 `models/` — ドメインモデル

DB設計書 v3.1 の各テーブルに対応する SQLAlchemy ORM モデルを定義します。

| ファイル | 対応テーブル | 主な制約 |
|---|---|---|
| `user.py` | `users` | `google_id` UNIQUE |
| `trip.py` | `trips` | `CHECK (start_date <= end_date)` |
| `trip_member.py` | `trip_members` | 複合PK、`role` CHECK制約 |
| `spot.py` | `spots` | `google_place_id` UNIQUE |
| `candidate_spot.py` | `candidate_spots` | — |
| `candidate_reaction.py` | `candidate_reactions` | `UNIQUE(candidate_spot_id, user_id, emoji_type)` |
| `itinerary_activity.py` | `itinerary_activities` | — |

### 4.4 `repositories/` — データアクセス層

各 Repository は SQLAlchemy Session を受け取り、対応するモデルの CRUD 操作を提供します。Usecase は Repository のメソッドのみを通じてデータにアクセスします。

| ファイル | 主な操作 |
|---|---|
| `user_repository.py` | `find_by_google_id`, `find_by_id`, `create`, `update` |
| `trip_repository.py` | `find_by_id`, `find_by_user`, `create`, `update`, `delete` |
| `trip_member_repository.py` | `find_members`, `add_member`, `update_role`, `remove_member` |
| `spot_repository.py` | `find_by_google_place_id`, `create`, `search_nearby` |
| `candidate_spot_repository.py` | `find_by_trip`, `create`, `update_status`, `delete` |
| `candidate_reaction_repository.py` | `upsert`, `delete`, `count_by_candidate` |
| `itinerary_activity_repository.py` | `find_by_trip_grouped`, `create`, `update`, `delete`, `bulk_update_order` |

### 4.5 `usecases/` — ビジネスロジック層

Usecase はビジネスルールを集約し、Repository を依存注入で受け取ります。Usecase はフレームワーク（FastAPI）に依存しません。

| ファイル | 主な責務 |
|---|---|
| `auth_usecase.py` | Google OAuth code の検証 → ユーザー取得 or 作成 → JWT 発行 / リフレッシュ |
| `user_usecase.py` | プロフィール取得・更新 |
| `trip_usecase.py` | 旅行の作成（invite_code 自動生成）、更新（日付整合性チェック）、削除（カスケード） |
| `trip_member_usecase.py` | 招待コード検証 → 参加、ロール変更（owner 権限チェック）、メンバー除外 |
| `candidate_spot_usecase.py` | 候補追加（spots キャッシュ連携）、ステータス変更、削除 |
| `candidate_reaction_usecase.py` | リアクション登録（UPSERT）、削除 |
| `itinerary_usecase.py` | タイムライン取得（日ごとグルーピング）、追加、更新、並べ替え（sort_order 一括更新） |
| `spot_search_usecase.py` | Google Places 検索 → spots テーブルへのキャッシュ保存 → 結果返却 |

### 4.6 `routers/` — APIエンドポイント

API仕様書 v1.0 のエンドポイントに対応します。Router は Usecase を `Depends` で受け取り、リクエストのバリデーションとレスポンスの返却に専念します。

| ファイル | エンドポイント | 対応API仕様書セクション |
|---|---|---|
| `auth.py` | `POST /auth/google`, `POST /auth/refresh` | 2.2 |
| `users.py` | `GET/PATCH /users/me` | 5.1 |
| `trips.py` | `POST/GET /trips`, `GET/PATCH/DELETE /trips/:tripId` | 5.2 |
| `trip_members.py` | `POST /trips/:tripId/join`, `GET/PATCH/DELETE .../members` | 5.3 |
| `candidates.py` | `POST/GET /trips/:tripId/candidates`, `PATCH/DELETE .../:candidateId` | 5.4 |
| `reactions.py` | `PUT/DELETE .../reactions` | 5.5 |
| `itinerary.py` | `GET/POST .../itinerary`, `PATCH/DELETE .../:activityId`, `PATCH .../reorder` | 5.6 |
| `spots.py` | `GET /spots/search` | 5.7 |

### 4.7 `schemas/` — リクエスト/レスポンス DTO

Pydantic モデルで入出力のバリデーションとシリアライゼーションを行います。`requests/` と `responses/` に分離することで責務を明確にします。

### 4.8 `exceptions/` — カスタム例外

API仕様書のエラーコード一覧（セクション3.2）に対応するカスタム例外クラスを定義します。

```python
# exceptions/app_exceptions.py

class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

class NotFoundException(AppException):
    def __init__(self, message: str = "指定されたリソースが存在しません。"):
        super().__init__("NOT_FOUND", message, 404)

class ForbiddenException(AppException):
    def __init__(self, message: str = "この操作を行う権限がありません。"):
        super().__init__("FORBIDDEN", message, 403)

class ConflictException(AppException):
    def __init__(self, code: str = "CONFLICT", message: str = "リソースが競合しています。"):
        super().__init__(code, message, 409)

class AlreadyMemberException(ConflictException):
    def __init__(self):
        super().__init__("ALREADY_MEMBER", "すでにこの旅行のメンバーです。")

class InvalidDateRangeException(AppException):
    def __init__(self):
        super().__init__("INVALID_DATE_RANGE", "出発日は帰宅日より前である必要があります。", 400)

class InvalidInviteCodeException(AppException):
    def __init__(self):
        super().__init__("INVALID_INVITE_CODE", "招待コードが無効または期限切れです。", 422)
```

`exception_handlers.py` で FastAPI に登録:

```python
# exceptions/exception_handlers.py

from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.app_exceptions import AppException


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )
```

### 4.9 `tests/` — テスト

| ディレクトリ | 内容 |
|---|---|
| `unit/usecases/` | Usecase のユニットテスト。Repository をモックして純粋なロジックを検証 |
| `unit/repositories/` | Repository のユニットテスト。テスト用DBセッションを使用 |
| `integration/` | Router の統合テスト。`TestClient` でエンドポイント全体を検証 |

---

## 5. 依存関係の流れ

```
routers (FastAPI Router)
   │
   │  Depends()
   ▼
usecases (ビジネスロジック)
   │
   │  コンストラクタ注入
   ▼
repositories (データアクセス)
   │
   │  SQLAlchemy Session
   ▼
models (ORMモデル)
   │
   ▼
infrastructure/database.py (DB接続)
```

Router → Usecase → Repository → Model の一方向依存を守ることで、各レイヤーを独立してテスト・差し替えできます。たとえば Repository をモック実装に差し替えるだけで、Usecase のユニットテストが可能です。

---

## 6. ドキュメント間の対応関係

| ドキュメント | 対応するフォルダ |
|---|---|
| DB設計書 v3.1 → テーブル定義 | `models/` の各ファイル |
| DB設計書 v3.1 → 制約（CHECK, UNIQUE） | `models/` のカラム定義 + `repositories/` のバリデーション |
| API仕様書 v1.0 → エンドポイント一覧 | `routers/` の各ファイル |
| API仕様書 v1.0 → リクエスト/レスポンス例 | `schemas/requests/`, `schemas/responses/` |
| API仕様書 v1.0 → エラーコード一覧 | `exceptions/app_exceptions.py` |
| API仕様書 v1.0 → 認証フロー | `config/jwt.py` + `infrastructure/google_oauth.py` + `usecases/auth_usecase.py` |
| OpenAPI YAML v1.0 | `main.py` の FastAPI 自動生成（`/docs`） |
