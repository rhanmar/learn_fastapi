from typing import List
from fastapi import FastAPI, HTTPException, status
from models import User, Gender, Role

app = FastAPI()

# from fastapi.middleware.cors import CORSMiddleware
# origins = ["*"]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


db: List[User] = [
    User(
        id=1,
        first_name="Dmitriy",
        last_name="Ov",
        gender=Gender.male,
        roles=[Role.admin, Role.user],
    ),
    User(
        id=2,
        first_name="Ekaterina",
        middle_name="Igor",
        last_name="Tk",
        gender=Gender.female,
        roles=[Role.user, Role.student],
    ),
    User(
        id=3,
        first_name="Aristotle",
        middle_name="Ἀριστοτέλης",
        last_name="Greek",
        gender=Gender.male,
        roles=[Role.admin],
    ),
    User(
        id=4,
        first_name="Bad",
        middle_name="Guy",
        last_name="Removable",
        gender=Gender.male,
        roles=[Role.user],
    )
]


@app.get('/')
def get_hello():
    return {"Hello!": "Dima"}


@app.get('/api/users/')
async def get_users() -> List:
    return db


@app.get("/api/users/{user_id}")
async def get_user(user_id: int) -> User:
    return list(
        filter(
            lambda x: x.id == user_id,
            db
        )
    )[0]


@app.post("/api/users/")
async def create_user(user: User):
    db.append(user)
    return {
        "id": user.id,
        "status_code": 200,
    }


@app.delete("/api/users/{user_id}", status_code=status.HTTP_201_CREATED)
async def delete_user(user_id: int):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user with id {user_id} does not exist."
    )
