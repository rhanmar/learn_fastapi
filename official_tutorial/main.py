from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Query
from enum import Enum
from datetime import datetime


app = FastAPI()


SOME_DATA = list(range(10))


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


class Point(BaseModel):
    name: str
    coordinates: str
    created_at: Optional[datetime] = datetime.now()
    # rate: str | None = None


class Status(str, Enum):
    error = "error"
    sent = "sent"
    scheduled = "scheduled"
    draft = "draft"
    in_progress = "in progress"


@app.post("/body/{item_pk}")
def test_body_with_many_params(
        point: Point,
        item_pk: int,
        is_valid: bool,
        q: Optional[str] = Query(..., max_length=4, min_length=3, regex="^_"),
):
    return (
        point.name,
        point.coordinates,
        point.created_at,
        point.rate,
        q,
    )


@app.post("/body/")
def test_body(point: Point):
    print(point.dict())
    print(point.__dict__)
    return (
        point.name,
        point.coordinates,
        point.created_at,
        point.rate,
    )


# @app.get("/data/")
# def get_some_data_slice(q: Optional[str] = None, start: int = 0, offset: int = 10, z: str | None = None):
#     # return SOME_DATA[start:start + offset]
#     return {"q": q, "data": SOME_DATA, "skip": start, "offset": offset, "z": z}


@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/statuses")
def get_statuses():
    return list(Status)


@app.get("/test/{test_param}")
def test_default_path_params(test_param: Optional[int] = None):  # NOT WORKING
    return test_param


@app.get("/status/{status_name}")
async def get_status(status_name: Optional[Status]):
    if status_name.value == "sent":
        return "ITS SENT!"
    if status_name == Status.error:
        return "Error :("
    if status_name.value == Status.draft.value:
        return "draaaaft...."
    return {"status_name": status_name, "extra": "--__--"}


@app.get("/")
def read_root():
    return {"Hello": "GET"}


@app.post("/")
def create_root():
    return {"Hello": "POST"}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, q: Optional[str] = None):
    return {
        "item_name": item.name,
        "item_price": item.price,
        "item_is_offer": item.is_offer,
        "item_id": item_id,
        "test": 123
    }


@app.get("/items/{item_id}")
def read_item(q: Optional[str], item_id: int):
    return {"item_id": item_id, "q": q}


@app.get("/items")
def read_items(www=None, q: Optional[int] = None, number: int =100):
    # return [www, q]
    return {
        "www": www,
        "q": q,
        "number": number
    }
