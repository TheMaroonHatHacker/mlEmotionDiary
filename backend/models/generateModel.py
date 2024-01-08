import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# import numpy as np  # linear algebra
import neattext.functions as neattxt  # text cleaning

# from sklearn.linear_model import LogisticRegression # model
from sklearn.ensemble import RandomForestClassifier  # model
from sklearn.pipeline import Pipeline  # pipeline

# from sklearn.naive_bayes import MultinomialNB # model
from sklearn.feature_extraction.text import CountVectorizer  # vectorizer
from sklearn.model_selection import train_test_split  # splitting data
import joblib  # saving model

importedSentimentData = pd.read_csv("./data/tweet_emotions.csv")  # importing data
importBinaryData = "";
importedSentimentData = importedSentimentData.drop(
    ["tweet_id"], axis=1
)  # dropping tweet_id column since it is not needed

# now to clean the data
importedSentimentData["refined_text"] = importedSentimentData["content"].apply(
    neattxt.remove_userhandles
)  # removing user handles
importedSentimentData["refined_text"] = importedSentimentData["refined_text"].apply(
    neattxt.remove_puncts
)  # removing punctuations
importedSentimentData["refined_text"] = importedSentimentData["refined_text"].apply(
    neattxt.remove_urls
)  # removing urls
importedSentimentData["refined_text"] = importedSentimentData["refined_text"].apply(
    neattxt.remove_special_characters
)  # removing special characters

cleanedData = importedSentimentData[
    "refined_text"
]  # creating a new dataframe with only the refined_text column
labels = importedSentimentData[
    "sentiment"
]  # creating a new dataframe with only the sentiment column
cleanedData_train, cleanedData_test, labels_train, labels_test = train_test_split(
    cleanedData, labels, test_size=0.2, random_state=42
)  # splitting the data into training and testing data

rfPipeline = Pipeline(
    [("vectorizer", CountVectorizer()), ("model", RandomForestClassifier())]
)  # creating a pipeline with a vectorizer and a model
rfPipeline.fit(
    cleanedData_train, labels_train
)  # fitting the training data to the pipeline
rfPipeline.score(cleanedData_test, labels_test)  # testing the model
pipeline_file = open(
    "emotion_classifier_pipe_rf.pkl", "wb"
)  # creating a file to dump the pipeline into
joblib.dump(
    rfPipeline, pipeline_file
)  # dumping th contents of the pipeline into the file
pipeline_file.close()  # closing the file
