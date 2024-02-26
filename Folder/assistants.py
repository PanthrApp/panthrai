from openai import OpenAI 
import assistantsfunctions
import time
import json
from adamopenailib import await_run_completion
from lunchmenu import getmenu

client = OpenAI()
# from main import assistant

assistant = client.beta.assistants.retrieve(
  assistant_id="asst_qDS5qAI2qmbD6dV4xwyXSwiw"
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

  # messagesclean = []
  # for message in messages.data:
  #   print(message.role)
  #   messagesclean.append(message.content[0].text.value)

  # return messagesclean

# thread = client.beta.threads.create()
threadid = "thread_HsvyQDiN4QM0KvFh9hApNnlX"

def askquestion(messagecontent, threadid):
  return message(messagecontent, threadid)[0]

def createnewthread():
  thread = client.beta.threads.create()
  threadid = thread.id
  return threadid

def getmessages(threadid):
  messages = client.beta.threads.messages.list(thread_id=threadid)
  messagesclean = []
  for message in messages.data:
    messagesclean.append(message.content[0].text.value)
  return messagesclean

def getmessagesjson(threadid):
  messages = client.beta.threads.messages.list(thread_id=threadid)
  finaljson = {}
  templist = []
  for message in messages.data:
    templist.append({"role": message.role, "content": message.content[0].text.value, "time": message.created_at, "id": message.id})
  templist.reverse()
  finaljson["messages"] = templist
  return finaljson

def getrawmessages(threadid):
  messages = client.beta.threads.messages.list(thread_id=threadid)
  return messages

def convertunix(unix):
  timeconverted = time.strftime('%m/%d/%Y', time.localtime(unix))
  temptime = time.strftime('%H', time.localtime(unix))
  pmtime = False
  if int(temptime) > 12:
    temptime = str(int(temptime) - 12)
    pmtime = True
  if pmtime:
    timeconverted += " " + temptime + ":" + time.strftime('%M:%S', time.localtime(unix)) + "PM"
  else:
    timeconverted += " " + temptime + ":" + time.strftime('%M:%S', time.localtime(unix)) + "AM"
  return timeconverted