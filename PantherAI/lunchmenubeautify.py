# print("Paste in lunch menu. When finished, enter a blank line.")
menu = ""
while True:
  line = input()
  if line == "":
    break
  menu += line + "\n"

def printsection(section):
  print('"', end='')
  print(section, end='')
  print('"', end='')

sections = []
superfoodsindex = menu.find("SUPER FOODS")
sections.append(menu[:superfoodsindex].replace("\n", " ").rstrip(" "))
everydayselectsindex = menu.find("EVERYDAY SELECTS")
sections.append(menu[superfoodsindex:everydayselectsindex].replace("\n", " ").rstrip(" "))
sections.append(menu[everydayselectsindex:].replace("\n", " ").rstrip(" "))
for i in range(3):
#   if i != 0:
  print(' '*16, end='')
  printsection(sections[i])
  if i != 2:
    print(",\n", end='')