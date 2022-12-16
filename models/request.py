from pydantic import BaseModel, Field, EmailStr

class List(BaseModel):
    title: str = Field(None, title="Task Name")
    complete: bool = Field(False , title= "If the Task is complete or Not")


class UserRequest(BaseModel):
    fullname: str = Field(None, title="User Name")
    email: EmailStr = Field(None , title="User Email")
    password: str = Field(None,title="User Password")


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(None, title="User Email")
    password: str = Field(None,title="User Password")

