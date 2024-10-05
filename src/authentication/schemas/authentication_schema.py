from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None


class AuthUser(BaseModel):
    id: int
    email: str
    token: Token
