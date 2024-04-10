const express = require('express');
const { readFile } = require('fs').promises;
const { exec } = require('child_process');
const bodyParser = require('body-parser');
const dotenv = require('dotenv');
const path = require('path');
const { setupAndInvokeAgent } = require('./Main/chatBot.cjs');

dotenv.config();
const app = express();

// Serve static files from the 'Main' directory
app.use(express.static('Main'));

// Use bodyParser middleware to parse JSON bodies
app.use(bodyParser.json());

// Define the route for serving the main web application
app.get('/', async (request, response) => {
    response.send(await readFile('./Main/index.html', 'utf8'));
});

// Define the route for serving the Dash app HTML with iframe (if needed)
app.get('/dash', async (request, response) => {
    const iframeHTML = ``; // iframe content here
    response.send(iframeHTML);
});

let chatHistory = []; // This will hold the conversation history for the chatbot

// Define a route for POST requests to '/query' for the chatbot
app.post('/query', async (req, res) => {
    const { input } = req.body;
    try {
        chatHistory.push({ sender: 'user', message: input }); // Add user input to history
        const result = await setupAndInvokeAgent(input, chatHistory); // Pass history to the function
        chatHistory.push({ sender: 'bot', message: result.output }); // Add bot response to history
        res.json({ message: result.output, chatHistory }); // Return the chat history along with the message
    } catch (error) {
        console.error('Error handling chat query:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Execute the Python script if needed
exec('python3 Main/colantest.py', (error, stdout, stderr) => {
    if (error) {
        console.error(`Error executing colantest.py: ${error}`);
        return;
    }
    console.log(`colantest.py stdout: ${stdout}`);
    console.error(`colantest.py stderr: ${stderr}`);
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
