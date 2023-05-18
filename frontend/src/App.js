import React, { useState } from 'react';
import { Container, Box, Typography} from '@mui/material';
import PromptForm from './components/PromptForm';
import GeneratedText from './components/GeneratedText';
import ImageResults from './components/ImageResults';
import MessageHistory from './components/MessageHistory';
import VideoComponent from './components/VideoComponent';
import CustomProgressBar from './components/CustomProgressBar';
import './App.css';



const App = () => {
  const [prompt, setPrompt] = useState('');
  const [generatedText, setGeneratedText] = useState({});
  const [imageResults, setImageResults] = useState([]);
  const [messageHistory, setMessageHistory] = useState([]);
  const [audioBase64, setAudioBase64] = useState('');
  const [videoSrc, setVideoSrc] = useState(null);
  const [showSubtitles, setShowSubtitles] = useState(false);
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');
  const [taskProgress, setTaskProgress] = useState(0); // New state for task progress

  const toggleSubtitles = () => {
    setShowSubtitles(!showSubtitles);
  };

  const startCheckingStatus = async (taskId) => {
    console.log('Starting to check status for task:', taskId);
    setLoading(true);
    setStatusMessage('Processing video...');
    const response = await fetch(`http://localhost:5000/api/status/${taskId}`);
    const data = await response.json();
    console.log('Response from /api/status:', data);
    if (data.state === 'PENDING' || data.state === 'PROGRESS') {
      setTaskProgress(data.current / data.total); // Update task progress
      setTimeout(() => startCheckingStatus(taskId), 1000);
    } else if (data.state === 'SUCCESS') {
      setVideoSrc(data.result);
      setLoading(false);
      setStatusMessage('Video processed successfully!');
      setTaskProgress(0); // Reset task progress
    } else {
      console.error('Task failed');
      setLoading(false);
      setStatusMessage('Error processing video.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Show subtitles:", showSubtitles);

    const response = await fetch("http://localhost:5000/api/start", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt: prompt,
      }),
    });

    const data = await response.json();

    // Start checking the task status
    console.log('Task ID:', data.task_id);
    startCheckingStatus(data.task_id);
  };

  return (
    <div className="App">
      <Container maxWidth="md">
        <Box my={4}>
          <Typography variant="h3" align="center" gutterBottom>
            Script Topic 📜
          </Typography>
          {messageHistory.length > 0 && (
            <MessageHistory messageHistory={messageHistory} />
          )}
          <PromptForm
            handleSubmit={handleSubmit}
            setPrompt={setPrompt}
            showSubtitles={showSubtitles}
            toggleSubtitles={toggleSubtitles}
            startCheckingStatus={startCheckingStatus}
          />
          <VideoComponent
            videoSrc={videoSrc}
            setVideoSrc={setVideoSrc}
            imageResults={imageResults}
            audioBase64={audioBase64}
            generatedText={generatedText}
          />
          {loading && <div className="spinner"></div>}
          <div>{statusMessage}</div>
          <CustomProgressBar progress={taskProgress * 100} />
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