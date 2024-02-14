import emotionPrediction
from jwthandler import jwtHandler
from dbInterface import dbInterface
from pwHash import pwHash

import os
from dotenv import load_dotenv

import mysql.connector

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    autocommit=True
)

jwtHandle = jwtHandler(os.getenv("JWT_SECRET"))
dbHandle = dbInterface(connection)
hashhandle = pwHash()

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

def login(username, password):
    user = dbHandle.getUser(username)
    if user is None:
        return "invalid"
    if hashhandle.check(password, user[2]):
        return jwtHandle.createJWTToken(username)
    return "invalid"

def signup(username, password):
    if dbHandle.getUser(username) is not None:
        return "invalid"
    dbHandle.addUser(username, hashhandle.hash(password))
    return jwtHandle.createJWTToken(username)

def getEmotions(input_text):
    return emotionPrediction.getPredictionProbability(input_text)

def createEntry(username, emotion, text):
    dbHandle.createEntry(username, emotion, text)
    return "success"

def getAnalysis(username):
    return dbHandle.getAnalysis(username)

