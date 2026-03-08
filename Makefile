-include .env

.PHONY: build up down logs shell db-shell restart

# イメージのビルド
build:
	docker compose build

# アプリとDBの起動
up:
	docker compose up -d

# アプリとDBの停止・削除
down:
	docker compose down

# FastAPI側のログ監視
logs:
	docker compose logs -f web

# FastAPIコンテナに入る
shell:
	docker compose exec web bash

# ★追加：PostgreSQLのデータベースの中に直接入ってSQLを叩く
db-shell:
	docker compose exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

# 再起動（パッケージ追加時などに使用）
restart: down build up