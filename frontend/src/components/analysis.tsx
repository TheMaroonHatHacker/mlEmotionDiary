"use client"; /* Tells nextJS this is a client component, and should be rendered client-side */
import React, { useState } from "react";
import "chart.js/auto";
import { Chart } from "react-chartjs-2";

/* imports all the libraries needed (react, Chart.js, and react-chartjs used for rendering the chart as a react component) */

export const Analysis = (props: { token: string | null }) => {
  /* Analysis component takes a token as a prop */
  const [status, setStatus] = useState("");
  const [chartData, setChartData] = useState<any>({
    /* initialising chartData and it's respective setter functions. We give it "values" just to prevent it from being null*/
    labels: [],
    datasets: [],
  });
  const usrToken = props.token; /* setting the token to a variable */
  function generateRandomColourRGB() {
    /* Function to generate a random colour */
    const r = Math.floor(Math.random() * 256); /* Generating a random number */
    const g = Math.floor(Math.random() * 256); /* Generating a random number */
    const b = Math.floor(Math.random() * 256); /* Generating a random number */
    return `rgb(${r}, ${g}, ${b})`; /* Returning the random colour */
  }
  const handleAnalysis = async () => {
    /* Requests user data using the API, then adds the data received to the chartData variable used to display data on the chart*/
    if (usrToken === null) {
      /* If the user is not logged in, it will display a message to the user */
      setStatus("please login to use this feature");
      return;
    }
    setStatus("loading...");
    const form =
      new FormData(); /* Creating a new form to send the token to the server */
    form.append("token", usrToken); /* Appending the token to the form */
    const response = await fetch(`http://127.0.0.1:8000/ai/analysis`, {
      /* Fetching the data from the server */ method: "POST",
      body: form,
    });
    const data =
      await response.json(); /* Parsing the data received from the server */
    let datasets = []; /* Creating a new array to store the data */
    for (let item in data) {
      /* Looping through the data received from the server */
      if (item !== "timeframe") {
        /* If the item is not the timeframe, it will add the data to the datasets array */

        datasets.push({
          /* Pushing the data to the datasets array */ label: item,
          data: data[item],
          fill: false,
          borderColor: generateRandomColourRGB(),
          tension: 0.1,
        });
      }
    }
    setChartData({
      /* Setting the chartData to the data received from the server */
      labels: data["timeframe"],
      datasets: datasets,
    });
    setStatus("done");
  };
  return (
    <div className="flex flex-col w-96">
      <button className="btn btn-primary" onClick={handleAnalysis}>
        Analyze
      </button>
      <p>{status}</p>
      <div
        className="h-screen"
        style={{
          height: "50vh",
          position: "relative",
          marginBottom: "1%",
          padding: "1%",
        }}
      >
        <Chart
          type="line"
          data={chartData}
          options={{ maintainAspectRatio: false }}
        />
      </div>
    </div>
  );
};
