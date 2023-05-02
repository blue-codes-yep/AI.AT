import React from 'react';

const VideoComponent = ({ videoSrc }) => {
    return (
        <div>
            {videoSrc ? (
                <video controls>
                    <source src={videoSrc} type="video/mp4" />
                    Your browser does not support the video tag.
                </video>
            ) : (
                <p>No video available.</p>
            )}
        </div>
    );
};

export default VideoComponent;
