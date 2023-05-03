import React, { useRef, useEffect } from 'react';
import videojs from 'video.js';
import 'video.js/dist/video-js.min.css';

const VideoComponent = ({ videoSrc, generatedText, imageResults, audioBase64, setVideoSrc }) => {
    const videoRef = useRef();

    useEffect(() => {
        if (videoRef.current && videoSrc) {
            const player = videojs(videoRef.current, {
                autoplay: true,
                controls: true,
            });

            player.src({ type: 'video/mp4', src: videoSrc });

            return () => {
                player.dispose();
            };
        }
    }, [videoSrc]);


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
            <div data-vjs-player>
                <video ref={videoRef} className="video-js" />
            </div>
            {videoSrc ? (
                <p>Video is available. Press play to watch.</p>
            ) : (
                <p>No video available.</p>
            )}
            <button onClick={handleGenerateVideo}>Create Video</button>
        </div>
    );
};

export default VideoComponent;
