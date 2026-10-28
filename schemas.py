from pydantic import BaseModel, ConfigDict, EmailStr, Field


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteOut(NoteCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str