from typing import List
from bson import ObjectId
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typings.users import one, many

from models.user import CreateUser, UpdateUser, User

router = APIRouter()

@router.post("/", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=User)
def create(request: Request, user: CreateUser = Body(...)):
    user = jsonable_encoder(user)
    new_user = request.app.database["users"].insert_one(dict(user))
    created = request.app.database["users"].find_one(
        {"_id": new_user.inserted_id}
    )
    return created

@router.get("/", response_description="Find users", response_model=List[User])
async def find_many(request: Request):
    users = many(request.app.database["users"].find(limit=100))
    return users

@router.get("/{id}", response_description="Find user", response_model=User)
def find_one(id: str, request: Request):
    if (user := one(request.app.database["users"].find_one({"_id": ObjectId(id)}))) is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")

@router.patch("/{id}", response_description="Update a user", response_model=User)
def update(id: str, request: Request, user: UpdateUser = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        update_result = request.app.database["users"].update_one(
            {"_id": ObjectId(id)}, {"$set": dict(user)}
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
    if (
        existing := request.app.database["users"].find_one({"_id": ObjectId(id)})
    ) is not None:
        return existing
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")

@router.delete("/{id}", response_description="Delete a user")
def remove(id: str, request: Request, response: Response):
    result = request.app.database["users"].delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")