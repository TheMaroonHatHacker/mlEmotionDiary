"""Rewrite of the API to all use one file. This file will be used to run the API on the server."""

# Description: This file contains the API for the emotion detection model
import emotionPrediction

# import random
from random import randint

# import time
import time
import datetime

import os

# import FastAPI
from fastapi import FastAPI
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


# produce a prediction based on the text provided
@app.get("/predict/{username}/{query}")
def gatherUserInput(username: str, query: str):
    rawPredictionData = emotionPrediction.getPredictionProbability(query)
    mainPrediction = emotionPrediction.predictEmotions(query)  #
    proccessedPredictionData = rawPredictionData
    proccessedPredictionData[
        "main-emotion"
    ] = mainPrediction  # adding the main emotion to the dictionary
    jsonifiedPredictionData = json.dumps(proccessedPredictionData)
    newID = randint(0, 100000)
    cursor = connection.cursor()
    # combine the random id with the current time to create a unique id
    cursor.execute(
        f"INSERT into entries (entryID, username, context, analysis) VALUES ({newID}, '{username}', '{query}', '{jsonifiedPredictionData}');"
    )
    connection.commit()
    cursor.close()
    # return {"main-emotion": mainPrediction}
    return rawPredictionData
    # for i in range(len(rawPredictionData)):
    #    rawPredictionData[i] = rawPredictionData[i] * 100 # converting the probabilities into percentages
    #    return {emotionPrediction.emotionsArray[i]: rawPredictionData[i]}


@app.get("/analysis/{username}")
def overallAnalysis(username: str):
    cursor = connection.cursor()
    cursor.execute(f"SELECT analysis FROM entries WHERE username = '{username}'")
    retrieved = cursor.fetchall()
    newdict = {}
    for item in retrieved:
        actuallyParsed = json.loads(item[0])
        for currentemotion in arrayOfEmotions:
            newdict[currentemotion] = newdict.get(currentemotion, 0) + actuallyParsed[currentemotion]
    for i in range(0, len(newdict)):
        newdict[arrayOfEmotions[i]] = newdict[arrayOfEmotions[i]] / 5
    return newdict


# create user in the database, if the user already exists, return a message saying so
@app.get("/create/{username}/{password}")
def createUser(username: str, password: str):
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT * FROM credentials WHERE username = '{username}' AND password = '{password}'"
    )
    if cursor.fetchone() is None:
        cursor.execute(
            f"INSERT INTO credentials (username, password) VALUES ('{username}', '{password}')"
        )
        connection.commit()
        cursor.close()
        return {"username": username, "password": password, "AlreadyExists": False}
    else:
        cursor.close()
        return {"username": "null", "password": "null", "AlreadyExists": True}


# authenicate user. Returns true if both the username and password match, false otherwise
@app.get("/auth/{username}/{password}")
def authUser(username: str, password: str):
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT * FROM credentials WHERE username = '{username}' AND password = '{password}'"
    )
    if cursor.fetchone() is None:
        cursor.close()
        return {"auth": False}
    else:
        cursor.close()
        return {"auth": True}
