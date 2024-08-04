import uuid
from fastapi import Body, Query
from pydantic import BaseModel
from typing import Annotated, Optional, Required, Union
from pydantic import BaseModel, Field
from datetime import datetime, date


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="id")
    createdAt: str | datetime = Field(...)
    updatedAt: str | datetime = Field(...)
    active: bool = Field(...)
    role: Union[str, None] = Field(default=str | None)
    image: Union[str, None] = Field(default=str | None)
    email: Union[str, None] = Field(default=str | None)
    phone: str = Field(...)
    account: Union[str, None] = Field(default=str | None)

class CreateUser(BaseModel):
    createdAt: Annotated[datetime, Body(default=datetime.now())]
    updatedAt: Annotated[datetime, Body(default=datetime.now())]
    active: Annotated[bool, Query(default=True), Optional]
    role: Annotated[str | None, Query(default=None), Optional]
    image: Annotated[str | None, Query(default=None), Optional]
    email: Annotated[str | None, Query(default=None), Optional]
    phone: Annotated[str, Query(), Required]
    secret: Annotated[str | None, Query(default=None), Optional]
    account: Annotated[str | None, Query(default=None), Optional]

class UpdateUser(BaseModel):
    updatedAt: Annotated[datetime, Body(default=datetime.now())]
    active: Annotated[bool, Body()] = True
    role: Annotated[str | None, Body()] = None
    image: Annotated[str | None, Body()] = None
    email: Annotated[str | None, Body()] = None
    phone: Annotated[str | None, Body()] = None
    secret: Annotated[str | None, Body()] = None
    account: Annotated[str | None, Body()] = None
