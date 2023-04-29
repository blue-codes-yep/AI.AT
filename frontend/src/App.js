import React, { useState, useEffect } from 'react';
import PromptForm from './components/PromptForm';
import GeneratedText from './components/GeneratedText';
import ImageResults from './components/ImageResults';
import MessageHistory from './components/MessageHistory';
import AudioPlayer from './components/AudioPlayer';
import './App.css';

const App = () => {
  const [prompt, setPrompt] = useState('');
  const [generatedText, setGeneratedText] = useState({});
  const [imageResults, setImageResults] = useState([]);
  const [messageHistory, setMessageHistory] = useState([]);
  const [audioBase64, setAudioBase64] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch("http://localhost:5000/api", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: prompt }),
    });
    const data = await response.json();

    // Update the state with the received data
    setGeneratedText(data.generated_text);
    setImageResults(data.image_results);
    setMessageHistory(data.message_history);
    setAudioBase64('');
  };

  const handleTextToSpeech = async (text) => {
    try {
      const response = await fetch("http://localhost:5000/api/tts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: text }),
      });

      if (response.ok) {
        const data = await response.json();
        setAudioBase64(data.audio_base64);
      } else {
        console.error("Failed to synthesize speech");
      }
    } catch (error) {
      console.error("Error fetching speech synthesis API", error);
    }
  };

  return (
    <div className="App">
      <h1>Generated Text</h1>
      <PromptForm handleSubmit={handleSubmit} setPrompt={setPrompt} />
      <AudioPlayer audioBase64={audioBase64} text={generatedText.script} setAudioBase64={setAudioBase64} />
      {generatedText.script && (
        <GeneratedText generatedText={generatedText} handleTextToSpeech={handleTextToSpeech} />
      )}
      <ImageResults imageResults={imageResults} />
      <MessageHistory messageHistory={messageHistory} />
    </div>
  );
};

export default App;





