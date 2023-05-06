import React from 'react';
import { TextField, Button, Box } from '@mui/material';

const PromptForm = ({ handleSubmit, setPrompt }) => {
    return (
        <Box my={4}>
            <form onSubmit={handleSubmit}>
                <TextField
                    label="Enter your prompt"
                    fullWidth
                    variant="outlined"
                    onChange={(e) => setPrompt(e.target.value)}
                />
                <Box mt={2}>
                    <Button variant="contained" color="primary" type="submit">
                        Submit
                    </Button>
                </Box>
            </form>
        </Box>
    );
};

export default PromptForm;
