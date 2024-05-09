from random import randint

class dbInterface: # class to interface with the database
    def __init__(self, connection):
        self.connection = connection # initialize the connection to the database
    def checkUserPresence(self, username):
        cursor = self.connection.cursor() # create a cursor object
        try :
            cursor.execute("SELECT * FROM credentials WHERE username = %s", (username,)) # execute the query
            result = cursor.fetchone()
            cursor.close()
            return result
        except: # if there is an error, return false
            return False

    def createUser(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO credentials (username, password) VALUES (%s, %s)", (username, password)) # insert the new user into the database
        cursor.close()

    def createEntry(self, username, context, emotions):
        cursor = self.connection.cursor()
        entryID = randint(0, 100000) # generate a random entry ID
        cursor.execute("INSERT INTO entries (entryID, username, text, timeanddate) VALUES (%s, %s, %s, NOW())", (entryID, username, context,)) # insert the entry into the database
        for emotion, value in emotions.items():
            cursor.execute("SELECT emotionID FROM emotions WHERE emotionType = %s", (emotion,)) # get the emotion ID
            emotionID = cursor.fetchone()[0]
            cursor.execute("INSERT INTO emotionEntries (entryID, emotionID, intensity) VALUES (%s, %s, %s)", (entryID, emotionID, value)) # insert the emotion data into the database
        cursor.close()

    def getAnalysis(self, username):
        cursor = self.connection.cursor()
        analysis = {}
        analysis["timeframe"] = []
        # get the average intensity of each emotion for each month
        cursor.execute("SELECT emotionType, AVG(intensity) AS avg_intensity, DATE_FORMAT(timeanddate, '%Y-%m') AS month FROM emotionEntries JOIN emotions ON emotionEntries.emotionID = emotions.emotionID JOIN entries ON emotionEntries.entryID = entries.entryID WHERE entries.username = %s GROUP BY emotionType, month ORDER BY month ASC, emotionType ASC", (username,))
        monthlyAverages = cursor.fetchall() # fetch the data
        for emotion, avgIntensity, month in monthlyAverages:
            if emotion not in analysis: # if the emotion is not in the analysis dictionary, add it
                analysis[emotion] = []
            analysis[emotion].append(avgIntensity) # add the data to the analysis dictionary
            if month not in analysis["timeframe"]: # if the month is not in the timeframe, add it
                analysis["timeframe"].append(month)
        return analysis
    def getTextHistory(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT entryID, timeanddate, text FROM entries WHERE username = %s ORDER BY timeanddate DESC", (username,))
        entries = cursor.fetchall()
        return entries
