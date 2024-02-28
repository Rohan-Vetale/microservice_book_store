from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import BigInteger, Boolean, Column, String, create_engine
from settings import DATABASE_DIALECT, DATABASE_DRIVER, BOOK_DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USERNAME, DEFAULT_PORT, HOST

database_url = f"{DATABASE_DIALECT}+{DATABASE_DRIVER}://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{HOST}:{DEFAULT_PORT}/{BOOK_DATABASE_NAME}"
engine = create_engine(database_url)
session = Session(engine)
Base = declarative_base()

def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()
class Books(Base):
    __tablename__ = "books"
    id = Column(BigInteger, primary_key=True, index=True)
    book_name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    price = Column(BigInteger, nullable=False)
    quantity = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)