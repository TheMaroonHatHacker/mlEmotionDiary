from jose import jwt, JWTError, ExpiredSignatureError
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class jwtHandler:
    def __init__(self, secret):
        self.secret = secret
        if self.secret is None:
            raise ValueError("Secret was not supplied.") # if the secret is not supplied, raise an error


    def createJWTToken(self, username):
        if username is None:
            raise ValueError("Username was not supplied.") # if the username is not supplied, raise an error
        token = jwt.encode(
            {"exp": datetime.utcnow() + timedelta(days=5), "username": username},
            self.secret,
            algorithm="HS256",
        ) # create a token with the username and an expiry time of 5 days
        return token
    def decodeJWTToken(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"]) # decode the token
            return payload # return the payload
        except ExpiredSignatureError:
            return "expired" # if the token is expired, return expired
        except JWTError:
            return "invalid" # if the token is invalid, return invalid
