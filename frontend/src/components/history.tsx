"use client";
import React, { useState } from "react"; /* import react JS library */

export const History = (props: { token: string | null }) => {
  /* create a function called History, defines props and their types */
  const [status, setStatus] = useState("");
  const [entries, setEntries] = useState<any>([]);
  const usrToken = props.token; /* define usrToken as the token from props */
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
    }); /* fetch the history data from the server */
    const data = await response.json();
    if (data.error) {
      /* if there is an error, set status to error */
      setStatus(data.error);
      return;
    }
    setEntries(data);
    console.log(data);
    setStatus("done");
  };
  return (
    /* return the following JSX */
    <div className="flex flex-col w-96">
      <button className="btn btn-primary" onClick={handleHistory}>
        History
      </button>
      <p>{status}</p>
      <div>
        {entries.map(
          (entry: any /* map through the entries and display them */) => (
            <div key={entry.entryID} className="collapse bg-base-100">
              <input type="radio" />
              <div className="collapse-title text-xl">{entry.timeanddate}</div>
              <div className="collapse-content">
                <p>{entry.text}</p>
              </div>
            </div>
          ),
        )}
      </div>
    </div>
  );
};
