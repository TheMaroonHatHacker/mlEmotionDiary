//import Image from 'next/image'
import UserInput from './userInput'


export default function Home() {
  return (
    <main className="flex flex-col items-center justify-between p-24">
      <h1 className="text-6xl font-bold m-8">
        ML Emotion Diary
      </h1>



      <p className="m-8">
        Please enter some text and click the button to predict the emotion of the text.
      </p>
      <UserInput />
      <p className='text-center'>
        All code is property of The Maroon Hat Hacker, if you find this.... honestly well done.
      </p>
    </main>
  )
}

