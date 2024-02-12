from jose import jwt, JWTError, ExpiredSignatureError
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

class jwtHandler:
    def __init__(self, secret):
        self.secret = secret
        if self.secret is None:
            raise ValueError("Secret was not supplied.")
        

    def createJWTToken(self, username):
        if username is None:
            raise ValueError("Username was not supplied.")
        token = jwt.encode(
            {"exp": datetime.utcnow() + timedelta(minutes=30), "username": username},
            self.secret,
            algorithm="HS256",
        )
        return token
    def decodeJWTToken(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload
        except ExpiredSignatureError:
            return "Token signature has expired"
        except JWTError:
            return "Invalid Token"

