# Importing the libraries
import joblib
# Loading the model
theModel = joblib.load(open("./models/emotion_classifier_pipe_rf.pkl", "rb"))


# Takes input from the user and returns one dominant emotion as a string

# Takes input from the user and returns the probabilities of all the emotions as a list
def getPredictionProbability(input_text):  # input_text is a list of strings
    results = theModel.predict_proba([input_text])[0]
    proccessedResults = {}
    for i in range(len(results)):
        proccessedResults[theModel.classes_[i]] = (
         int(results[i]*100)
        )  # converting the probabilities into percentages

    return proccessedResults
