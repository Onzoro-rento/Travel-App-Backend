# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリで作業する際のガイドラインです。

## プロジェクト概要

旅行予定管理アプリのバックエンド — FastAPI + PostgreSQL による REST API。共同旅行計画のためのリアルタイムなタイムライン同期、候補スポット投票、Google OAuth 認証を提供します。現在は初期段階（main.py にプレースホルダーのルートのみ）で、詳細な設計は `/docs/` に格納されています。

## コマンド

```bash
# Docker ライフサイクル（Makefile 経由）
make build          # Docker イメージをビルド
make up             # FastAPI + PostgreSQL コンテナを起動
make down           # コンテナを停止・削除
make restart        # 再ビルド + 再起動（依存関係変更後に使用）
make logs           # FastAPI コンテナのログを表示
make shell          # FastAPI コンテナにシェルで入る
make db-shell       # PostgreSQL に psql で接続

# コンテナ内
fastapi dev app/main.py --host 0.0.0.0 --port 8000   # ホットリロード付き開発サーバー
```

FastAPI 自動生成ドキュメント: `http://localhost:8000/docs`（Swagger UI）、`/redoc`（ReDoc）

## アーキテクチャ

Clean Architecture に基づく一方向の依存フロー:

```
routers → usecases → repositories → models
   ↓                                    ↓
schemas (Pydantic DTO)          infrastructure/database.py
```

| レイヤー | 配置先 | 責務 |
|----------|--------|------|
| Routers | `app/routers/` | HTTP エンドポイント定義、リクエストバリデーション |
| Schemas | `app/schemas/requests/`, `app/schemas/responses/` | Pydantic によるリクエスト/レスポンス DTO |
| Usecases | `app/usecases/` | ビジネスロジック（FastAPI に依存しない） |
| Repositories | `app/repositories/` | データアクセスの抽象化 |
| Models | `app/models/` | SQLAlchemy ORM エンティティ |
| Infrastructure | `app/infrastructure/` | DB セッション管理、Google OAuth、Google Places API |
| Config | `app/config/` | DI 定義（`dependency.py`）、環境変数（`env.py`）、JWT（`jwt.py`） |
| Exceptions | `app/exceptions/` | カスタム例外クラスと FastAPI 例外ハンドラ |

依存注入: FastAPI `Depends()` → Usecase コンストラクタが Repository を受け取る → Repository が `AsyncSession` を受け取る

## 技術スタック

- **Python 3.14**、**FastAPI 0.113.x**、**Pydantic 2.7+**、**SQLAlchemy 2.0+**（async）
- **PostgreSQL 18**（`psycopg2-binary` 経由）
- **Docker Compose** でローカル開発（サービス: `web`, `db`）
- **JWT**（access + refresh トークン）と **Google OAuth 2.0** による認証

## データベース

7テーブル: `users`, `trips`, `trip_members`, `candidate_spots`, `candidate_reactions`, `spots`（Google Places キャッシュ）, `itinerary_activities`

主要パターン:
- 全テーブルで UUID を主キーに使用
- `trip_members` のロールベースアクセス制御（owner / editor / viewer）
- `itinerary_activities` の辞書式順序 `sort_order` によるドラッグ＆ドロップ並べ替え
- `(candidate_spot_id, user_id, emoji_type)` の複合ユニーク制約で冪等なリアクション
- `trips` からの子エンティティへのカスケード削除
- `spots` テーブルで Google Places データをキャッシュし、重複 API コールを回避

スキーマ詳細: `docs/travel-app-db-design-v3-final.md`

## API 規約

- **成功:** `200`（GET/PATCH）、`201`（POST）、`204`（DELETE）
- **エラー:** `{ "error": { "code": "...", "message": "...", "details": [...] } }`
- **ページネーション:** `{ "data": [...], "pagination": { "page", "per_page", "total_count", "total_pages" } }`
- 認証: `Authorization: Bearer <token>` ヘッダ

API 仕様書: `docs/travel-app-api-spec-v1.md`

## テスト

- ユニットテスト: Usecase（Repository をモック）、Repository（テスト用 DB）
- 統合テスト: Router（HTTP クライアントによるエンドポイント全体テスト）
- 共通フィクスチャは `conftest.py` に定義

## スキル

プロジェクト固有のスキルは `.claude/skills/` に格納されている。対応するレイヤーのコードを生成する前に、必ず該当する SKILL.md を読み込むこと。

| スキル名 | パス | 使用タイミング |
|----------|------|----------------|
| FastAPI エンドポイント生成 | `.claude/skills/fastapi-endpoint-gen/SKILL.md` | Router、Usecase、Repository、Schema など API エンドポイントの実装時。バックエンドのコードを書く前に必ず読む。 |
| DB モデル・マイグレーション生成 | `.claude/skills/db-model-migration-gen/SKILL.md` | SQLAlchemy ORM モデルの作成・変更、Alembic マイグレーションの生成時。モデルやマイグレーションを書く前に必ず読む。 |

各スキルの `references/` フォルダにはプロジェクトの設計書（DB スキーマ、API 仕様書、ディレクトリ構成書）が同梱されており、生成コードの仕様との整合性を担保する。

**利用ルール:**
- エンドポイント実装を依頼されたとき（例: 「旅行の CRUD を作って」）→ まず `fastapi-endpoint-gen/SKILL.md` を読み、Schema → Repository → Usecase → Router の順で生成する。
- モデルやマイグレーション作成を依頼されたとき（例: 「モデルを作って」）→ まず `db-model-migration-gen/SKILL.md` を読み、型マッピングと制約ルールに従って生成する。
- コード生成前に必ず `references/db-design.md` でカラム定義を、`references/api-spec.md` でエンドポイント仕様を確認すること。

## 主要ドキュメント

- `docs/travel-app-directory-structure-v1.md` — アーキテクチャとレイヤーの責務
- `docs/travel-app-db-design-v3-final.md` — データベーススキーマと制約
- `docs/travel-app-api-spec-v1.md` — REST API エンドポイント仕様（24エンドポイント、7リソースカテゴリ）
- `docs/travel-app-openapi-v1.yaml` — OpenAPI 3.0 仕様