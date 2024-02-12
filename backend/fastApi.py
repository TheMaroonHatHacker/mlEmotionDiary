"""Rewrite of the API to all use one file. This file will be used to run the API on the server."""

# Import user defined modules
import emotionPrediction
from jwthandler import jwtHandler
from dbInterface import dbInterface

# import all the libraries needed for JWT
from typing import Annotated
from datetime import datetime, timedelta
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





# create a list of all the emotions that the model can detect.
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
origins = ["*"] # allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

host = os.getenv("DB_HOST")
user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
autocommit = True



# create the JWT handler and the database interfacez
jwtHandle = jwtHandler(os.getenv("JWT_SECRET"))
dbHandle = dbInterface(host, user, password, database)

# reimplment password hashing to be more stateful?
def hashThePassword(password):
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")


def checkPassword(password, hashed):
    return checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def decodePassword(password):
    return password.decode("utf-8")


# authenicate user. Returns true if both the username and password match, false otherwise
@app.post("/auth/login")
def authLogin(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
):
    record = dbHandle.checkUserPresence(username) # check if the username exists
    if record is None:
        return {"auth": False, "token": None} # if the username does not exist, return false
    hashed_password = record[0] # get the hashed password from the returned record
    success = checkPassword(password, hashed_password)  # check if the password matches the hashed password
    if not success: # if the password does not match, return false
        return {"auth": False, "token": None}
    return {"auth": success, "token": jwtHandle.createJWTToken(username)} # if the password matches, return true and a token


# create a new user
@app.post("/auth/signup") # declaring the API route
def authSignUp(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
):
    hashed = hashThePassword(password) # hash the password
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM credentials WHERE username = %s", (username,)) # check if the username already exists
    if cursor.fetchone() is None: # if the username does not exist, create a new entry
        try:
            cursor.execute(
                "INSERT INTO credentials (username, password) VALUES (%s, %s)",
                (username, hashed),
            ) 
            success = True # return true if the user was created
        except Exception as e: # if there is an error, return false
            print(e)  
            success = False
    else:
        success = False # if the username already exists, return false
    cursor.close() # close the cursor
    return {"auth": success}


# Create a new entry
@app.post("/ai/entry") # declare the API route
def processEntry(text: Annotated[str, Form()], token: Annotated[str, Form()]):
    cursor = connection.cursor()
    decodedToken = jwtHandle.decodeJWTToken(token) # decode the token
    if decodedToken == "expired" or decodedToken == "invalid": # if the token is expired or invalid, return an error
        return {"error": "Invalid token"}
    username = decodedToken["username"] # get the username from the token
    query = "SELECT username FROM credentials WHERE username = %s" # check if the user exists
    cursor.execute(query, (username,)) # execute the query
    record = cursor.fetchone() # get the result of the query
    if record is None: # if the user does not exist, return an error
        return {"error": "User does not exist"} 
    else:
        rawPredictionData = emotionPrediction.getPredictionProbability(text) # get the prediction data
        proccessedPredictionData = rawPredictionData 
        jsonifiedPredictionData = json.dumps(proccessedPredictionData)  # convert the prediction data from a dictionary to a json string
        newID = randint(0, 100000)
        # combine the random id with the current time to create a unique id
        query = "INSERT into entries (entryID, username, context, analysis, timeanddate) VALUES (%s, %s, %s, %s, NOW())" # create the query 
        values = (newID, username, text, jsonifiedPredictionData) # create the values to be inserted
        cursor.execute(query, values) # execute the query
         # commit the changes
        cursor.close() # close the cursor
        return proccessedPredictionData # return the prediction data

@app.post("/ai/analysis")
def overallAnalysis(token: Annotated[str, Form()]):
    decodedToken = jwtHandle.decodeJWTToken(token) # decode the token
    if decodedToken == "expired" or decodedToken == "invalid": # if the token is expired or invalid, return an error
        #cursor.close()
        return {"error": "Invalid token"}
    username = decodedToken["username"] # get the username from the token
    cursor = connection.cursor() # create a cursor
    cursor.execute("SELECT analysis, timeanddate FROM entries WHERE username = %s", (username, )) # get the analysis data for the user
    retrieved = cursor.fetchall() # get the result of the query
    emotionData = {} # create a dictionary to store the data
    for i in arrayOfEmotions:
        emotionData[i] = [] # create a list for each emotion
    emotionData["timeframe"] = [] # create a list for the timeframe
    for item in retrieved: 
        emotionData["timeframe"].append(item[1]) # add the time and date to the timeframe list
        retrievedEmotionData = json.loads(item[0]) # get the analysis data
        for i in retrievedEmotionData:
            emotionData[i].append(retrievedEmotionData[i]) # add the analysis data to the dictionary
    cursor.close()
    return emotionData # return the analysis data

        
