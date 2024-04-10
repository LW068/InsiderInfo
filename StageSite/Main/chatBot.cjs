// Using CommonJS require syntax
const { ChatOpenAI } = require('@langchain/openai');
const { DuckDuckGoSearch } = require('@langchain/community/tools/duckduckgo_search');
const { AgentExecutor, createOpenAIFunctionsAgent } = require('langchain/agents');
const { pull } = require('langchain/hub');
const dotenv = require('dotenv');

dotenv.config();

async function setupAndInvokeAgent(inputQuery, chatHistory) {
    console.log('setupAndInvokeAgent started with inputQuery:', inputQuery);
    const tools = [new DuckDuckGoSearch({ maxResults: 3 })];

    // Build the chat history into a prompt
    let historyPrompt = '';
    if (chatHistory) {
        // Concatenate all previous exchanges into a single string
        historyPrompt = chatHistory.map(h => `${h.sender}: ${h.message}`).join('\n');
    }

    // Append the latest user input to the chat history prompt
    const fullPrompt = `${historyPrompt}\nYou: ${inputQuery}\nAI:`;
    
    const prompt = await pull("hwchase17/openai-functions-agent");
    console.log('Prompt pulled successfully');

    const llm = new ChatOpenAI({
        apiKey: process.env.OPENAI_API_KEY,
        modelName: 'gpt-3.5-turbo',
        maxTokens: 256, // longer response
        temperature: 0,
    });
    console.log('LLM initialized');

    const agent = await createOpenAIFunctionsAgent({
        llm,
        tools,
        prompt,
    });
    console.log('Agent created successfully');
    
    const agentExecutor = new AgentExecutor({
        agent,
        tools,
    });
    console.log('AgentExecutor initialized');

    const result = await agentExecutor.invoke({
        input: fullPrompt, // Use the full prompt including history
    });
    console.log('Result received:', result);
    
    // Consider returning just the result needed
    return result;
}

setupAndInvokeAgent().catch(console.error);
module.exports = { setupAndInvokeAgent };
