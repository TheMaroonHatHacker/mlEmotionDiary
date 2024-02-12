import mysql.connector
from random import randint


class dbInterface:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            autocommit=True,
        )
    def checkUserPresence(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT password FROM credentials WHERE username = %s", (username,))
        result = cursor.fetchall()
        cursor.close()
        return result
    def checkUserAndPass(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT password FROM credentials WHERE username = %s", (username,))
        result = cursor.fetchnone()
        cursor.close()
        return result
    def createUser(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO credentials (username, password) VALUES (%s, %s)", (username, password))
        cursor.close()
    def createEntry(self, username, context, rawdata):
        entryID = randint(0, 100000)
        cursor = self.connection.cursor()
        cursor.execute("INSERT into entries (entryID, username, context, analysis, timeanddate) VALUES (%s, %s, %s, %s, NOW())", (entryID, username, context, rawdata))
        cursor.close()
    def getAnalysis(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT analysis, timeanddate FROM entries WHERE username = %s", (username,))
        result = cursor.fetchall()
        cursor.close()
        return result
    