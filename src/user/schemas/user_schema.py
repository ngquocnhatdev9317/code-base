from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    is_superuser: bool

    class Config:
        from_attributes = True
