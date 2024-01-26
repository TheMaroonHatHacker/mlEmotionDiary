'use client'
import React, { useState } from 'react';
import dynamic from 'next/dynamic';

const LoginSystem: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleUsernameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);
  };

  const handleLogin = async  () => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const response =  await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    console.log(data['auth']);
    if(data['auth'] == 'true'){
      (window as any).localStorage.setItem('username', username);

    }
    
  };
  const handleRegister = async () => {
    const response = await fetch(`http://127.0.0.1:8000/create/${username}/${password}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
          });
  };

  return (
    <div className='flex flex-col w-96'>
      <input className="input input-bordered" type="text" value={username} onChange={handleUsernameChange} placeholder="Username" />
      <input className="input input-bordered" type="password" value={password} onChange={handlePasswordChange} placeholder="Password" />
      <button className="btn" onClick={handleLogin}>Login</button>
      <button className="btn" onClick={handleRegister}>Create</button>
    </div>
  );
};

const DynamicComponentWithNoSSR = dynamic(() => Promise.resolve(LoginSystem), { ssr: false });

export default function LoginHandler() {
  return <DynamicComponentWithNoSSR />;
}
