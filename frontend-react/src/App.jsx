import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App(){
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSummarize = async ()=>{

    if(!text.trim()){
      setError("Please type or paste some text first!");
      return;
    }
    setError("");
    setLoading(true);
    setSummary("");

    try{
      const response = await fetch("http://127.0.0.1:5000/summarize", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text})
      });

      const data = await response.json();

      if(response.ok){
        setSummary(data.summary);
      }
      else{
        setError(data.error || "Some Error Occoured");
      }
    }
    catch{
      setError("Backend is not accessible");
    }
    finally{
      setLoading(false);
    }

  }


  return(
    <div className="app-container">
      <header className="header">
        <h1>Privacy & Policy Summarizer (Text Summarizer) AI</h1>
        <p>Paste those boring long Terms & Privacy Policies to get their instant summaries.</p>
        <p>- Designed by <b><a href='https://ashimnepal.com.np' target='_blank'>Ashim Nepal</a></b></p>
      </header>

      <div className="inpit-section">
        <textarea className="input-field" placeholder="PAste the privacy policy terms text here..." value={text} onChange={(e) => setText(e.target.value)}/>
          <button className="send-btn" onClick={handleSummarize} disabled={loading}>
            {loading ? "Summarizing..." : "Summarize"}
          </button>
          </div>


          {error && <div className="error">{error}</div>}

          {summary &&(
            <div className="output-summary">
              <h2>✨Summary</h2>
              <p>{summary}</p>
            </div>
          )}
    </div>
  );



}


export default App
