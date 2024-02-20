from random import randint
from datetime import datetime, timedelta

class dbInterface:
    def __init__(self, connection):
        self.connection = connection
    def checkUserPresence(self, username):
        cursor = self.connection.cursor()
        try :
            cursor.execute("SELECT * FROM credentials WHERE username = %s", (username,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except:
            return False
    
    def createUser(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO credentials (username, password) VALUES (%s, %s)", (username, password))
        cursor.close()

    def createEntry(self, username, context, emotions):
        cursor = self.connection.cursor()
        entryID = randint(0, 100000)
        cursor.execute("INSERT INTO entries (entryID, username, text, timeanddate) VALUES (%s, %s, %s, NOW())", (entryID, username, context,))
        for emotion, value in emotions.items():
            cursor.execute("SELECT emotionID FROM emotions WHERE emotionType = %s", (emotion,))
            emotionID = cursor.fetchone()[0]
            cursor.execute("INSERT INTO emotionEntries (entryID, emotionID, intensity) VALUES (%s, %s, %s)", (entryID, emotionID, value))
        cursor.close()
    
    def getAnalysis(self, username):
        cursor = self.connection.cursor()
        analysis = {}
        analysis["timeframe"] = []
        cursor.execute("SELECT emotionType, AVG(intensity) AS avg_intensity, DATE_FORMAT(timeanddate, '%Y-%m') AS month FROM emotionEntries JOIN emotions ON emotionEntries.emotionID = emotions.emotionID JOIN entries ON emotionEntries.entryID = entries.entryID WHERE entries.username = %s GROUP BY emotionType, month ORDER BY month ASC, emotionType ASC", (username,))
        monthlyAverages = cursor.fetchall()
        for emotion, avgIntensity, month in monthlyAverages:
            if emotion not in analysis:
                analysis[emotion] = []
            analysis[emotion].append(avgIntensity)
            if month not in analysis["timeframe"]:
                analysis["timeframe"].append(month)
        return analysis
    def getTextHistory(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT entryID, timeanddate, text FROM entries WHERE username = %s ORDER BY timeanddate DESC", (username,))
        entries = cursor.fetchall()
        return entries