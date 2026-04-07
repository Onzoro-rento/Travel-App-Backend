from contextlib import asynccontextmanager
from app.infrastructure.database import init_db,engine
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ① 【起動時】お店を開ける前の準備（yield の前）
    print("アプリケーションの起動処理を開始...")
    await init_db()  # ← DBのテーブルを作成したり、接続の準備をする

    yield  # ② 【営業中】ここでAPIサーバーが立ち上がり、ユーザーからのアクセスを受け付け始める！
    
    # ③ 【終了時】サーバーを停止したときの片付け（yield の後）
    print("シャットダウンします。DBの接続を閉じます...")
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
