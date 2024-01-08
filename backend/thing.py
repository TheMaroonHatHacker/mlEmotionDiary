from dotenv import load_dotenv
import os
import MySQLdb

load_dotenv()

connection = MySQLdb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True,
    ssl={"ca": "/etc/ssl/cert.pem"},
)

cursor = connection.cursor()
cursor.execute(
    f"CREATE TABLE `userprompts` (`username` varchar(36) NOT NULL, `context` varchar(36),`happiness` int, PRIMARY KEY (`username`))"
)
