import React from 'react';

const PromptForm = ({ handleSubmit, setPrompt }) => {
    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Enter your prompt"
                onChange={(e) => setPrompt(e.target.value)}
            />
            <input type="submit" value="Generate" />
        </form>
    );
};

export default PromptForm;