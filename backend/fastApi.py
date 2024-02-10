"""Rewrite of the API to all use one file. This file will be used to run the API on the server."""

# Description: This file contains the API for the emotion detection model
import emotionPrediction

#For data analysis
import pandas as pd

# import all the libraries needed for JWT
from typing import Annotated
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from bcrypt import hashpw, gensalt, checkpw

# import random
from random import randint

import os

# import FastAPI
from fastapi import FastAPI, Form, Response, status
from fastapi.middleware.cors import CORSMiddleware

# Allow for the use of .env files
from dotenv import load_dotenv

# mysql connection
# import MySQLdb
import mysql.connector

# json handling
import json


# load the .env file
load_dotenv()

# connect to the database
connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    autocommit=True,
)

arrayOfEmotions = [
    "fun",
    "hate",
    "love",
    "anger",
    "empty",
    "worry",
    "relief",
    "boredom",
    "neutral",
    "sadness",
    "surprise",
    "happiness",
    "enthusiasm",
]

# initialize the FastAPI app
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def hashThePassword(password):
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")


def checkPassword(password, hashed):
    return checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def decodePassword(password):
    return password.decode("utf-8")

def createJWTToken(username):
    token = jwt.encode(
        {"exp": datetime.utcnow() + timedelta(minutes=30), "username": username},
        os.getenv("JWT_SECRET"),
        algorithm="HS256",
    )
    return token
def decodeJWTToken(token):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        return "expired"
    except JWTError:
        return "invalid"


# authenicate user. Returns true if both the username and password match, false otherwise
@app.post("/auth/login")
def authLogin(
    username: Annotated[str, Form()], password: Annotated[str, Form()], res: Response
):
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM credentials WHERE username = %s", (username,))
    record = cursor.fetchone()
    cursor.close()
    if record is None:
        return {"auth": False, "token": None}
    hashed_password = record[0]
    success = checkPassword(password, hashed_password)
    if not success:
        return {"auth": False, "token": None}
    return {"auth": success, "token": createJWTToken(username)}


# create a new user
@app.post("/auth/signup")
def authSignUp(
    username: Annotated[str, Form()], password: Annotated[str, Form()], res: Response
):
    hashed = hashThePassword(password)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM credentials WHERE username = %s", (username,))
    if cursor.fetchone() is None:
        try:
            cursor.execute(
                "INSERT INTO credentials (username, password) VALUES (%s, %s)",
                (username, hashed),
            )
            connection.commit()
            success = True
        except Exception as e:
            print(e)  # or log the error
            success = False
    else:
        success = False
    cursor.close()
    return {"auth": success}


# Create a new entry
@app.post("/ai/predict")
def createEntry(text: Annotated[str, Form()], token: Annotated[str, Form()]):
    cursor = connection.cursor()
    decodedToken = decodeJWTToken(token)
    if decodedToken == "expired" or decodedToken == "invalid":
        return {"error": "Invalid token"}
    username = decodedToken["username"]
    query = "SELECT username FROM credentials WHERE username = %s"
    cursor.execute(query, (username,))
    record = cursor.fetchone()
    if record is None:
        return {"error": "User does not exist"}
    else:
        rawPredictionData = emotionPrediction.getPredictionProbability(text)
        proccessedPredictionData = rawPredictionData
        jsonifiedPredictionData = json.dumps(proccessedPredictionData)
        newID = randint(0, 100000)
        # combine the random id with the current time to create a unique id
        query = "INSERT into entries (entryID, username, context, analysis, timeanddate) VALUES (%s, %s, %s, %s, NOW())"
        values = (newID, username, text, jsonifiedPredictionData)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        return proccessedPredictionData

@app.post("/ai/analysis")
def overallAnalysis(token: Annotated[str, Form()]):
    decodedToken = decodeJWTToken(token)
    if decodedToken == "expired" or decodedToken == "invalid":
        #cursor.close()
        return {"error": "Invalid token"}
    username = decodedToken["username"]
    cursor = connection.cursor()
    cursor.execute("SELECT analysis, timeanddate FROM entries WHERE username = %s", (username, ))
    retrieved = cursor.fetchall()
    emotionData = {}
    for i in arrayOfEmotions:
        emotionData[i] = []
    emotionData["timeframe"] = []    
    for item in retrieved:
        emotionData["timeframe"].append(item[1])
        retrievedEmotionData = json.loads(item[0])
        for i in retrievedEmotionData:
            emotionData[i].append(retrievedEmotionData[i])
    cursor.close()
    return emotionData

        
