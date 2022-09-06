from pydantic import BaseModel


class ItemBase(BaseModel):  # BASE Item
    title: str
    description: str | None = None


class ItemCreate(ItemBase):  # CREATE Item
    pass


class Item(ItemBase):  # READ Item
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):  # BASE User
    email: str


class UserCreate(UserBase):  # CREATE User
    password: str


class User(UserBase):  # READ User
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
