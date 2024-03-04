"""
@Author: Rohan Vetale

@Date: 2024-03-03 11:30:00

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-03-04 11:30:00

@Title :  Book microservice of book store
"""
from fastapi import FastAPI, Security, status, Response, Depends, Path, HTTPException, Request
from Book.schema import BookSchema
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, Request, Response, HTTPException, status
from sqlalchemy.orm import Session
from model import  Books, get_db
from schema import BookSchema
import requests as rq
from utils import jwt_authentication
app = FastAPI(title='Book Store ',dependencies=[Security(APIKeyHeader(name='authorization')),Depends(jwt_authentication)])

@app.post("/add_book", status_code=status.HTTP_201_CREATED, tags=["Books"])
def add_book(request: Request, payload: BookSchema, response: Response, db: Session = Depends(get_db)):
    """
    Description: Add a new book.
    Parameter: payload : UserLogin object, response : Response object, db : database session.
    Return: Message of book added with status code 201.
    """
    try:
        user_data = request.state.user
        if not user_data['is_super_user']:
            raise HTTPException(detail="You are not SuperUser", status_code=status.HTTP_400_BAD_REQUEST)
        if not user_data['is_verified']:
            raise HTTPException(detail='You are not verified user', status_code=status.HTTP_400_BAD_REQUEST)
        book_data = payload.model_dump()
        book_data.update({'user_id': user_data['id']})
        book_data = Books(**book_data)
        db.add(book_data)
        db.commit()
        db.refresh(book_data)
        return {"message": "Book Added", "status": 201, "data": book_data}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}

@app.get("/get_all_books/{user_id}", status_code=status.HTTP_200_OK, tags=["Books"])
def read_all_books(request: Request, response: Response, db: Session = Depends(get_db) ):
    """
    Description: Get all books of the authenticated user.
    Parameter:request: User Request, response : Response object, db : database session.
    Return: List all books details
    """
    try:
        user_data = request.state.user
        user_id = user_data['id']
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
        user_data = request.state.user
        user_id = user_data['id']
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
        user_data = request.state.user
        user_id = user_data['id']
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
        user_data = request.state.user
        user_id = user_data['id']
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
        user_data = request.state.user
        user_id = user_data['id']
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
