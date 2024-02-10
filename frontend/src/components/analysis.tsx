"use client";
import React, { useState } from "react";
import 'chart.js/auto';
import { Chart } from 'react-chartjs-2';



export const Analysis = (props: { token: string | null }) => {
  const [status, setStatus] = useState("");
  const [chartData, setChartData] = useState<any>({
    labels: [],
    datasets: [],
  
  });
  const usrToken = props.token;
  const handleAnalysis = async () => {
    if (usrToken === null) {
      setStatus("please login to use this feature");
      return;
    }
    setStatus("loading...");
    const form = new FormData();
    form.append("token", usrToken);
    const response = await fetch(`http://127.0.0.1:8000/ai/analysis`, {
      method: "POST",
      body: form,
    });
    const data = await response.json();
    console.log(data);
    let datasets = [];
    for (let emotion in data) {
        if (emotion !== "timeframe"){
            datasets.push({
                label: emotion,
                data: data[emotion],
                fill: false,
                borderColor: "rgb(75, 192, 192)",
                tension: 0.1
            });
        }
    }
    setChartData({
        labels: data["timeframe"],
        datasets: datasets
    });
    setStatus("done");
  };
  return (
    <div className="flex flex-col w-96">
      <button className="btn btn-primary" onClick={handleAnalysis}>
        Analyze
      </button>
      <p>{status}</p>
      <div className="h-screen">
        <Chart type="line" data={chartData} />
      </div>
      
    </div>
  );
};
