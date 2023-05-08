import React, { useState } from 'react';
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
  const [showSubtitles, setShowSubtitles] = useState(false);

  const toggleSubtitles = () => {
    setShowSubtitles(!showSubtitles);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Show subtitles:", showSubtitles);
    const initialApiResponse = await fetch("http://localhost:5000/api", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt: prompt,
      }),
    });
    const initialApiData = await initialApiResponse.json();

    setGeneratedText(initialApiData.generated_text);
    setImageResults(initialApiData.image_results);

    const ttsResponse = await fetch("http://localhost:5000/api/tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: initialApiData.generated_text.refine,
      }),
    });
    const ttsData = await ttsResponse.json();

    setAudioBase64(ttsData.audio_base64);

    const videoResponse = await fetch("http://localhost:5000/api/video", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        image_results: initialApiData.image_results,
        audioBase64: ttsData.audio_base64,
        generatedText: initialApiData.generated_text,
        showSubtitles: showSubtitles,
      }),
    });
    const videoData = await videoResponse.json();

    if (videoResponse.ok) {
      const videoSrc = videoData.video_url;
      setVideoSrc(videoSrc);

      // Fetch the updated message history and other necessary data
      const updatedApiResponse = await fetch("http://localhost:5000/api");
      const updatedApiData = await updatedApiResponse.json();
      setMessageHistory(updatedApiData.message_history);
    }
  };

  return (
    <div className="App">
      <Container maxWidth="md">
        <Box my={4}>
          <Typography variant="h3" align="center" gutterBottom>
            Input script topic
          </Typography>
          {messageHistory.length > 0 && (
            <MessageHistory messageHistory={messageHistory} />
          )}
          <PromptForm
            handleSubmit={handleSubmit}
            setPrompt={setPrompt}
            showSubtitles={showSubtitles}
            toggleSubtitles={toggleSubtitles}
          />
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