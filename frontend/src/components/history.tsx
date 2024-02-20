"use client";
import React, { useState } from "react";

export const History = (props: { token: string | null }) => {
  const [status, setStatus] = useState("");
  const [entries, setEntries] = useState<any>([]);
  const usrToken = props.token;
  const handleHistory = async () => {
    if (usrToken === null) {
      setStatus("please login to use this feature");
      return;
    }
    setStatus("loading...");
    const form = new FormData();
    form.append("token", usrToken);
    const response = await fetch(`http://127.0.0.1:8000/ai/history`, {
      method: "POST",
      body: form,
    });
    const data = await response.json();
    setEntries(data);
    console.log(data);
    setStatus("done");
  };
  return (
    <div className="flex flex-col w-96">
      <button className="btn btn-primary" onClick={handleHistory}>
        History
      </button>
      <p>{status}</p>
      <div>
        {entries.map((entry: any) => (
          <div key={entry.entryID} className="collapse bg-base-100">
            <input type="radio" />
            <div className="collapse-title text-xl">{entry.timeanddate}</div>
            <div className="collapse-content">
              <p>{entry.text}</p>
            </div>
          </div>
        ))
        }
      </div>
    </div>
  );
};
