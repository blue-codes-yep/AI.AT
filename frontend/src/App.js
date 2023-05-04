import React, { useState, useEffect } from 'react';
import PromptForm from './components/PromptForm';
import GeneratedText from './components/GeneratedText';
import ImageResults from './components/ImageResults';
import MessageHistory from './components/MessageHistory';
import VideoComponent from './components/VideoComponent';
import './App.css';

const App = () => {
  const [prompt, setPrompt] = useState('');
  const [generatedText, setGeneratedText] = useState({});
  const [imageResults, setImageResults] = useState([]);
  const [messageHistory, setMessageHistory] = useState([]);
  const [audioBase64, setAudioBase64] = useState('');
  const [videoSrc, setVideoSrc] = useState(null);


  const handleSubmit = async (e) => {
    e.preventDefault();
    const response1 = await fetch("http://localhost:5000/api", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt: prompt,
      }),
    });
    const data1 = await response1.json();

    setGeneratedText(data1.generated_text);
    setImageResults(data1.image_results);
    setMessageHistory(data1.message_history);

    const response3 = await fetch("http://localhost:5000/api/tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: data1.generated_text.script,
      }),
    });
    const data3 = await response3.json();

    setAudioBase64(data3.audio_base64);

    const response2 = await fetch("http://localhost:5000/api/video", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        image_results: data1.image_results,
        audioBase64: data3.audio_base64,
        generatedText: data1.generated_text,
      }),
    });
    const data2 = await response2.json();

    if (response2.ok) {
      const videoSrc = data2.video_url;
      setVideoSrc(videoSrc);
    }
  };

  return (
    <div className="App">
      <h1>Generated Text</h1>
      <PromptForm handleSubmit={handleSubmit} setPrompt={setPrompt} />
      <VideoComponent
        videoSrc={videoSrc}
        setVideoSrc={setVideoSrc}
        imageResults={imageResults}
        audioBase64={audioBase64}
        generatedText={generatedText}
      />


      {generatedText.script && (
        <GeneratedText generatedText={generatedText} handleSubmit={handleSubmit} />
      )}
      <ImageResults imageResults={imageResults} />
      <MessageHistory messageHistory={messageHistory} />

    </div>
  );
};

export default App;