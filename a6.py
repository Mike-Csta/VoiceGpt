import openai  # for OpenAI API calls
import json
import time

start_time = time.time()

openai.api_key = "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"
openai.organization = "org-OoztSZ0bl4hd36f4gED0N8bj"
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': 'opisz historie polski?'}
    ],
    temperature=0,
    stream=True
)

collected_chunks = []
collected_messages = []
zdanie=""

for chunk in response:
    chunk_message = chunk['choices'][0]['delta']  # extract the message
    y =  json.loads(str(chunk_message))
    collected_messages.append(y)  # save the message

    if 'content' in y:
        text = y['content']
        zdanie += text  # concatenate the text

        if '.' in zdanie:
            print(zdanie)
            zdanie = ""
