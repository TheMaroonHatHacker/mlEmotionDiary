"use server"

export async function query(data:FormData){
    const userInput = data.get("input");

    if (typeof userInput !== "string"){

    }
    await fetch("http://127.0.0.1:8000/ai/query/", {
    method: "POST",
    body: data,
  });
}