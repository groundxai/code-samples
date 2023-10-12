import sys

from groundx import Groundx, ApiException
import openai

########## CHANGE THESE ############

# GroundX API Key
# Found in your GroundX account:
# https://dashboard.groundx.ai/apikey
groundxKey = "YOUR_GROUNDX_KEY"

# GroundX Project ID, GroupID, or Bucket ID
# Found in your GroundX account
# OR by querying /project, /group, /bucket
groundxId = YOUR_ID

# OpenAI API Key
# Found in your OpenAI account:
# https://platform.openai.com/account/api-keys
openaiKey = "YOUR_OPENAI_KEY"

# OpenAI model ID (e.g. gpt-4, gpt-3.5-turbo)
openaiModel = "gpt-3.5-turbo"

# Your question
query = "YOUR QUESTION HERE"

# Number of characters of search text to include
# ~3.5 characters per token
maxInstructCharacters = 2000

######## END CHANGE THESE ##########


# Instructions sent to ChatGPT for completions
# You may want to change this
instruction = "You are a helpful virtual assistant that answers questions using the content below. Your task is to create detailed answers to the questions by combining your understanding of the world with the content provided below. Do not share links."

# Initialize the GroundX and OpenAI clients
groundx = Groundx(
    api_key=groundxKey,
)

openai.api_key = openaiKey


# Do a GroundX search
try:
    content_response = groundx.search.content(id=groundxId, search={"query": query})
    results = content_response.body["search"]
except ApiException as e:
    print("Exception when calling SearchApi.content: %s\n" % e)

# Fill the LLM context window with search results
llmText = ""
for r in results["results"]:
    if "text" in r and len(r["text"]) > 0:
        if len(llmText) + len(r["text"]) > maxInstructCharacters:
            break
        elif len(llmText) > 0:
            llmText += "\n"
        llmText += r["text"]

# Do an OpenAI completion with the search results
completion = openai.ChatCompletion.create(
    model=openaiModel,
    messages=[
        {
            "role": "system",
            "content": """%s
===
%s
===
"""
            % (instruction, llmText),
        },
        {"role": "user", "content": query},
    ],
)

if len(completion.choices) == 0:
    print("\n\n\tempty result from OpenAI for query [%s]\n\ntresult:\n\n\n" % query)
    print(completion)
    sys.exit()

print(
    "\n\nQUERY\n\n%s\n\n\nSCORE\n\n[%.2f]\n\n\nRESULT\n\n%s\n\n\n"
    % (query, results["score"], completion.choices[0].message.content)
)
