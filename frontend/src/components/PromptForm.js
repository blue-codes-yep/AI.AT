import React from 'react';
import { TextField, Button, Box } from '@mui/material';
import { FormControlLabel, Checkbox } from '@mui/material';

const PromptForm = ({ handleSubmit, setPrompt, showSubtitles, toggleSubtitles }) => {
    return (
        <Box my={4}>
            <form onSubmit={handleSubmit}>
                <TextField
                    label="Enter a topic"
                    fullWidth
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
                </div>
            </form>
        </Box>
    );
};

export default PromptForm;
