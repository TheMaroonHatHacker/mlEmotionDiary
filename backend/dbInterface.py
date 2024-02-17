from random import randint
from datetime import datetime

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
        cursor.execute("INSERT INTO entries (entryID, username, text, timeanddate) VALUES (%s, %s, %s, NOW())", (entryID, username, context))
        for emotion, value in emotions.items():
            cursor.execute("SELECT emotionID FROM emotions WHERE emotionType = %s", (emotion,))
            emotionID = cursor.fetchone()[0]
            cursor.execute("INSERT INTO emotionEntries (entryID, emotionID, intensity) VALUES (%s, %s, %s)", (entryID, emotionID, value))
        cursor.close()
    
    def getAnalysis(self, username):
        cursor = self.connection.cursor()
        analysis = {}
        analysis["timeframe"] = []
        cursor.execute("SELECT emotionType, intensity FROM emotionEntries JOIN emotions ON emotionEntries.emotionID = emotions.emotionID JOIN entries ON emotionEntries.entryID = entries.entryID  WHERE entries.username = %s", (username,))
        emotions = cursor.fetchall()
        for emotion in emotions:
            print(emotion)
            if emotion[0] not in analysis:
                analysis[emotion[0]] = []
            analysis[emotion[0]].append(emotion[1])
        cursor.execute("SELECT timeanddate FROM entries WHERE username = %s", (username,))
        time = cursor.fetchall()
        for item in time:
            analysis["timeframe"].append(datetime.strftime(item[0], "%Y-%m-%d %H:%M:%S"))
                
        return analysis
    