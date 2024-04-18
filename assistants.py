from openai import OpenAI 
import time
import json
from adamopenailib import await_run_completion
from lunchmenu import getmenu
from config import openai_api_key, openai_assistant_id

client = OpenAI(api_key=openai_api_key)

assistant = client.beta.assistants.retrieve(
  assistant_id=openai_assistant_id
)

def message(messagecontent, threadid):
  print(messagecontent)
  thread = client.beta.threads.retrieve(threadid)
  message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=messagecontent
  )

  run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
  )

  run = await_run_completion(run, thread, client)

  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages.data[0].content[0].text.value)
  return messages.data[0].content[0].text.value

def createnewthread():
  thread = client.beta.threads.create()
  threadid = thread.id
  return threadid

def getmessagesjson(threadid, threadname):
  messages = client.beta.threads.messages.list(thread_id=threadid)
  finaljson = {"name": threadname}
  templist = []
  for message in messages.data:
    templist.append({"role": message.role, "content": message.content[0].text.value, "time": message.created_at, "id": message.id})
  templist.reverse()
  finaljson["messages"] = templist
  return finaljson