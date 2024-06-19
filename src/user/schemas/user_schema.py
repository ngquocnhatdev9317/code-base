from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str
    is_superuser: bool

    class Config:
        from_attributes = True
