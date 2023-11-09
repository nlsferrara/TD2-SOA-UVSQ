from fastapi import FastAPI
import random
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: Optional[int] = None
    gender: str
    phone: Optional[str] = None


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# http://127.0.0.1:8000/user/Quentin
@app.get("/user/{name}")
async def read_name(name: str):
    return {"message": f"Hello, {name}"}


@app.get("/user-name/")
async def create_user(user: User):
    return user


# http://127.0.0.1:8000/user/?start=1&end=10
@app.get("/user/")
async def create_user_id(start: int, end: int):
    return {"user id": random.randint(start, end)}

@app.get("/user/id/{iid}")
async def read_name(iid: int):
    return {"user id": iid}