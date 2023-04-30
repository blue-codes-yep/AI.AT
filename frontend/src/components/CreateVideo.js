import React from "react";

const createVideo = async (imageResults, audioBase64, generatedText) => {
    try {
        const response = await fetch("http://localhost:5000/api/video", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ imageResults, audioBase64, generatedText }),
        });

        if (response.ok) {
            const data = await response.json();
            // Do something with the received video_base64
            console.log(data.video_base64);
        } else {
            console.error("Failed to create video");
        }
    } catch (error) {
        console.error("Error fetching video creation API", error);
    }
};

export default createVideo;