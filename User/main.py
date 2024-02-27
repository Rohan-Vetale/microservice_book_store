
from utils import JWT
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from model import User, get_db
from schema import UserDetails, Userlogin
from passlib.hash import sha256_crypt
from settings import super_key
app = FastAPI()
jwt_handler = JWT()


@app.post("/register", status_code=status.HTTP_201_CREATED)
def user_registration(body: UserDetails, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create api for adding a new user.
    Parameter: body : UserDetails object, response : Response object, db : database session.
    Return: Message of user data added with status code 201.
    """
    try:
        user_data = body.model_dump()
        user_data['password'] = sha256_crypt.hash(user_data['password'])
        #if user has provided valid super key user is super user
        if user_data['super_key'] == super_key:
            user_data['is_super_user'] = True
        user_data.pop('super_key')
        new_user = User(**user_data)
        db.add(new_user)
        db.commit()
        
        token = jwt_handler.jwt_encode({'user_id': new_user.id})
        #using celery to send mail
        
        #result = send_verification_mail.delay(token, new_user.email)
        
        db.refresh(new_user)
        return {"status": 201, "message": "Registered successfully, check your mail to verify email", 'data': new_user, 'token' : token}
    except Exception as e:
        response.status_code = 400
        print(e)
        return {"message": str(e), 'status': 400}


@app.post("/login", status_code=status.HTTP_200_OK)
def user_login(payload: Userlogin, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create api for login the user.
    Parameter: payload : UserLogin object, response : Response object, db : database session.
    Return: Message of user logged in with status code 200.
    """
    try:
        user = db.query(User).filter_by(user_name=payload.user_name).first()
        if user and sha256_crypt.verify(payload.password, user.password) and user.is_verified:
            token = jwt_handler.jwt_encode({'user_id': user.id})
            return {'status': 200, "message": 'Logged in successfully', 'access_token': token}
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"message": 'Invalid username, password, or user not verified', 'status': 401}
        
    except Exception as e:
        response.status_code = 400
        return {"message": str(e), 'status': 400}
    
    
@app.get("/verify")
def verify_user(token: str, db: Session = Depends(get_db)):
    """
    Description: This function create api to verify the request when we click the verification link on send on mail.
    Parameter: token : object as string, db : as database session.
    Return: Message with status code 200 if verified done or 500 if internal server error
    """
    try:
        decode_token = JWT.jwt_decode(token)
        
        user_id = decode_token.get('user_id')
        user = db.query(User).filter_by(id=user_id, is_verified=False).one_or_none()
        if not user:
            raise HTTPException(status_code=400, detail='User already verified or not found')
        user.is_verified = True
        db.commit()
        return {'status': 200, "message": 'User verified successfully', }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal Server Error')