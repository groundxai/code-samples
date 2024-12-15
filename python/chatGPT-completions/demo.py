import os
import sys
from groundx import GroundX
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

if os.getenv("GROUNDX_API_KEY") is None:
    raise Exception("environment variable GROUNDX_API_KEY is not set")
if os.getenv("OPENAI_API_KEY") is None:
    raise Exception("environment variable OPENAI_API_KEY is not set")

opts = {
    # Your question
    "query": "Transformer",

    # GroundX Project ID or Bucket ID
    # Found in your GroundX account
    # OR by querying /project, /bucket
    "id": 13403,

    # Instructions sent to ChatGPT for completions
    # You may want to change this
    "instruction": "You are a helpful virtual assistant that answers questions using the content below. Your task is to create detailed answers to the questions by combining your understanding of the world with the content provided below. Do not share links.",

    # OpenAI model
    "openai_model": "gpt-4o-mini"
}

# Initialize the GroundX and OpenAI clients
groundx = GroundX(api_key=os.getenv("GROUNDX_API_KEY"))
openai = OpenAI()

# Do a GroundX search
try:
    content_response = groundx.search.content(id=opts["id"], query=opts["query"])
    results = content_response.search
except Exception as e:
    raise Exception("Exception when calling SearchApi.content: %s\n" % e)

# Access our suggested retrieved context
llmText = results.text
if llmText == "":
    raise Exception("\n\n\tYour search returned an empty result\n")

# Do an OpenAI generation with the retrieved context
completion = openai.chat.completions.create(
    model=opts["openai_model"],
    messages=[
        {
            "role": "system",
            "content": """%s
===
%s
===
"""
            % (opts["instruction"], llmText),
        },
        {"role": "user", "content": opts["query"]},
    ],
)

if len(completion.choices) == 0:
    print("\n\n\tempty result from OpenAI for query [%s]\n\ntresult:\n\n\n" % opts["query"])
    print(completion)
    sys.exit()

print(
    "\n\nQUERY\n\n%s\n\n\nSCORE\n\n[%.2f]\n\n\nRESULT\n\n%s\n\n\n"
    % (opts["query"], results.score, completion.choices[0].message.content)
)
