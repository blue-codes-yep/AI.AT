import React from 'react';

const GeneratedText = ({ generatedText }) => {
    return (
        <div>
            <h2>Generated Text</h2>
            <p>{generatedText.refined_script}</p>
        </div>
    );
};

export default GeneratedText;