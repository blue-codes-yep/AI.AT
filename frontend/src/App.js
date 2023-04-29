import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [generatedText, setGeneratedText] = useState(null);
  const [imageResults, setImageResults] = useState([]);
  const [messageHistory, setMessageHistory] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("/api", { prompt: prompt });
      setGeneratedText(response.data.generated_text);
      setImageResults(response.data.image_results);
      setMessageHistory(response.data.message_history);
    } catch (error) {
      console.error("Error calling Flask API:", error);
    }
  };

  return (
    <div className="App">
      <h1>Generated Text</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="prompt"
          placeholder="Enter your prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <input type="submit" value="Generate" />
      </form>

      {generatedText && (
        <div className="generated-text">
          <h2>Generated Script</h2>
          <p>{generatedText.script}</p>

          <h2>Adjusted Script</h2>
          <p>{generatedText.adjust}</p>
        </div>
      )}

      <div className="image-results">
        <h2>Image Results</h2>
        <ul>
          {imageResults.map((image) => (
            <li key={image.link}>
              <a href={image.link} target="_blank" rel="noreferrer">
                <img src={image.thumbnail} alt={image.title} />
              </a>
            </li>
          ))}
        </ul>
      </div>

      <div className="message-history">
        <h2>Message History</h2>
        <ul>
          {messageHistory.map((message, index) => (
            <li key={index}>
              <div>
                <strong>Script:</strong> {message.script}
              </div>
              <div>
                <strong>Adjusted:</strong> {message.adjust}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
