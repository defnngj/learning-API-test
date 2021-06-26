"""
auth: bugmaster
data: 2021-06-26
"""
from enum import Enum
from typing import Optional
from fastapi import FastAPI
from fastapi import Form
from fastapi import File, UploadFile
from fastapi import Cookie, Header
from pydantic import BaseModel

app = FastAPI()


ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', "json"]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        return {"item_id": item_id, "q": q}
    if not short:
        item.update({
            "description": "This is an amazing item that has a long description"
        })
    return item


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None  # 可选参数


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}


fake_items_db = [
    {"item_name": "apple"}, 
    {"item_name": "banana"}, 
    {"item_name": "orange"},
    {"item_name": "watermelon"},
    {"item_name": "grape"}
]


@app.get("/items/")
def read_item(start: int = 0, length: int = 10):
    return fake_items_db[start : start + length]


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


class Commodity(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.post("/commodity/")
async def create_commodity(commodity: Commodity):
    commodity_dict = commodity.dict()
    if commodity.tax:
        price_with_tax = commodity.price + commodity.tax
        commodity_dict.update({"price_with_tax": price_with_tax})
    return commodity_dict


# from-data 参数
@app.post("/login/")
async def login(*, username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}


# 文件后缀名的判断
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 文件上传
@app.post("/files/")
async def create_file(file: UploadFile = File(...)):
    if file and allowed_file(file.filename):
        contents = await file.read()
        with open("./upload/"+file.filename, "wb") as f:
            f.write(contents)
        return {"success": True, "filename": file.filename}
    else:
        return {"success": False, "message": "file type nonsupport"}


# Cookie
@app.get("/cookies/")
async def read_cookie(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}


# Header
@app.get("/headers/")
async def read_headers(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}


