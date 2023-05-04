
const PromptForm = ({ handleSubmit, setPrompt, imageResults, audioBase64, generatedText, setVid }) => {

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <input
                type="text"
                className="prompt-input"
                placeholder="Enter your prompt"
                onChange={(e) => setPrompt(e.target.value)}
                required
            />
            <button type="submit">Generate</button>
        </form>
    );
};

export default PromptForm;
