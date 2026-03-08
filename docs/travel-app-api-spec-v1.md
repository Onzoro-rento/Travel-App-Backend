# 旅行予定管理アプリ REST API 仕様書

> **Version:** 1.0
> **最終更新日:** 2026-03-08
> **ベースURL:** `https://api.example.com/v1`
> **対応DB設計書:** v3.1

---

## 1. 概要

旅行予定管理アプリのバックエンド REST API 仕様です。Google OAuth によるユーザー認証、旅行プロジェクトの CRUD、候補スポットの投票、タイムライン管理などの機能を提供します。

### 共通仕様

| 項目 | 内容 |
|---|---|
| プロトコル | HTTPS |
| データ形式 | JSON（`Content-Type: application/json`） |
| 文字コード | UTF-8 |
| 日時形式 | ISO 8601（`2026-03-08T09:00:00+09:00`） |
| ID形式 | UUID v4 |
| 認証方式 | Bearer Token（JWT） |

---

## 2. 認証・認可

### 2.1 認証フロー（Google OAuth 2.0）

```
┌────────┐     ┌────────────┐     ┌──────────┐     ┌────────┐
│ Client │────▶│ Google     │────▶│ Google   │────▶│  API   │
│  App   │     │ OAuth画面  │     │ (token)  │     │ Server │
└────────┘     └────────────┘     └──────────┘     └────────┘
    │                                                   │
    │  1. Googleログイン画面へリダイレクト                │
    │  2. ユーザーが認可                                 │
    │  3. authorization_code を取得                      │
    │  4. POST /auth/google に code を送信 ──────────────▶│
    │                                                   │
    │  5. サーバーが Google に code を検証                │
    │  6. ユーザー作成 or 取得                            │
    │  7. JWT (access_token + refresh_token) を返却 ◀────│
    │                                                   │
    │  8. 以降のリクエストに Authorization ヘッダ付与     │
    └───────────────────────────────────────────────────┘
```

### 2.2 認証エンドポイント

#### `POST /auth/google`

Google から取得した authorization code をサーバーに送信し、JWT を取得します。

**リクエスト:**

```json
{
  "code": "4/0AX4XfWh..."
}
```

**レスポンス: `200 OK`**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "dGhpcyBpcyBhIHJlZnJl...",
  "expires_in": 3600,
  "token_type": "Bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "田中 太郎",
    "email": "tanaka@example.com",
    "avatar_url": "https://lh3.googleusercontent.com/..."
  }
}
```

#### `POST /auth/refresh`

期限切れの access_token を再発行します。

**リクエスト:**

```json
{
  "refresh_token": "dGhpcyBpcyBhIHJlZnJl..."
}
```

**レスポンス: `200 OK`**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

### 2.3 認証ヘッダ

認証が必要なすべてのエンドポイントには、以下のヘッダを付与します。

```
Authorization: Bearer <access_token>
```

### 2.4 認可（ロールベース）

旅行リソースへのアクセスは `trip_members.role` に基づいて制御されます。

| 操作 | `owner` | `editor` | `viewer` |
|---|---|---|---|
| 旅行情報の閲覧 | ✅ | ✅ | ✅ |
| 旅行情報の編集 | ✅ | ✅ | ❌ |
| 旅行の削除 | ✅ | ❌ | ❌ |
| メンバーの招待・削除 | ✅ | ❌ | ❌ |
| 候補スポットの追加 | ✅ | ✅ | ❌ |
| リアクションの投稿 | ✅ | ✅ | ✅ |
| タイムラインの編集 | ✅ | ✅ | ❌ |

---

## 3. エラーレスポンス定義

### 3.1 共通エラーフォーマット

すべてのエラーレスポンスは以下の形式で返却されます。

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "リクエストの入力値が不正です。",
    "details": [
      {
        "field": "title",
        "reason": "必須項目です。"
      }
    ]
  }
}
```

### 3.2 エラーコード一覧

| HTTPステータス | エラーコード | 説明 |
|---|---|---|
| 400 | `VALIDATION_ERROR` | リクエストパラメータの形式・値が不正 |
| 400 | `INVALID_DATE_RANGE` | `start_date` が `end_date` より後 |
| 401 | `UNAUTHORIZED` | 認証トークンが未提供または無効 |
| 401 | `TOKEN_EXPIRED` | access_token の有効期限切れ |
| 403 | `FORBIDDEN` | リソースに対する権限が不足 |
| 404 | `NOT_FOUND` | 指定されたリソースが存在しない |
| 409 | `CONFLICT` | 一意制約の違反（招待コード重複、リアクション重複など） |
| 409 | `ALREADY_MEMBER` | すでに旅行メンバーとして登録済み |
| 422 | `INVALID_INVITE_CODE` | 招待コードが無効または期限切れ |
| 429 | `RATE_LIMITED` | リクエスト回数の上限超過 |
| 500 | `INTERNAL_ERROR` | サーバー内部エラー |

