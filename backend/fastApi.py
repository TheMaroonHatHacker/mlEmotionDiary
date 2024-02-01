"""Rewrite of the API to all use one file. This file will be used to run the API on the server."""

# Description: This file contains the API for the emotion detection model
import emotionPrediction

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


@app.post("/ai/analysis")
def overallAnalysis(username: str):
    cursor = connection.cursor()
    cursor.execute(f"SELECT analysis FROM entries WHERE username = '{username}'")
    retrieved = cursor.fetchall()
    newdict = {}
    for item in retrieved:
        actuallyParsed = json.loads(item[0])
        for currentemotion in arrayOfEmotions:
            newdict[currentemotion] = (
                newdict.get(currentemotion, 0) + actuallyParsed[currentemotion]
            )
    for i in range(0, len(newdict)):
        newdict[arrayOfEmotions[i]] = newdict[arrayOfEmotions[i]] / 5
    return newdict


# authenicate user. Returns true if both the username and password match, false otherwise
@app.post("/auth/login")
def authLogin(
    username: Annotated[str, Form()], password: Annotated[str, Form()], res: Response
):
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM credentials WHERE username = %s", (username,))
    record = cursor.fetchone()
    if record is None:
        success = False
    else:
        hashed_password = record[0]
        success = checkPassword(password, hashed_password)
    cursor.close()
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
def createEntry(username: Annotated[str, Form()], text: Annotated[str, Form()]):
    cursor = connection.cursor()
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
        query = "INSERT into entries (entryID, username, context, analysis) VALUES (%s, %s, %s, %s)"
        values = (newID, username, text, jsonifiedPredictionData)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        return proccessedPredictionData
