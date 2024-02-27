from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr



class UserDetails(BaseModel):
    user_name: str = Field(default='Enter user name', title='Enter User name')
    password: str = Field(default='Enter user password', title='Enter User password', min_length=8)
    email: EmailStr = Field(default='Enter email id', title='Enter your email')
    first_name: str = Field(default='Enter First Name', title='Enter First Name', pattern=r"^[A-Z]{1}\D{3,}$")
    last_name: str = Field(default='Enter Last Name', title='Enter Last Name', pattern=r"^[A-Z]{1}\D{3,}$")
    state: str = Field(default='Enter your state Name', title='Enter your state Name')
    phone: int = Field(default='Enter phone number', title='Enter phone number')
    is_verified: Optional[bool] = Field(default=False)
    super_key: Optional[str] = None
    
class Userlogin(BaseModel):
    user_name: str = Field(default='Enter user name', title='Enter User name')
    password: str = Field(default='Enter user password', title='Enter User password')