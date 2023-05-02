import React from 'react';

const VideoComponent = ({ videoSrc, generatedText, imageResults, audioBase64, setVideoSrc }) => {

    const fetchGeneratedVideo = async () => {
        const response = await fetch("http://localhost:5000/api/video", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                generatedText: generatedText,
                imageResults: imageResults,
                audioBase64: audioBase64,
            }),
        });

        if (response.ok) {
            const data = await response.json();
            return data.video_url;
        } else {
            throw new Error("Failed to generate video");
        }
    };

    const handleGenerateVideo = async () => {
        try {
            const videoUrl = await fetchGeneratedVideo();
            setVideoSrc(videoUrl);
        } catch (error) {
            console.error("Failed to generate video", error);
        }
    };

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
            <button onClick={handleGenerateVideo}>Create Video</button>
        </div>
    );
};

export default VideoComponent;
