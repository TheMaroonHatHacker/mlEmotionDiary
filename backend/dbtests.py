import mysql.connector
import os
from dotenv import load_dotenv
from random import randint
from datetime import datetime, timedelta

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user="4fht33e26c8bc9t5iy2s",
    password="pscale_pw_a0Qo2bMTwOE1HkOFsSQFxRvfzbDjs2ZiYPzhhpAMMaf",
    database=os.getenv("DB_NAME"),
    autocommit=True,
)

cursor = connection.cursor()


username = "thing"
context = "This is an example entry number 3"
emotions = {
    "happiness": 0.8,
    "sadness": 0.2,
    "anger": 0.5, 
    "worry": 0.1,
}

# Define a function to insert emotions into the Emotions table
def addEntryBeta (username, context, emotions):
    entryID = randint(0, 100000)
    cursor.execute("INSERT INTO entries (entryID, username, text, timeanddate) VALUES (%s, %s, %s, NOW())", (entryID, username, context))
    for emotion, value in emotions.items():
        cursor.execute("SELECT emotionID FROM emotions WHERE emotionType = %s", (emotion,))
        emotionID = cursor.fetchone()[0]
        cursor.execute("INSERT INTO emotionEntries (entryID, emotionID, intensity) VALUES (%s, %s, %s)", (entryID, emotionID, value))
    cursor.execute("SELECT * FROM emotionEntries WHERE entryID = %s", (entryID,))
    return cursor.fetchall()

def getAnalysisBeta (username):
    cursor.execute("SELECT entryID, timeanddate FROM entries WHERE username = %s", (username,))
    entries = cursor.fetchall()
    analysis = {}
    analysis["timeframe"] = []
    for entry in entries:
        cursor.execute("SELECT emotionType, intensity FROM emotionEntries JOIN emotions ON emotionEntries.emotionID = emotions.emotionID WHERE entryID = %s", (entry[0],))
        emotions = cursor.fetchall()
        analysis["timeframe"].append(datetime.strftime(entry[1], "%Y-%m-%d %H:%M:%S"))
        for emotion in emotions:
            if emotion[0] not in analysis:
                analysis[emotion[0]] = []
            analysis[emotion[0]].append(emotion[1])
            
    return analysis

# Test the function
print(addEntryBeta(username, context, emotions))
print(getAnalysisBeta(username))