from jose import jwt, JWTError, ExpiredSignatureError
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

class jwtHandler:
    def __init__(self):
        if os.getenv("JWT_SECRET") == None:
            self.secret = os.getenv("JWT_SECRET")
            if self.secret is None:
                raise ValueError("JWT Secret environment variable missing.")

    def createJWTToken(self, username):
        if username is not str:
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

