# (( Still WIP placeholder readme ))

# AI-Driven YouTube Script Creator

This project is an AI-driven web application for generating YouTube video scripts based on user input. The application leverages state-of-the-art language models and multiple APIs to create engaging and informative scripts for various topics. It is currently in development but has already demonstrated promising results.

## Overview

The application takes a user's input (a topic or a keyword) and generates a YouTube video script by performing the following steps:

1. Research the topic using Google Search and SerpAPI.
2. Generate a script using a custom-trained language model (based on OpenAI's GPT).
3. Edit and adjust the script in a fun and relaxed way.
4. Retrieve relevant images for the script using Google Images and SerpAPI.

The application is built using Flask, a lightweight Python web framework. It also employs various libraries, such as `langchain` for interacting with the language model and `serpapi` for working with Google Search and Google Images APIs.

## Features

- AI-driven script generation: The application uses a powerful language model to create engaging and informative scripts for a wide range of topics.
- Research integration: The app integrates Google Search results to provide up-to-date and relevant information for the generated script.
- Image retrieval: The application uses SerpAPI to fetch relevant images from Google Images, enhancing the final script's visual appeal.
- User-friendly interface: The application is designed to be easy to use, with a simple input prompt and a clear display of generated results.

## Future Development

As the project progresses, we plan to add more features and fine-tune each component of the application. Some of the planned improvements include:

- Image collection and processing: We will implement a mechanism to collect and process images for the video. This may involve using image search APIs, such as Google Images or Bing Image Search, to find relevant images based on user input. We will also consider incorporating image processing libraries like OpenCV or PIL to resize or manipulate the images.

- Text generation with GPT-4: We aim to develop a module that communicates with the GPT-4 API to generate the text for the voiceover. This module will take user input or predefined templates and generate high-quality scripts using the advanced capabilities of the language model.

- Text-to-speech with Google's Poly API: Another planned module will utilize Google's Poly API to convert the generated text into audio files. We will explore options to cache the audio files for future use and allow users to customize the voice type and speed to enhance the overall quality of the voiceover.

- Video creation: We will leverage video editing libraries such as MoviePy or FFmpeg to combine the generated images and voiceover into a cohesive video. This module will provide options to add effects, transitions, or captions to create visually appealing and engaging videos.

- User interface: We will focus on designing a user-friendly interface for the application. Depending on the application type (web-based or desktop), we will use web frameworks like Flask or Django or GUI libraries like Tkinter or PyQt to create an intuitive and interactive interface that enhances the user experience.

We are excited about the potential of this project and look forward to implementing these features to create a robust and user-friendly AI-driven YouTube script creator.
