import joblib
import numpy as np
import pandas as pd

dataSet1 = pd.read_csv("./data/tweet_emotions.csv")
dataSet2 = pd.read_csv("./data/emotion_dataset_raw.csv")

#now test the model
gradientBoostingModel = joblib.load(open("emotion_classifier_pipe_gb.pkl","rb"))
randomForestModel = joblib.load(open("emotion_classifier_pipe_rf.pkl","rb"))
linearRegressionModel = joblib.load(open("emotion_classifier_pipe_lr.pkl","rb"))
print(randomForestModel.score(dataSet2["Text"], dataSet2["Emotion"]))
print(linearRegressionModel.score(dataSet2["Text"], dataSet2["Emotion"])) 
print(gradientBoostingModel.score(dataSet1["content"], dataSet1["sentiment"])) 