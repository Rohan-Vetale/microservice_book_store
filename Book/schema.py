from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
class BookSchema(BaseModel):
    book_name: str = Field(default='Enter book name', title='Enter book name')
    author: str = Field(default='Enter author name', title='Enter author name')
    price: int = Field(default='Enter the price of book', title='Enter the price of book')
    quantity: int = Field(default='Enter the quantity of book', title='Enter the quantity of book')