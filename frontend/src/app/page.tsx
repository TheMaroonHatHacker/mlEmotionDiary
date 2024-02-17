"use client"
import { useState } from 'react';
import { UserInput } from '@/components/userInput'
import { LoginSystem } from '@/components/loginSystem'
import { Analysis } from '@/components/analysis'

export default function Home() {
  const [usrName, setUserName] = useState<string | null>(typeof localStorage !== 'undefined' ? localStorage.getItem('username') : "");
  const [token, setToken] = useState<string | null>(typeof localStorage !== 'undefined' ? localStorage.getItem('token') : "");
  return (
    <main className="flex flex-col items-center justify-between p-24">
      <h1 className="text-6xl font-bold m-8">
        ML Emotion Diary
      </h1>
      <LoginSystem setter={setUserName} tokenSetter={setToken} />


      <p className="m-8">
        Please enter some text and click the button to predict the emotion of the text.
      </p>
      <UserInput userName={usrName} token={token} />
      <Analysis token={token} />
    </main>
  )
}

