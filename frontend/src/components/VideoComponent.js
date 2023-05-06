import React, { useRef, useEffect } from 'react';
import videojs from 'video.js';
import 'video.js/dist/video-js.min.css';
import { Box } from '@mui/material';

const VideoComponent = ({ videoSrc, setVideoSrc, imageResults, audioBase64, generatedText }) => {
    const videoRef = useRef();

    useEffect(() => {
        if (videoRef.current && videoSrc) {
            const player = videojs(videoRef.current, {
                autoplay: false,
                controls: true,
            });

            player.src({ type: 'video/mp4', src: videoSrc });

            return () => {
                player.dispose();
            };
        }
    }, [videoSrc]);

    return (
        <Box display="flex" alignItems="center" justifyContent="center" flexDirection="column">
            <div data-vjs-player>
                <video ref={videoRef} className="video-js" />
            </div>
            {videoSrc ? (
                <p>Video is available. Press play to watch.</p>
            ) : (
                <p>No video available.</p>
            )}
        </Box>
    );
};

export default VideoComponent;
