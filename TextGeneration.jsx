// TextGeneration.js
import React, { useState } from 'react';
import axios from 'axios';

const TextGeneration = () => {
    const [userPrompt, setUserPrompt] = useState('');
    const [aiResponse, setAiResponse] = useState('');

    const generateText = async () => {
        try {
            const response = await axios.post('http://localhost:8502/', { prompt: userPrompt });
            setAiResponse(response.data);
        } catch (error) {
            console.error('Error generating text:', error);
        }
    };

    return (
        <div>
            <h1>AI Text Generation</h1>
            <input
                type="text"
                value={userPrompt}
                onChange={(e) => setUserPrompt(e.target.value)}
            />
            <button onClick={generateText}>Generate</button>
            <div>
                <h2>AI's Response:</h2>
                <p>{aiResponse}</p>
            </div>
        </div>
    );
};

export default TextGeneration;
