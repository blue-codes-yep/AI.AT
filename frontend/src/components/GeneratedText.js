import React from 'react';

const GeneratedText = ({ generatedText }) => {
    return (
        <div className="generated-text">
            <h2>Generated Script</h2>
            <p>{generatedText.script}</p>

            <h2>Adjusted Script</h2>
            <p>{generatedText.adjust}</p>
        </div>
    );
};

export default GeneratedText;