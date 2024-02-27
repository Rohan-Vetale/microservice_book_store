
import pytz

from datetime import datetime, timedelta
from settings import HOST, REDIS_PORT, SECRET_KEY, ALGORITHM, SENDER_EMAIL, SENDER_PASSWORD, REDIS_URL
from datetime import datetime, timedelta
import pytz
from jose import jwt
from fastapi import Depends, HTTPException, Request,status
from sqlalchemy.orm import Session
from model import get_db, User
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import redis

redis_obj = redis.Redis(host=HOST, port=REDIS_PORT, decode_responses=True)


def jwt_authentication(request : Request, db:Session = Depends(get_db)):
    try:
        token = request.headers.get('authorization')
        decoded_token = JWT.jwt_decode(token)
        user_id = decoded_token.get('user_id')
        user_data = db.query(User).filter_by(id=user_id).one_or_none()
        if not user_data:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        request.state.user = user_data
    except Exception as e:
        print(e)
    
    
   
class JWT:
    @staticmethod
    def jwt_encode(payload: dict):
        if 'exp' not in payload:
            payload.update(exp=datetime.now(pytz.utc) + timedelta(hours=1), iat=datetime.now(pytz.utc))
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def jwt_decode(token):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.JWTError as e:
            print(e)
        
def send_verification_mail(verification_token : str, email):
    """
    Description:
    Function to send token link over provided email using smtp

    Parameter:
    verification_token : token generated while user login
    email : email of whom we want to send the link as a mail

    Return:
    None
    """
    try:
        # Your Gmail account details
        sender_email = SENDER_EMAIL
        sender_password = SENDER_PASSWORD
        recipient_email = email
        
        # Compose the email
        subject = 'Email Verification'
        body = f"Click the link to verify your email: http://127.0.0.1:8080/user/verify?token={verification_token}"
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
       
        # Set up the SMTP server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, recipient_email, msg.as_string())
        
        server.quit()
    except Exception as e:
        print(e)
        
class Redis:
    @staticmethod
    def add_redis(name, key, value):
        """
        Description: This function add and update data in redis memory.
        Parameter: name: key, key: field ,  value: value as parameter.
        Return: set the name, key, value to redis memory
        """
        return redis_obj.hset(name, key, value)

    @staticmethod
    def get_redis(name):
        """
        Description: This function get all data from redis memory.
        Parameter: name as parameter.
        Return: get all data from the redis memory using name.
        """
        return redis_obj.hgetall(name)

    @staticmethod
    def delete_redis(name, key):
        """
        Description: This function delete data from redis memory.
        Parameter: name, key as parameter.
        Return: delete data from redis using name and list of key.
        """
        return redis_obj.hdel(name, key)
    
    
def send_confirmation_mail( email: str,message_body:str):
    """
    Description:
    Function to send order confirmation over provided email using smtp

    Parameter:
    message_body : message to be sent to the user
    email : email of whom we want to send the message as a mail

    Return:
    None
    """
    try:
        # Your Gmail account details
        sender_email = SENDER_EMAIL
        sender_password = SENDER_PASSWORD
        recipient_email = email
        
        # Compose the email
        subject = 'Order Confirmation'
        body = message_body
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
       
        # Set up the SMTP server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, recipient_email, msg.as_string())
        
        server.quit()
    except Exception as e:
        print(e)