from fastapi import FastAPI
from enum import Enum

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
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning!"}
    
    if model_name is ModelName.lenet:
        return {"model_name": model_name, "message": "AAAA!"}
