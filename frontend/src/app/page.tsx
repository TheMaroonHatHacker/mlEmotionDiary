//import Image from 'next/image'
"use client"
import { useState } from 'react';
import { UserInput }from '../components/userInput'
import { LoginSystem } from '@/components/loginSystem'



export default function Home() {
  const [usrName, setUserName] = useState(localStorage.getItem("username"));
  return (
    <main className="flex flex-col items-center justify-between p-24">
      <h1 className="text-6xl font-bold m-8">
        ML Emotion Diary
      </h1>
      <LoginSystem setter={setUserName} />


      <p className="m-8">
        Please enter some text and click the button to predict the emotion of the text.
      </p>
      <UserInput userName={usrName} />
      <p className='text-center'>
        All code is property of The Maroon Hat Hacker, if you find this.... honestly well done.
      </p>
    </main>
  )
}

