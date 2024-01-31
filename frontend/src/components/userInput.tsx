"use client";
import React, { useState } from "react";

export const UserInput = (props: {userName: string | null}) => {
  type Emotion = {
    anger: number;
    boredom: number;
    empty: number;
    enthusiasm: number;
    fun: number;
    happiness: number;
    hate: number;
    love: number;
    neutral: number;
    relief: number;
    sadness: number;
    suprise: number;
    worry: number;
  };
  const initialEmotion: Emotion = {
    anger: 0,
    boredom: 0,
    empty: 0,
    enthusiasm: 0,
    fun: 0,
    happiness: 0,
    hate: 0,
    love: 0,
    neutral: 0,
    relief: 0,
    sadness: 0,
    suprise: 0,
    worry: 0,
  };
  const [status, setStatus] = useState("");
  const [emotions, setEmotions] = useState<Emotion | null>(initialEmotion);
  const [inputText, setInputText] = useState("");
  const usrName = props.userName;
  console.log(usrName);
  const handlePredict = async () => {
    if (inputText === "") {
      setStatus("please enter some text");
    } else {
      setStatus("loading...");
      const form = new FormData();
      form.append("text", inputText);
      form.append("username", usrName);
      const response = await fetch(
        `http://127.0.0.1:8000/ai/predict`,
        {
          method: "POST",
          body: form,
        }
      );
      const data = await response.json();
      setEmotions(data);
      setStatus("Data Loaded");
      const emotion = [
        "anger",
        "boredom",
        "empty",
        "enthusiasm",
        "fun",
        "happiness",
        "hate",
        "love",
        "neutral",
        "relief",
        "sadness",
        "suprise",
        "worry",
      ];
    }
  };

  const handleAnalysis = async () => {
    setStatus("Loading...")
    const form = new FormData()
    form.append("username", usrName);
      const response = await fetch(
        `http://127.0.0.1:8000/ai/analysis`,
        {
          method: "POST",
          body: form,
        }
      );
      const data = await response.json();
      if (data["error"]) {
        setStatus("No data found")
      } else {
        setEmotions(data);
        setStatus("Data Loaded");
        const emotion = [
        "anger",
        "boredom",
        "empty",
        "enthusiasm",
        "fun",
        "happiness",
        "hate",
        "love",
        "neutral",
        "relief",
        "sadness",
        "suprise",
        "worry",
      ];
      }
      
    
  }

  return (
    <div className="">
      <div className="justify-center items-center flex join join-horizontal">
      <textarea className="textarea textarea-primary join-item" type="text" value={inputText} onChange={(e) => setInputText(e.target.value)} />
            <button className="btn btn-primary join-item" onClick={handlePredict}>Predict Emotion</button>
            <button className="btn btn-primary join-item" onClick={handleAnalysis}>Analysis</button>
      </div>
      <div className="text-center justify-center m-8">
        <p>{status}</p>
        <p>{usrName}</p>
      </div>
      <div className="m-8 grid grid-cols-5 text-center">
        {emotions &&
          Object.entries(emotions).map(([emotion, intensity], index) => (
            <div
              key={index}
              className="radial-progress m-8 text-primary"
              style={{ "--value": intensity }}
            >
              {emotion} | {intensity}
            </div>
          ))}
      </div>
    </div>
  );
}
