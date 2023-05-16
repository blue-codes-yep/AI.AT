import React, { useState } from 'react';
import { TextField, Button, Box } from '@mui/material';
import { FormControlLabel, Checkbox } from '@mui/material';
import axios from 'axios';

const PromptForm = ({ handleSubmit, setPrompt, showSubtitles, toggleSubtitles }) => {
    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [statusMessage, setStatusMessage] = useState('');

    const startTask = async (e) => {
        e.preventDefault();
        setLoading(true);
        const res = await axios.get('http://localhost:5000/start-task');
        const taskId = res.data.task_id;
        getStatus(taskId);
    }
    
    const getStatus = async (taskId) => {
        const res = await axios.get(`http://localhost:5000/task-status/${taskId}`);
        if (res.data.state === 'PROGRESS') {
            setProgress(res.data.current / res.data.total);
            setStatusMessage('Task in progress...');
            setTimeout(() => getStatus(taskId), 1000);
        } else if (res.data.state === 'SUCCESS') {
            setLoading(false);
            setProgress(1);
            setStatusMessage('Task completed!');
        } else {
            setLoading(false);
            setStatusMessage('Task failed. Please try again.');
        }
    }

    return (
        <Box my={4}>
            <form onSubmit={handleSubmit}>
                <TextField
                    label="Enter a topic"
                    fullWidth
                    defaultValue={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                />
                <div className="GenterateVideo">
                    <Box mt={2}>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={showSubtitles}
                                    onChange={toggleSubtitles}
                                    color="primary"
                                />
                            }
                            label="Show subtitles"
                        />
                    </Box>
                    <Box mt={2}>
                        <Button variant="contained" color="primary" type="submit">
                            Generate video
                        </Button>
                    </Box>
                    {loading && <div className="spinner"></div>}
                    <progress value={progress} max="1" />
                    <div>{statusMessage}</div>
                </div>
            </form>
        </Box>
    );
};

export default PromptForm;
