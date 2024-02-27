from celery import Celery
from User.settings import REDIS_URL
from User.settings import HOST, REDIS_PORT, SECRET_KEY, ALGORITHM, SENDER_EMAIL, SENDER_PASSWORD, REDIS_URL
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

celery = Celery(
    __name__,
    broker=REDIS_URL,
    backend=REDIS_URL,
    broker_connection_retry_on_startup=True
)
@celery.task
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
        
@celery.task
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
# celery -A task worker -l info --pool=solo -E