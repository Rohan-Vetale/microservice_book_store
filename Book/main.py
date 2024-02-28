""
from fastapi import APIRouter, Depends, FastAPI, Request, Response, HTTPException, status
from sqlalchemy.orm import Session
from model import  Books, get_db
from schema import BookSchema

app = FastAPI()

@app.post("/add_book/{user_id}", status_code=status.HTTP_201_CREATED, tags=["Books"])
def add_book(payload: BookSchema, user_id: int, response: Response, db: Session = Depends(get_db)):
    """
    Description: Add a new book.
    Parameter: payload : UserLogin object, response : Response object, db : database session.
    Return: Message of book added with status code 201.
    """
    try:
        # user_id = request.state.user.id
        book_data = payload.model_dump()
        book_data["user_id"] = user_id
        book = Books(**book_data)
        book_exists = db.query(Books).filter_by(book_name = book.book_name, author = book.author).one_or_none()
        if book_exists:
            response.status_code = status.HTTP_200_OK
            return {"message": "This book with same author already exists, use update API instead", "status": 200}
        db.add(book)
        db.commit()
        db.refresh(book)
        return {"message": "Book Added", "status": 201, "data": book}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}

@app.get("/get_all_books/{user_id}", status_code=status.HTTP_200_OK, tags=["Books"])
def read_all_books(user_id: int, response: Response, db: Session = Depends(get_db) ):
    """
    Description: Get all books of the authenticated user.
    Parameter:request: User Request, response : Response object, db : database session.
    Return: List all books details
    """
    try:
        # user_id = request.state.user.id
        books = db.query(Books).filter_by(user_id=user_id).all()
        if not books:
            response.status_code = status.HTTP_404_NOT_FOUND
            return HTTPException(detail="No books found for the user", status_code=status.HTTP_404_NOT_FOUND)
        return {"message": "Data retrieved", "status": 200, "data": books}
    except Exception as e:
        return {"message": str(e)}

@app.get("/get_book/{book_id}", status_code=status.HTTP_200_OK, tags=["Books"])
def read_book(book_id: int, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: Get details of a specific book.
    Parameter: book_id : id of a book, response : Response object, db : database session, request: User Request.
    Return: Details of that one book
    """
    try:
        user_id = request.state.user.id
        book = db.query(Books).filter_by(id=book_id, user_id=user_id).first()
        if not book:
            raise HTTPException(detail="Book not found", status_code=status.HTTP_404_NOT_FOUND)
        return {"message": "Book details retrieved", "status": 200, "data": book}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}

@app.put("/update_book/{book_id}", status_code=status.HTTP_200_OK, tags=["Books"])
def update_book(book_id: int, payload: BookSchema, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: Update details of a specific book.
    Parameter: book_id : id of a book, payload : UserLogin object, response : Response object, db : database session, request: User Request.
    Return: Message of book updated
    """
    try:
        user_id = request.state.user.id
        book = db.query(Books).filter_by(id=book_id, user_id=user_id).first()
        if not book:
            raise HTTPException(detail="Book not found", status_code=status.HTTP_404_NOT_FOUND)
        updated_data = payload.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(book, key, value)
        db.commit()
        db.refresh(book)
        return {"message": "Book updated successfully", "status": 200}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}

@app.delete("/delete_book/{book_id}", status_code=status.HTTP_200_OK, tags=["Books"])
def delete_book(book_id: int, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: Delete a specific book.
    Parameter: book_id : id of a book, response : Response object, db : database session, request: User Request.
    Return: Message of book deleted.
    """
    try:
        user_id = request.state.user.id
        book = db.query(Books).filter_by(id=book_id, user_id=user_id).first()
        if not book:
            raise HTTPException(detail="Book not found", status_code=status.HTTP_404_NOT_FOUND)
        db.delete(book)
        db.commit()
        return {"message": "Book deleted successfully", "status": 200}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}

@app.delete("/delete_all_books", status_code=status.HTTP_200_OK, tags=["Books"])
def delete_all_books(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: Delete all book.
    Parameter: response : Response object, db : database session, request: User Request.
    Return: Message of all books deleted.
    """
    try:
        user_id = request.state.user.id
        books = db.query(Books).filter_by(user_id=user_id).all()
        if not books:
            raise HTTPException(detail="No books found for the user", status_code=status.HTTP_404_NOT_FOUND)
        
        # Delete each book
        for book in books:
            db.delete(book)
        db.commit()
        
        return {"message": "All books deleted successfully", "status": 200}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}
