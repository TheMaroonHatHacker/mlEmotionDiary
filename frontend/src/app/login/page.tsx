import Image from 'next/image'
import LoginHandler from '../loginSystem'

import dynamic from 'next/dynamic'

export default function Login() {
    return(
        <main className="flex flex-col justify-center text-center">
            <h1 className="text-6xl font-bold m-24`">
                Login
            </h1>
            <LoginHandler />
        </main>
    )
}