from pydantic import BaseModel


class UserRead(BaseModel):
    id: str
    user_name: str
    role: str
    email: str | None
    status: str

