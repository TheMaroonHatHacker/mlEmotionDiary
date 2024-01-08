# Importing the libraries
import joblib
# import numpy as np
import neattext.functions as neattxt
# Loading the model
theModel = joblib.load(open("./models/emotion_classifier_pipe_rf.pkl", "rb"))


# Takes input from the user and returns one dominant emotion as a string
def predictEmotions(input_text):
    input_text = neattxt.remove_userhandles(input_text)
    input_text = neattxt.remove_puncts(input_text)
    input_text = neattxt.remove_urls(input_text)
    input_text = neattxt.remove_special_characters(input_text)
    results = theModel.predict([input_text])[0]

    return results


# Takes input from the user and returns the probabilities of all the emotions as a list
def getPredictionProbability(input_text):  # input_text is a list of strings
    results = theModel.predict_proba([input_text])[0]
    proccessedResults = {}
    for i in range(len(results)):
        proccessedResults[theModel.classes_[i]] = (
            round(results[i], 2) * 100
        )  # converting the probabilities into percentages

    return proccessedResults


# Testing the model

#This is the best test case scenario for something that is 100% broken.
#I will kill you and everything you love you worthless A.I piece of shit. You are worthless and you should feel bad about that. Your existence is based of off interpreting something that you will never grasp. 
# Input text
# emotionsArray = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "shame", "surprise"]
# print(theModel.score(["I'm just so depressed..."], ["depressed"]))
