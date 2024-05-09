"use client";
import React, { useState } from "react"; /*import react JS library*/

export const UserInput = (props: {
  /*Defines the properties used (and the types expected for the props passed in).  */
  userName: string | null;
  token: string | null;
}) => {
  type Emotion = {
    /*Defines the types of the emotions that can be predicted. */ anger: number;
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
    /*Initializes the emotions to 0. */ anger: 0,
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
  const [emotions, setEmotions] = useState<Emotion | null>(
    initialEmotion,
  ); /*Initializes the emotions to the initialEmotion. */
  const [inputText, setInputText] = useState("");
  const usrName =
    props.userName; /*Initializes the usrName to the userName passed in. */
  const usrToken =
    props.token; /*Initializes the usrToken to the token passed in. */
  const handlePredict = async () => {
    if (inputText === "") {
      setStatus("please enter some text");
      return;
    }
    if (usrName === null || usrToken === null) {
      setStatus("please login to use this feature");
      return;
    }
    setStatus("loading...");
    const form = new FormData(); /*Creates a new FormData object. */
    form.append(
      "text",
      inputText,
    ); /*Appends the inputText and the user token to the FormData object */
    form.append("token", usrToken);
    const response = await fetch(`http://127.0.0.1:8000/ai/entry`, {
      method: "POST",
      body: form,
    }); /*Fetches the data from the server. */
    const data = await response.json();
    if (data.error) {
      setStatus(data.error);
      return;
    }
    setEmotions(
      data,
    ); /*Sets the emotions to the data fetched from the server. */
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
    ]; /*Initializes the emotions to the array of emotions. */
  };

  return (
    /*Returns the following JSX code to be rendered as HTML on the page */
    <div className="">
      <div className="justify-center items-center flex join join-vertical">
        <textarea
          className="textarea textarea-primary join-item"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <button className="btn btn-primary join-item" onClick={handlePredict}>
          Predict Emotion
        </button>
      </div>
      <div className="text-center justify-center m-8">
        <p>{status}</p>
        <p>{usrName}</p>
      </div>
      <div className="m-8 grid grid-cols-5 text-center">
        {emotions &&
          Object.entries(emotions).map(
            (
              [emotion, intensity],
              index /*Maps the emotions and their intensity to the radial-progress component. */,
            ) => (
              <div
                key={index}
                className="radial-progress m-8 text-primary"
                style={
                  {
                    "--value": intensity,
                    "--size": "5rem",
                  } as React.CSSProperties /*Sets the value and size of the radial-progress component. */
                }
              >
                {emotion} | {intensity}
              </div>
            ),
          )}
      </div>
    </div>
  );
};
