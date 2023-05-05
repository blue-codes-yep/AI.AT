import React from 'react';

const GeneratedText = ({ generatedText }) => {
    return (
        <div className="generated-text">
            <h2>Generated Script</h2>
            <p>{generatedText.refine}</p>
        </div>
    );
};

export default GeneratedText;