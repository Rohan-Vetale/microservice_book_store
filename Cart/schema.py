from pydantic import BaseModel


class CartItemsSchema(BaseModel):
    book_id: int
    quantity: int
