from random import randint
from datetime import datetime


class dbInterfaceLite:
    def __init__(self, connection):
        self.connection = connection
    def checkUserPresence(self, username):
        try:
            result = self.connection.execute("SELECT * FROM credentials WHERE username = ?", (username,)).fetchone()
            return result
        except:
            return False
        
    def createUser(self, username, password):
        try:
            self.connection.execute("INSERT INTO credentials (username, password) VALUES (?, ?)", (username, password))
            self.connection.commit()
            self.connection.sync()
            return True
        except:
            return False
    
    def createEntry(self, username, context, emotions):
        entryID = randint(0, 100000)
        try:
            self.connection.execute("INSERT INTO entries (entryID, username, text, timeanddate) VALUES (?, ?, ?, ?)", (entryID, username, context, datetime.now()))
            for emotion, value in emotions.items():
                emotionID = self.connection.execute("SELECT emotionID FROM emotions WHERE emotionType = ?", (emotion,)).fetchone()[0]
                self.connection.execute("INSERT INTO emotionEntries (entryID, emotionID, intensity) VALUES (?, ?, ?)", (entryID, emotionID, value))
            #self.connection.commit()
            self.connection.sync()
            return True
        except:
            return False
        
    def getAnalysis(self, username):
        analysis = {}
        analysis["timeframe"] = []
        monthlyAverages = self.connection.execute("SELECT emotionType, AVG(intensity) AS avg_intensity, strftime('%Y-%m', timeanddate) AS month FROM emotionEntries JOIN emotions ON emotionEntries.emotionID = emotions.emotionID JOIN entries ON emotionEntries.entryID = entries.entryID WHERE entries.username = ? GROUP BY emotionType, month ORDER BY month ASC, emotionType ASC", (username,)).fetchall()
        for emotion, avgIntensity, month in monthlyAverages:
            if emotion not in analysis:
                analysis[emotion] = []
            analysis[emotion].append(avgIntensity)
            if month not in analysis["timeframe"]:
                analysis["timeframe"].append(month)
        return analysis
    
    def getTextHistory(self, username):
        entries = self.connection.execute("SELECT entryID, timeanddate, text FROM entries WHERE username = ? ORDER BY timeanddate DESC", (username,)).fetchall()
        return entries
    
        

            