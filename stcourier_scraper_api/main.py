from typing import Optional

from fastapi import FastAPI

from stcourier_firefox_selenium import track

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/track")
def read_item(q: Optional[str] = None):

    response=track(q)

    return  response