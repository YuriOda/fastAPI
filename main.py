from fastapi import FastAPI
from enum import Enum
from typing import Union

# fastAPIのインスタンス化
app = FastAPI()

# mainのURLにアクセスがあったら、下記の関数を処理する
# @はdecorator
@app.get("/") 
async def root():
    return {"message": "Hello World"}

@app.get("/user/me")
async def user_me():
    return {"user_id": "current user"}

@app.get("/user/{user_id}")
# {}で囲むと引数として設定できる
async def user_id(user_id: int):
    return {"user_id": user_id}

class ModelName(str, Enum):
    alexnet = "kiki"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
# model_nameはModelNameで設定された値以外を受け取らない
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning!"}
    
    if model_name is ModelName.lenet:
        return {"model_name": model_name, "message": "AAAA!"}
    
    # resnetがはいってきた時のレスポンス
    return {"model_name": model_name, "message": "other"}

# http://127.0.0.1:8000/files/items/?skip=0&limit=10
# 上記をリクエストすると、file_path: "items/" が返ってきた
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# クエリを設定する方法
# パスパラではない関数パラメータを宣言すると、自動的にクエリとして解釈される
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# Unionは複数の型をもつことができ、ここではstring or None(デフォルト)
# queryの2個目の引数はクエリを指す
@app.get("/query/{item_id}")
# strをintにしてstrを入力すると422 Unprocessable Entityが発生する
# ❌ http://127.0.0.1:8000/query/aaa?q=aa
# ⭕️ http://127.0.0.1:8000/query/aaa?q=1
async def query(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@app.get("/query2/{item_id}")
# Noneがあるとoptionalだとわかる
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    # shortがfalseだった場合に返す値
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    # 入力されたクエリがbool以外の場合はエラーを返す
    # case insensitive
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    # qがある場合はqを追加
    if q:
        item.update({"q": q})
    # falseの場合は下記のdescriptionを追加する
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# needyにデフォルト値がないので、needyをクエリとして設定しないとエラーが発生する
@app.get("/query-items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}

    return item

# Request Body ----------------------------------------------------
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.post("/items/")
async def create_item(item: Item):
    new = {"name": item.name, "price": item.price}
    if item.description is None or item.description == "":
        new.update({"description": "no description"})
    if item.description:
        new.update({"description": "aaaaa"})
    return new

# .dict()でitemが持つ値にアクセスすることができる
@app.post("/cart/")
async def add_cart(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Query Param ----------------------------------------------------
from fastapi import FastAPI, Query

# クエリに最短・最長の長さを指定することができる
# min_length, max_length
@app.get("/new-items/")
async def read_items(q: Union[str, None] = Query(default=None, min_length=3, max_length=5)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# default=Noneをとってあげるだけ
@app.get("/query-required/")
async def read_items(q: str = Query(min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

