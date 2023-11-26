import json

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

def getmenu(date):
  dateday = betterdate(date)
  print(dateday)
  date = dateday.split("/")
  month = months[int(date[0])-1]
  year = date[2]
  if year not in calendar:
    # todo: determine if it is too far in the future or past
    # if year < 2023:
    #   return "Tell the user that the date asked for is way to far in the past"
    # elif year > 2023:
    return "Tell the user that the year was not found."
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
  return 'No menu found for that date, is it a weekend?'
