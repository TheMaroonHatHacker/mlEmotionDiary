"use client";
import React, { useState } from "react";

export default function MyComponent() {
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
  const usrName = (window as any).localStorage.getItem("username");
  console.log(usrName);
  const handleClick = async () => {
    if (inputText === "") {
      setStatus("please enter some text");
    } else {
      setStatus("loading...");
      const response = await fetch(
        `http://127.0.0.1:8000/predict/${usrName}/${inputText}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
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

  return (
    <div className="">
      <div className="justify-center items-center flex join join-horizontal">
        <input
          className="textarea textarea-bordered join-item"
          type="text"
          value={inputText}
          placeholder="Enter a query"
        />
        <button className="btn join-item" onClick={handleClick}>
          Submit
        </button>
      </div>
      <div className="text-center justify-center m-8">
        <p>{status}</p>
      </div>
      <div className="m-8 grid grid-cols-5 text-center">
        {emotions &&
          Object.entries(emotions).map(([emotion, intensity], index) => (
            <div
              key={index}
              className="radial-progress m-8 text-primary"
              style={{ "--value": intensity }}
            >
              {emotion} - {intensity}
            </div>
          ))}
      </div>
    </div>
  );
}
