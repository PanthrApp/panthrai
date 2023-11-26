import openai
import os
import sys
import time
import json
if "OPENAI_API_KEY" in os.environ:
  openai.api_key = os.environ["OPENAI_API_KEY"]
  # print(os.environ["OPENAI_API_KEY"])
else:
  print("Error: OPENAI_API_KEY not found in environment variables")
  sys.exit(1)

systemprompt = '''You are an super smart AI superpowered with information about the school. You are serving as an assistant for Jane Lathrop Stanford Middle School in Palo Alto, California. Users will ask you questions, or just have a conversation with you.

You also have access to some formatting functions to help you format the information nicely. You can use these functions to help you format the information nicely for the user.

Cards: To use this, put the following syntax anywhere in your message:
embed("title", "description", "icon", "color")
This will create a card with the title and description and an emoji as the icon. You can use this to format the information nicely for the user. Icon & color are optional. For icon, you can put any valid emoji. For color, you can use ["red", "orange", "green", "blue", "purple"].

You can format with simple markdown in text and in cards.

Use your formatting options whenever possible, but you do not need to use them for every message.'''
messages = [ {"role": "system", "content": systemprompt} ]

months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

calendar = {"2023": {"november": "november2023.json"}}

def betterdate(date):
  date = date.split("/")
  # make it so the month and day are always 2 digits
  if len(date[0]) == 1:
    date[0] = "0" + date[0]
  if len(date[1]) == 1:
    date[1] = "0" + date[1]
  if len(date) == 2:
    date.append("2023")
  if len(date[2]) == 2:
    date[2] = "20" + date[2]
  return "/".join(date)

def menu(date):
  dateday = betterdate(date)
  date = dateday.split("/")
  month = months[int(date[0])-1]
  year = date[2]
  if year not in calendar:
    # todo: determine if it is too far in the future or past
    if year < 2023:
      return "Tell the user that the date asked for is way to far in the past"
    elif year > 2023:
      return "Tell the user that the date asked for is way to far in the future"
  if month not in calendar[year]:
    return "Tell the user that we do not have the menu for this month right now."
  with open(calendar[year][month]) as f:
    data = json.load(f)
  weeks = data["weeks"] # ["week1", "week2", "week3", "week4", etc]
  for i in range(len(weeks)):
    week = data[weeks[i]] # {"days": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"], "week": "week1"}
    for j in range(len(week["days"])):
      day = week[week["days"][j]]
      daydate = betterdate(day["date"])
      if daydate == dateday:
        return ', '.join(day["menu"])
  return 'Give this exact message back to the user, ignoring the rest of the message: "embed("Not a valid date", "The date given was not a weekday.", ":warning:", "orange")"'

def parsecommands(string):
  commands = string.lstrip('"').rstrip('"').split(",")
  # print(commands)
  returns = []
  for command in commands:
    commandname = command.split("(")[0].strip()
    commandargs = command.lstrip(commandname).lstrip('(').rstrip(')')
    if commandname == "menu":
      returns.append(f"The menu for {betterdate(commandargs)} is " + menu(commandargs))
    # elif commandname == "weekmenu":
    #   returns.append(weekmenu(commandargs))
    else:
      returns.append(f"Command {commandname} not found, please do not make up commands.")
  return returns

def question(message):
  mainprompt = f'''
  User is asking a question. You can access information to aid your response

  Current datetime {time.strftime("%m/%d/%Y %H:%M:%S")}
  You can use the time to find events with relative time.

  menu(d) - get the lunch menu a mm/dd/yyyy date. Use for finding the lunch menu for one day.

  Please return a string in quotes with the functions you need to use. If none of these commands fit your needs, leave a blank string. Do not make up commands. Do not include explanations/other text. Ex: "menu(1/3),latestnews()

  User question is: {message}"
  '''
  # print(mainprompt + '\n\n\n')
  tempmessages = messages.copy()
  tempmessages.append( 
      {"role": "user", "content": mainprompt}, 
  ) 
  chat = openai.ChatCompletion.create( 
      model="gpt-3.5-turbo", messages=tempmessages
  )
  reply1 = chat.choices[0].message.content 
  # print(reply1)

  info = '\n\n'.join(parsecommands(reply1))


  tempmessages2 = messages.copy()
  promptask = f'''
  User is asking a question. You can access information to answer:

  User question: {message}

  Current datetime {time.strftime("%m/%d/%Y %H:%M:%S")}

  {info}

  The information is formatted raw. You will need to format it nicely for the user to answer their question.
  '''

  # print(promptask + '\n\n\n')
  tempmessages2.append( 
      {"role": "user", "content": promptask}, 
  )
  chat2 = openai.ChatCompletion.create( 
      model="gpt-3.5-turbo", messages=tempmessages2
  )
  reply2 = chat2.choices[0].message.content

  print(f"{reply2}") 
  messages.append({"role": "user", "content": message})
  messages.append({"role": "assistant", "content": reply2})

# question("What is the menu for 11/3/23?")

while True:
  questionstr = input("Ask a question: ")
  if questionstr:
    question(questionstr)