---

## 4. エンドポイント一覧

| # | メソッド | パス | 説明 | 認証 |
|---|---|---|---|---|
| 1 | POST | `/auth/google` | Google OAuth ログイン | 不要 |
| 2 | POST | `/auth/refresh` | トークンリフレッシュ | 不要 |
| 3 | GET | `/users/me` | 自分のプロフィール取得 | 必要 |
| 4 | PATCH | `/users/me` | 自分のプロフィール更新 | 必要 |
| 5 | POST | `/trips` | 旅行作成 | 必要 |
| 6 | GET | `/trips` | 参加中の旅行一覧取得 | 必要 |
| 7 | GET | `/trips/:tripId` | 旅行詳細取得 | 必要 |
| 8 | PATCH | `/trips/:tripId` | 旅行情報更新 | 必要 |
| 9 | DELETE | `/trips/:tripId` | 旅行削除 | 必要 |
| 10 | POST | `/trips/:tripId/join` | 招待コードで旅行に参加 | 必要 |
| 11 | GET | `/trips/:tripId/members` | メンバー一覧取得 | 必要 |
| 12 | PATCH | `/trips/:tripId/members/:userId` | メンバーのロール変更 | 必要 |
| 13 | DELETE | `/trips/:tripId/members/:userId` | メンバー削除 | 必要 |
| 14 | POST | `/trips/:tripId/candidates` | 候補スポット追加 | 必要 |
| 15 | GET | `/trips/:tripId/candidates` | 候補スポット一覧取得 | 必要 |
| 16 | PATCH | `/trips/:tripId/candidates/:candidateId` | 候補スポットのステータス変更 | 必要 |
| 17 | DELETE | `/trips/:tripId/candidates/:candidateId` | 候補スポット削除 | 必要 |
| 18 | PUT | `/trips/:tripId/candidates/:candidateId/reactions` | リアクション登録・更新 | 必要 |
| 19 | DELETE | `/trips/:tripId/candidates/:candidateId/reactions` | リアクション削除 | 必要 |
| 20 | GET | `/trips/:tripId/itinerary` | タイムライン取得 | 必要 |
| 21 | POST | `/trips/:tripId/itinerary` | アクティビティ追加 | 必要 |
| 22 | PATCH | `/trips/:tripId/itinerary/:activityId` | アクティビティ更新 | 必要 |
| 23 | DELETE | `/trips/:tripId/itinerary/:activityId` | アクティビティ削除 | 必要 |
| 24 | GET | `/spots/search` | Google Places スポット検索 | 必要 |

---

## 5. エンドポイント詳細

### 5.1 ユーザー

#### `GET /users/me`

ログイン中のユーザー情報を取得します。

**レスポンス: `200 OK`**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "田中 太郎",
  "email": "tanaka@example.com",
  "avatar_url": "https://lh3.googleusercontent.com/...",
  "created_at": "2026-01-15T10:00:00+09:00"
}
```

#### `PATCH /users/me`

表示名やアバターURLを更新します。

**リクエスト:**

```json
{
  "name": "たなか"
}
```

**レスポンス: `200 OK`**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "たなか",
  "email": "tanaka@example.com",
  "avatar_url": "https://lh3.googleusercontent.com/...",
  "updated_at": "2026-03-08T12:00:00+09:00"
}
```

---

### 5.2 旅行プロジェクト

#### `POST /trips`

新しい旅行を作成します。作成者は自動的に `owner` ロールで登録されます。

**リクエスト:**

```json
{
  "title": "沖縄旅行 2026夏",
  "cover_photo_url": "https://storage.example.com/covers/okinawa.jpg",
  "start_date": "2026-07-20",
  "end_date": "2026-07-23"
}
```

