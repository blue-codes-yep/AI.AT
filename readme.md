# AI-Powered Script Generator 🚀


This is a work-in-progress application that uses AI to generate engaging video scripts based on your input. It showcases some cool features that demonstrate the capabilities of these technologies.

![Image 1](https://i.imgur.com/U81nqHn.png)
![Image 2](https://i.imgur.com/r0nHVR6.png)

## Features

The app currently has the following features:

- Researches the topic using Google Search and SerpAPI.
- Generates a script with a custom-trained language model (based on OpenAI's GPT).
- Edits and refines the script using memory integration to make it casual and engaging.
- Finds relevant images for the script using Unsplash API.
- Synthesizes speech audio using AWS Polly.
- Creates a video using the script, images, and audio.

## Work in Progress
* Writing subtitles can take time on longer videos, Just recent I did a fresh install of windows, and upgraded from 10, to windows 11, as well as set my dev environment up this time around using wsl2 with windows, and either the fresh install, or the wsl2 (maybe combination of both) pretty much around 2.5x the speed of rendering/encoding the video, as before.

I'm working on improving the app, and there are some features and refinements that I'm planning to implement in the future. Once I'm happy with the current state of the app and it showcases a few more exciting features, I'll be moving it into a private repository to continue the development.

## How to Use

1. Install Dependencies:
   - Open the terminal or command prompt.
   - Navigate to the root folder of the project.
   - Run the following command to install the necessary Python packages:
     ```
     pip install -r requirements.txt
     ```

2. Input API Keys:
   - Open `apikey.py` and provide the following API keys (feel free to switch them up and use whatever services you prefer):
     - OpenAI API Key
     - Google API Key
     - Google CSE ID
     - SERPAPI API Key (Used for images, but currently using Unsplash)
     - AWS Access Key ID
     - AWS Secret Access Key
     - AWS Default Region
     - Unsplash Access Key
     - Unsplash Secret Key
   - Save the file after updating the API keys.

3. Run the Python Application:
   - In the terminal or command prompt, still in the root folder, run the following command:
     ```
     python app.py
     ```
   - This will start the Python application and allow you to interact with it.

4. Set Up the Frontend:
   - Open a new terminal or command prompt window.
   - Change the directory to the "frontend" folder of the project:
     ```
     cd frontend
     ```
   - Run the following command to install the required Node.js packages:
     ```
     npm install
     ```

5. Start the Frontend Server:
   - After the installation is complete, run the following command in the "frontend" folder:
     ```
     npm start
     ```
   - This will start the frontend server and make the application accessible in your web browser.

6. Start The Application:
    - After starting both the back-end, and front-end you will be able to navigate to your react app, and provide a topic to have a video genterated!
    - The app will generate a script, find relevant images, synthesize speech audio, and create a video based on the provided input.

Please note that this is a general guide, and depending on your system configuration, there might be slight variations in the commands or steps required. If you encounter any issues, feel free to reach out for assistance. Your feedback and suggestions will be invaluable as I continue to work on this project.