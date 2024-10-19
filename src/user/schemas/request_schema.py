from pydantic import BaseModel, EmailStr, Field


class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)
