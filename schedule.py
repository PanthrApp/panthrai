import json
import datetime

months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

calendar = {
  "2024": {
    "february": "february2024.json",
    "march": "march2024.json",
    "april": "april2024.json",
  }
}

def isweekend(date):
    try:
      given_date = datetime.datetime.strptime(date, '%m/%d/%Y')
      day_of_week = (given_date.weekday() + 1) % 7  # Convert Sunday from 6 to 0
      if day_of_week < 5:
        return False
      else:
        return True
    except ValueError as e:
      return None

def betterdate(date):
  date = date.split("/")
  # make it so the month and day are always 2 digits
  if len(date[0]) == 1:
    date[0] = "0" + date[0]
  if len(date[1]) == 1:
    date[1] = "0" + date[1]
  if len(date) == 2:
    date.append("2024")
  if len(date[2]) == 2:
    date[2] = "20" + date[2]
  return "/".join(date)

def getschedulefromdate(date):
  date = betterdate(date)
  date = date.split("/")
  month = months[int(date[0])-1]
  year = date[2]

  if year not in calendar:
    return "We do not have the schedule for the specified year right now. It could be too far in the past or future."
  if month not in calendar[year]:
    return "We do not have the schedule for the specified month right now. It could be too far in the past or future."
  with open(f'schedules/{calendar[year][month]}') as f:
    data = json.load(f)
  weeks = data["weeks"] # ["week1", "week2", "week3", "week4", etc]
  for i in range(len(weeks)):
    week = data[weeks[i]]
    for j in range(len(week["days"])):
      day = week[week["days"][j]]
      daydate = betterdate(day["date"])
      if daydate == '/'.join(date):
        print(json.dumps(day))
        return json.dumps(day)
  if isweekend('/'.join(date)):
    return 'No schedule found for that date, it is a weekend.'
  return 'No schedule found for that date. It might not be valid, or something else might be wrong.'

def betterschedule(day):
  print(day)
  try:
    day = json.loads(day)
  except json.JSONDecodeError as e:
    return "Error"
  with open("schedules/scheduletemplates.json", 'r') as f:
    scheduletemplates = json.load(f)
  day["schedule"] = scheduletemplates[day["template"]]
  del day["template"]
  return str(json.dumps(day))

def getschedule(day):
  return betterschedule(getschedulefromdate(day))