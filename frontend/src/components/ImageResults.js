import React from 'react';

const ImageResults = ({ imageResults }) => {
    return (
        <div className="image-results">
            <h2>Image Results</h2>
            <ul>
                {imageResults.map((imageUrl, index) => (
                    <li key={index}>
                        <a href={imageUrl} target="_blank" rel="noopener noreferrer">
                            <img src={imageUrl} alt={`Image ${index + 1}`} />
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ImageResults;
