import React, { useState, useEffect, useRef } from 'react';

const AudioPlayer = ({ audioBase64, text, setAudioBase64 }) => {
    const [isPlaying, setIsPlaying] = useState(false);
    const audioRef = useRef(new Audio());

    useEffect(() => {
        if (isPlaying) {
            audioRef.current.play();
        } else {
            audioRef.current.pause();
            audioRef.current.currentTime = 0;
        }
    }, [isPlaying]);

    const handlePlayPause = () => {
        setIsPlaying(!isPlaying);
    };

    const handleTextToSpeech = async () => {
        try {
            const response = await fetch("http://localhost:5000/api/tts", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ text: text }),
            });

            if (response.ok) {
                const data = await response.json();
                setAudioBase64(data.audio_base64);
            } else {
                console.error("Failed to synthesize speech");
            }
        } catch (error) {
            console.error("Error fetching speech synthesis API", error);
        }
    };

    return (
        <div className="audio-player">
            <button onClick={handlePlayPause}>{isPlaying ? 'Pause' : 'Play'}</button>
            {audioBase64 && (
                <audio
                    ref={audioRef}
                    src={`data:audio/wav;base64,${audioBase64}`}
                    onEnded={() => setIsPlaying(false)}
                />
            )}
            {!audioBase64 && (
                <button onClick={handleTextToSpeech} disabled={!text}>
                    Generate Audio
                </button>
            )}
        </div>
    );
};


export default AudioPlayer;
