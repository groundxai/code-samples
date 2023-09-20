import json, sys

import openai
import requests


########## CHANGE THESE ############

# GroundX API Key
# Found in your GroundX account:
# https://dashboard.groundx.ai/apikey
groundxKey = "YOUR_GROUNDX_KEY"

# GroundX Project ID
# Found in your GroundX account OR by querying /project
# https://dashboard.groundx.ai/projects
groundxProjectId = PROJECT_ID

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


groundxVersion = "v1"
groundxBaseUrl = "https://api.groundx.ai/api/%s" % groundxVersion

openai.api_key = openaiKey

searchResult = requests.post(
    groundxBaseUrl + "/search/%d" % groundxProjectId,
    headers={
        "Content-Type": "application/json",
        "X-API-Key": groundxKey,
    },
    data=json.dumps(
        {
            "search": {
                "query": query,
            }
        }
    ),
)

if searchResult.status_code != 200:
    print(
        "\n\n\treceived status [%d] with message [%s]\n\n\n"
        % (searchResult.status_code, searchResult.text)
    )
    sys.exit()

searchData = json.loads(searchResult.text)

if "search" not in searchData or "results" not in searchData["search"]:
    print(
        "\n\n\tempty result for query [%s]\n\n\tresult:\n\n%s\n\n\n"
        % (query, searchResult.text)
    )
    sys.exit()

llmText = ""
for resl in searchData["search"]["results"]:
    if "text" in resl and len(resl["text"]) > 0:
        if len(llmText) + len(resl["text"]) > maxInstructCharacters:
            break
        elif len(llmText) > 0:
            llmText += "\n"
        llmText += resl["text"]

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
    print("\n\n\tempty result from OpenAI for query [%s]\n\ntresult:\n\n\ns" % query)
    print(completion)
    sys.exit()

print(
    "\n\nQUERY\n\n%s\n\n\nSCORE\n\n[%.2f]\n\nRESULT\n\n%s\n\n\n"
    % (query, searchData["search"]["score"], completion.choices[0].message.content)
)