**レスポンス: `201 Created`**

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "沖縄旅行 2026夏",
  "cover_photo_url": "https://storage.example.com/covers/okinawa.jpg",
  "start_date": "2026-07-20",
  "end_date": "2026-07-23",
  "invite_code": "ABC123XYZ",
  "created_at": "2026-03-08T10:00:00+09:00"
}
```

#### `GET /trips`

自分が参加中の旅行一覧を取得します。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|---|---|---|---|
| `page` | integer | | ページ番号（デフォルト: 1） |
| `per_page` | integer | | 1ページあたりの件数（デフォルト: 20, 最大: 50） |

**レスポンス: `200 OK`**

```json
{
  "data": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "title": "沖縄旅行 2026夏",
      "cover_photo_url": "https://storage.example.com/covers/okinawa.jpg",
      "start_date": "2026-07-20",
      "end_date": "2026-07-23",
      "my_role": "owner",
      "member_count": 4
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_count": 3,
    "total_pages": 1
  }
}
```

#### `GET /trips/:tripId`

旅行の詳細を取得します。メンバー一覧もネストして返却します。

**レスポンス: `200 OK`**

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "沖縄旅行 2026夏",
  "cover_photo_url": "https://storage.example.com/covers/okinawa.jpg",
  "start_date": "2026-07-20",
  "end_date": "2026-07-23",
  "invite_code": "ABC123XYZ",
  "members": [
    {
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "田中 太郎",
      "avatar_url": "https://lh3.googleusercontent.com/...",
      "role": "owner"
    },
    {
      "user_id": "660f9500-f30c-52e5-b827-557766550000",
      "name": "鈴木 花子",
      "avatar_url": "https://lh3.googleusercontent.com/...",
      "role": "editor"
    }
  ],
  "created_at": "2026-03-08T10:00:00+09:00",
  "updated_at": "2026-03-08T10:00:00+09:00"
}
```

#### `PATCH /trips/:tripId`

旅行情報を部分更新します。**必要ロール:** `owner` または `editor`

**リクエスト:**

```json
{
  "title": "沖縄旅行 2026夏（確定版）",
  "end_date": "2026-07-24"
}
```

**レスポンス: `200 OK`** — 更新後の旅行オブジェクトを返却

#### `DELETE /trips/:tripId`

旅行を削除します。関連する候補・リアクション・タイムラインもすべて削除されます。**必要ロール:** `owner`

**レスポンス: `204 No Content`**

---

### 5.3 メンバー管理

#### `POST /trips/:tripId/join`

招待コードを使って旅行に参加します。デフォルトロールは `editor` です。

**リクエスト:**

```json
{
  "invite_code": "ABC123XYZ"
}
```

**レスポンス: `201 Created`**

```json
{
  "trip_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "user_id": "770a0600-a41d-63f6-c938-668877660000",
  "role": "editor",
  "created_at": "2026-03-08T15:00:00+09:00"
}
```

**エラー例: `409 Conflict`**

```json
{
  "error": {
    "code": "ALREADY_MEMBER",
    "message": "すでにこの旅行のメンバーです。"
  }
}
```

#### `PATCH /trips/:tripId/members/:userId`

メンバーのロールを変更します。**必要ロール:** `owner`

**リクエスト:**

```json
{
  "role": "viewer"
}
```

**レスポンス: `200 OK`** — 更新後のメンバーオブジェクトを返却

#### `DELETE /trips/:tripId/members/:userId`

メンバーを旅行から除外します。**必要ロール:** `owner`（自分自身は削除不可）

**レスポンス: `204 No Content`**

---

### 5.4 候補スポット

#### `POST /trips/:tripId/candidates`

候補プールにスポットを追加します。`google_place_id` を指定すると、`spots` テーブルにキャッシュがなければ Google Places API から情報を取得して自動登録します。**必要ロール:** `owner` または `editor`

**リクエスト:**

```json
{
  "google_place_id": "ChIJ37wEMbOLGGARQm2asMVzHSE"
}
```

**レスポンス: `201 Created`**

```json
{
  "id": "cand-1111-2222-3333-444455556666",
  "trip_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "spot": {
    "id": "spot-aaaa-bbbb-cccc-ddddeeeeeeee",
    "google_place_id": "ChIJ37wEMbOLGGARQm2asMVzHSE",
    "name": "美ら海水族館",
    "address": "沖縄県国頭郡本部町字石川424番地",
    "latitude": 26.6944,
    "longitude": 127.8779
  },
  "added_by": "550e8400-e29b-41d4-a716-446655440000",
  "status": "in_pool",
  "reactions_summary": {},
  "created_at": "2026-03-08T11:00:00+09:00"
}
```

#### `GET /trips/:tripId/candidates`

候補スポット一覧をリアクション集計付きで取得します。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|---|---|---|---|
| `status` | string | | `in_pool` / `in_timeline` でフィルタ |

**レスポンス: `200 OK`**

