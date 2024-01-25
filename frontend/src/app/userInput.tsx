
'use client'
import React, { useState } from 'react';


export default function MyComponent() {
    const [inputText, setInputText] = useState('');
    const [mainEmotion, setMainEmotion] = useState('');
    const [anger, setAnger] = useState(0);
    const [boredom, setBoredom] = useState(0);
    const [empty, setEmpty] = useState(0);
    const [enthusiasm, setEnthusiam] = useState(0);
    const [fun, setFun] = useState(0);
    const [happiness, setHappiness] = useState(0);
    const [hate, setHate] = useState(0);
    const [love, setLove] = useState(0);
    const [neutral, setNeutral] = useState(0);
    const [relief, setRelief] = useState(0);
    const [sadness, setSadness] = useState(0);
    const [suprise, setSuprise] = useState(0);
    const [worry, setWorry] = useState(0);
    const usrName = localStorage.getItem('username'); 
    console.log(usrName);
    const handleClick = async () => {
        if (inputText === '') {
            setMainEmotion('please enter some text');
        } else {
            const response = await fetch(`http://127.0.0.1:8000/predict/${usrName}/${inputText}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            
        });
        const data = await response.json();
        
        console.log(data);
        setMainEmotion(data['main-emotion']);
        setAnger(data['anger']);
        setBoredom(data['boredom']);
        setEmpty(data['empty']);
        setEnthusiam(data['enthusiasm']);
        setFun(data['fun']);
        setHappiness(data['happiness']);
        setHate(data['hate']);
        setLove(data['love']);
        setNeutral(data['neutral']);
        setRelief(data['relief']);
        setSadness(data['sadness']);
        setSuprise(data['suprise']);
        setWorry(data['worry']);
        
        }
        
    }

    return (
        <div className="text-center">
            
            <div className="text-center flex">
            <h1 className="text-2xl">Welcome {usrName}</h1>
            <div className="join m-8">
            <textarea className="textarea textarea-primary w-full max-w-xs m-8" type="text" value={inputText} onChange={(e) => setInputText(e.target.value)} />
            <button className="btn btn-primary m-8" onClick={handleClick}>Predict Emotion</button>
            </div>
            
           
            </div>
            <div className="text-center justify-center m-8">
                <p>{mainEmotion}</p>
            </div>
            

            <div className="m-8 grid grid-cols-5 text-center">
            <div className="radial-progress m-8 text-primary" style={{"--value":anger}}>Anger</div>
            <div className="radial-progress m-8 text-secondary" style={{"--value":boredom}}>Boredom</div>
            <div className="radial-progress m-8 text-accent" style={{"--value":empty}}>Empty</div>
            <div className="radial-progress m-8 text-neutral" style={{"--value":enthusiasm}}>Enthusiasm</div>
            <div className="radial-progress m-8 text-base-100" style={{"--value":fun}}>Fun</div>
            <div className="radial-progress m-8 text-info" style={{"--value":happiness}}>Happiness</div>
            <div className="radial-progress m-8 text-success" style={{"--value":hate}}>Hate</div>
            <div className="radial-progress m-8 text-warning" style={{"--value":love}}>Love</div>
            <div className="radial-progress m-8 text-error" style={{"--value":neutral}}>Neutral</div>
            <div className="radial-progress m-8 text-primary" style={{"--value":relief}}>Relief</div>
            <div className="radial-progress m-8 text-secondary" style={{"--value":sadness}}>Sadness</div>
            <div className="radial-progress m-8 text-accent" style={{"--value":suprise}}>Suprise</div>
            <div className="radial-progress m-8 text-neutral" style={{"--value":worry}}>Worry</div>
            </div>      

            </div>
              
    );
}
