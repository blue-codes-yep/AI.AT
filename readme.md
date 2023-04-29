# Work-in-Progress: AI-Powered YouTube Script Generator 🚧

Welcome to the AI-Powered YouTube Script Generator project! This web application uses cool AI technology to create captivating and informative YouTube video scripts based on user inputs 😎.

The app takes input, creates a script, generates images, allows you to generate text-to-speech audio and play it, and we're working on adding video creation with the script, images, and text-to-speech audio. While the project is still under development, it has already shown promising results.
Demo Web-App

![Demo GIF](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTRiYjM2NzUzZDUxODg3NWZjNzJmNmFjZTgwMzViMTZiMjMxYzAwNSZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/WGXSVm4WdEYsqLGjb8/giphy.gif)

Takes input, Creates Script, and Generates Images, allows you to generate text-to-speech, audio and play it, and soon to create a video with the script and images, and text-to-speech audio.

## Introduction

Given a user's input (a topic or keyword), the application generates a YouTube video script through these steps:

- Research the topic using Google Search and SerpAPI.
- Generate a script with a custom-trained language model (based on OpenAI's GPT).
- Edit and refine the script with a casual and engaging tone.
- Acquire relevant images for the script using Google Images and SerpAPI.
- Generate text-to-speech audio for the script and allow playback.

We are also working on adding the ability to create a video using the generated script, images, and text-to-speech audio.

Built with Flask (backend), React (frontend), and other cool libraries, the application is designed to be user-friendly 🎉.

## Frontend Tech Stack 🛠

Using React for the frontend to make the app responsive and enjoyable to use. Here's a quick overview of our frontend dependencies currently:

- React: ^18.2.0
- React-DOM: ^18.2.0
- Axios: ^1.4.0
- And some testing libraries to keep our code reliable

The frontend also includes some handy scripts, such as "start" to run the development server, "build" to create the production build, "test" for running tests, and "eject" to customize the configuration (use with caution 😅).

## Key Features

- AI-powered script creation: The app harnesses a potent language model to generate compelling and informative scripts for a wide array of topics 🧠.
- Integrated research: The app incorporates Google Search results to ensure up-to-date and pertinent information for the produced script 🌐.
- Image acquisition: The app employs SerpAPI to obtain relevant images from Google Images, augmenting the script's visual appeal 🖼.
- Text-to-speech audio: The app generates audio from the script using text-to-speech technology, allowing you to play the audio and get a feel for the final voiceover 🔊.
- User-friendly design: The app is designed for ease of use, featuring a straightforward input prompt and clear presentation of generated results 😊.

## Upcoming Enhancements

Plan to continuously improve the project by adding new features and optimizing existing components. Some of our planned updates include:

- Image collection and manipulation: We intend to develop a mechanism to gather and process images for videos, using image search APIs like Google Images or Bing Image Search, as well as image processing libraries such as OpenCV or PIL 📸.

- Text generation with GPT-4: We aim to create a module that interfaces with the GPT-4 API for voiceover text generation, utilizing user input or pre-defined templates to produce high-quality scripts 📝.

- Text-to-speech using Google's Poly API: We plan to build a module that leverages Google's Poly API to convert generated text into audio files, offering options for caching, voice customization, and speed adjustments to improve voiceover quality 🔊.

- Video production: We will use video editing libraries like MoviePy or FFmpeg to merge generated images and voiceovers into a cohesive video, providing options for effects, transitions, and captions to create visually engaging content 🎥.

- User interface enhancement: We will concentrate on crafting a user-friendly interface for the app, utilizing web frameworks such as Flask or Django for web-based applications, or GUI libraries like Tkinter or PyQt for desktop applications to create an intuitive and interactive experience 🌟.
