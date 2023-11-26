import requests

def getweather(date):
  #date is in mm/dd/yyyy format
  url = f"https://api.open-meteo.com/v1/forecast?latitude=37.445&longitude=-122.16&daily=temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=America%2FLos_Angeles"
  response = requests.get(url)
  data = response.json()
  daily = data["daily"]
  highs = daily["temperature_2m_max"]
  lows = daily["temperature_2m_min"]
  dates = daily["time"]
  date = date.split("/")
  date = f"{date[2]}-{date[0]}-{date[1]}"
  print(date)
  print(dates)
  for i in range(len(dates)):
    if dates[i] == date:
      high = int(round(highs[i], 0))
      low = int(round(lows[i], 0))
      return f"High: {high}°F, Low: {low}°F"
  return "Date too far in the future or past."
    
# print(getweather("11/23/2023"))