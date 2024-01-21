import requests


def auth(username, password):
    requestUrl = "http://127.0.0.1:8000/auth/" + username + "/" + password
    response = requests.get(requestUrl)
    return response


def predict(username, context):
    requestUrl = "http://127.0.0.1:8000/predict/" + username + context
    response = requests.get(requestUrl)
    return response


def signup(username, password):
    requestUrl = "http://127.0.0.1:8000/create/" + username + password
    response = requests.get(requestUrl)
    return response


menuitems = ["login", "create user", "Predict Emotion", "Return Data"]

for i in range(0, len(menuitems)):
    print(i, menuitems[i])

userinput = input("Please enter an option")

if userinput == "0":
    usrname = input("Please enter the username")
    usrpaswd = input("Please enter your password")
    print(auth(usrname, usrpaswd))
