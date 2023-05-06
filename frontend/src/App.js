import React, { useState, useEffect } from 'react';
import { Container, Box, Typography } from '@mui/material';
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

    const response3 = await fetch("http://localhost:5000/api/tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: data1.generated_text.refine,
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

      // Fetch the updated message history and other necessary data
      const response4 = await fetch("http://localhost:5000/api");
      const data4 = await response4.json();
      setMessageHistory(data4.message_history);
    }
  };


  return (
    <div className="App">
      <Container maxWidth="md">
        <Box my={4}>
          <Typography variant="h3" align="center" gutterBottom>
            Generated Text
          </Typography>
          {messageHistory.length > 0 && (
            <MessageHistory messageHistory={messageHistory} />
          )}
          <PromptForm handleSubmit={handleSubmit} setPrompt={setPrompt} />
          <VideoComponent
            videoSrc={videoSrc}
            setVideoSrc={setVideoSrc}
            imageResults={imageResults}
            audioBase64={audioBase64}
            generatedText={generatedText}
          />

          {generatedText.refine && (
            <GeneratedText generatedText={generatedText} handleSubmit={handleSubmit} />
          )}
          {imageResults.length > 0 && <ImageResults imageResults={imageResults} />}
        </Box>
      </Container>
    </div>
  );
};

export default App;