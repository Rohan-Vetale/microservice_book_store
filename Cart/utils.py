import jwt
from fastapi import HTTPException,Depends, status,Request
import settings
import requests as rq
import logging


class JWT:
    @staticmethod
    def data_decode(token):
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        except Exception as ex:
            raise HTTPException(detail=str(ex), status_code=status.HTTP_400_BAD_REQUEST)


def jwt_authentication(request:Request):
    token = request.headers.get('authorization')
    data = JWT.data_decode(token)
    user_id = data.get('user_id')
    if user_id is None:
        raise HTTPException(detail="Not valid data ",status_code=status.HTTP_404_NOT_FOUND)

    response = rq.get(f'http://127.0.0.1:8080/auth_user?token={token}')

    if response is None:
        raise HTTPException(detail="User Not return anything ",status_code=status.HTTP_404_NOT_FOUND)
    request.state.user = response.json()['user_data']