import openai  # for OpenAI API calls
import time  # for measuring time duration of API calls# Example of an OpenAI ChatCompletion request
# https://platform.openai.com/docs/guides/chat

# record the time before the request is sent
start_time = time.time()

# send a ChatCompletion request to count to 100
start_time = time.time()

# send a ChatCompletion request to count to 100
openai.api_key = "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"
openai.organization = "org-OoztSZ0bl4hd36f4gED0N8bj"
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': 'co sądzisz o polsce?'}
    ],
    temperature=0,
    stream=True  # again, we set stream=True
)

# create variables to collect the stream of chunks
collected_chunks = []
collected_messages = []
# iterate through the stream of events
for chunk in response:
    # chunk_time = time.time() - start_time  # calculate the time delay of the chunk
    # collected_chunks.append(chunk)  # save the event response
    chunk_message = chunk['choices'][0]['delta']  # extract the message
    collected_messages.append(chunk_message)  # save the message

    print(f"seconds after request: {chunk_message}")  # print the delay and text

# # print the time delay and text received
# print(f"Full response received {chunk_time:.2f} seconds after request")
# full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
# print(f"Full conversation received: {full_reply_content}")