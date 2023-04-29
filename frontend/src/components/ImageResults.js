import React from 'react';

const ImageResults = ({ imageResults }) => {
    return (
        <div className="image-results">
            <h2>Image Results</h2>
            <ul>
                {imageResults.map((image, index) => (
                    <li key={index}>
                        <a href={image.link} target="_blank" rel="noopener noreferrer">
                            <img src={image.thumbnail} alt={image.title} />
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ImageResults;