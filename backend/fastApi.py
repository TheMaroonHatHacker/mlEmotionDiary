'''Rewrite of the API to all use one file. This file will be used to run the API on the server.'''

# Description: This file contains the API for the emotion detection model
import emotionPrediction

import os
# import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#Allow for the use of .env files
from dotenv import load_dotenv

# mysql connection
import MySQLdb

# json handling
import json

#load the .env file
load_dotenv()

#connect to the database
connection = MySQLdb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True,
    ssl={"ca": "/etc/ssl/cert.pem"},
)
cursor = connection.cursor()
#initialize the FastAPI app

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

    cursor.execute(f"INSERT into entries (username, context, analysis) VALUES ('{username}', '{query}', '{jsonifiedPredictionData}')") 
    # return {"main-emotion": mainPrediction}
    return rawPredictionData
    # for i in range(len(rawPredictionData)):
    #    rawPredictionData[i] = rawPredictionData[i] * 100 # converting the probabilities into percentages
    #    return {emotionPrediction.emotionsArray[i]: rawPredictionData[i]}


# create user in the database, if the user already exists, return a message saying so
@app.get("/create/{username}/{password}")
def createUser(username: str, password: str):
    cursor.execute(
        f"SELECT * FROM credentials WHERE username = '{username}' AND password = '{password}'"
    )
    if cursor.fetchone() is None:
        cursor.execute(
            f"INSERT INTO credentials (username, password) VALUES ('{username}', '{password}')"
        )
        return {"username": username, "password": password, "AlreadyExists": False}
    else:
        return {"username": "null", "password": "null", "AlreadyExists": True}


# authenicate user. Returns true if both the username and password match, false otherwise
@app.get("/auth/{username}/{password}")
def authUser(username: str, password: str):
    cursor.execute(f"SELECT * FROM credentials WHERE username = '{username}' AND password = '{password}'")
    if cursor.fetchone() is None:
        return {"auth": False}
    else:
        return {"auth": True}
    