```json
{
  "data": [
    {
      "id": "cand-1111-2222-3333-444455556666",
      "spot": {
        "id": "spot-aaaa-bbbb-cccc-ddddeeeeeeee",
        "name": "美ら海水族館",
        "latitude": 26.6944,
        "longitude": 127.8779
      },
      "added_by": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "田中 太郎"
      },
      "status": "in_pool",
      "reactions_summary": {
        "👍": 3,
        "😍": 1
      },
      "my_reaction": "👍",
      "created_at": "2026-03-08T11:00:00+09:00"
    }
  ]
}
```

#### `PATCH /trips/:tripId/candidates/:candidateId`

候補のステータスを変更します（例: プールからタイムラインへ移動）。**必要ロール:** `owner` または `editor`

**リクエスト:**

```json
{
  "status": "in_timeline"
}
```

**レスポンス: `200 OK`** — 更新後の候補オブジェクトを返却

#### `DELETE /trips/:tripId/candidates/:candidateId`

候補スポットを削除します。関連するリアクションも削除されます。**必要ロール:** `owner` または `editor`

**レスポンス: `204 No Content`**

---

### 5.5 リアクション

#### `PUT /trips/:tripId/candidates/:candidateId/reactions`

候補に対してリアクション（絵文字）を登録します。同じ `emoji_type` が既に存在する場合は上書き（冪等）。**必要ロール:** すべてのメンバー

**リクエスト:**

```json
{
  "emoji_type": "👍"
}
```

**レスポンス: `200 OK`**

```json
{
  "id": "react-1111-2222-3333-444455556666",
  "candidate_spot_id": "cand-1111-2222-3333-444455556666",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "emoji_type": "👍",
  "created_at": "2026-03-08T12:00:00+09:00"
}
```

#### `DELETE /trips/:tripId/candidates/:candidateId/reactions`

自分のリアクションを削除します。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|---|---|---|---|
| `emoji_type` | string | ✅ | 削除する絵文字（例: `👍`） |

**レスポンス: `204 No Content`**

---

### 5.6 タイムライン

#### `GET /trips/:tripId/itinerary`

タイムラインのアクティビティを日ごとにグルーピングして取得します。

**レスポンス: `200 OK`**

```json
{
  "trip_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "days": [
    {
      "day_number": 1,
      "date": "2026-07-20",
      "activities": [
        {
          "id": "act-1111-2222-3333-444455556666",
          "sort_order": "aaa",
          "spot": {
            "id": "spot-aaaa-bbbb-cccc-ddddeeeeeeee",
            "name": "美ら海水族館",
            "latitude": 26.6944,
            "longitude": 127.8779
          },
          "start_time": "2026-07-20T10:00:00+09:00",
          "memo": "開園直後がおすすめ",
          "created_at": "2026-03-08T13:00:00+09:00"
        }
      ]
    }
  ]
}
```

#### `POST /trips/:tripId/itinerary`

タイムラインにアクティビティを追加します。**必要ロール:** `owner` または `editor`

**リクエスト:**

```json
{
  "day_number": 1,
  "spot_id": "spot-aaaa-bbbb-cccc-ddddeeeeeeee",
  "sort_order": "aab",
  "start_time": "2026-07-20T12:00:00+09:00",
  "memo": "ランチ予約済み"
}
```

**レスポンス: `201 Created`** — 作成されたアクティビティオブジェクトを返却

#### `PATCH /trips/:tripId/itinerary/:activityId`

アクティビティの情報を部分更新します。**必要ロール:** `owner` または `editor`

**リクエスト:**

```json
{
  "start_time": "2026-07-20T13:00:00+09:00",
  "memo": "ランチ予約時間変更"
}
```

**レスポンス: `200 OK`** — 更新後のアクティビティオブジェクトを返却

#### `DELETE /trips/:tripId/itinerary/:activityId`

アクティビティを削除します。**必要ロール:** `owner` または `editor`

**レスポンス: `204 No Content`**


---

### 5.7 スポット検索

#### `GET /spots/search`

Google Places API を使ったスポット検索のプロキシです。結果は `spots` テーブルにキャッシュされます。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|---|---|---|---|
| `query` | string | ✅ | 検索キーワード（例: `沖縄 カフェ`） |
| `latitude` | number | | 検索の中心緯度 |
| `longitude` | number | | 検索の中心経度 |
| `radius` | integer | | 検索半径（メートル, デフォルト: 5000） |

**レスポンス: `200 OK`**

```json
{
  "data": [
    {
      "id": "spot-bbbb-cccc-dddd-eeeeffff0000",
      "google_place_id": "ChIJxxxxxxxxxxxxxxxxxxxxxx",
      "name": "浜辺の茶屋",
      "address": "沖縄県南城市玉城字玉城2-1",
      "latitude": 26.1511,
      "longitude": 127.7786
    }
  ]
}
```
