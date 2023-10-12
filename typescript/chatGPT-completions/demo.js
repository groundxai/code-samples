import { Groundx } from "groundx-typescript-sdk";
import OpenAI from 'openai';

/******* CHANGE THESE *******/

// GroundX API Key
// Found in your GroundX account:
// https://dashboard.groundx.ai/apikey
const groundxKey = "YOUR_GROUNDX_KEY";

// GroundX Project ID, GroupID, or Bucket ID
// Found in your GroundX account
// OR by querying /project, /group, /bucket
const groundxId = YOUR_ID;

// OpenAI API Key
// Found in your OpenAI account:
// https://platform.openai.com/account/api-keys
const openaiKey = "YOUR_OPENAI_KEY";

// OpenAI model ID (e.g. gpt-4, gpt-3.5-turbo)
const openaiModel = "gpt-3.5-turbo";

// Your question
const query = "YOUR QUESTION HERE";

// Number of characters of search text to include
// ~3.5 characters per token
const maxInstructCharacters = 2000;

/******* END CHANGE THESE *******/


// Instructions sent to ChatGPT for completions
// You may want to change this
const instruction = "You are a helpful virtual assistant that answers questions using the content below. Your task is to create detailed answers to the questions by combining your understanding of the world with the content provided below. Do not share links.";


// Initialize the GroundX and OpenAI clients
const groundx = new Groundx({
    apiKey: groundxKey,
});

const openai = new OpenAI({
    apiKey: openaiKey,
});


// Do a GroundX search
const result = await groundx.search.content({
    id: groundxId,
    search: {
      query: query
    },
});
if (!result || !result.status || result.status != 200 || !result.data || !result.data.search) {
    console.error(result);
    throw Error("GroundX request failed");
}

if (result.data.search.count < 1) {
    console.error("no results from search");
    console.log(result.data.search);
    throw Error("no results from GroundX search");
}

// Fill the LLM context window with search results
let llmText = "";
result.data.search.results.forEach((r) => {
    if (r["text"] && r["text"].length > 0) {
        if (llmText.length + r["text"].length > maxInstructCharacters) {
            return;
        } else if (llmText.length > 0) {
            llmText += "\n";
        }
        llmText += r["text"];
    }
});


// Do an OpenAI completion with the search results
const completion = await openai.chat.completions.create({
    model: openaiModel,
    messages: [
        {
            "role": "system",
            "content": `${instruction}
===
${llmText}
===
`
        },
        {"role": "user", "content": query},
    ],
});

if (!completion || !completion.choices || completion.choices.length == 0) {
    console.error(`\n\n\tempty result from OpenAI for query [${query}]\n\ntresult:\n\n\n`);
    console.log(completion);
    throw Error("OpenAI request failed")
}

console.log(`
    QUERY
    [${query}]
    
    SCORE
    [${result.data.search.score}]
    
    RESULT
    [${completion.choices[0].message.content}]
`);
