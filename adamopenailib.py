import time
import json
from lunchmenu import getmenu
from weathers import getweather
from schedule import getschedulefromdate as getscheduletemplate, betterschedule

def await_run_completion(run, thread, client):
  
  while run.status != "completed":
    time.sleep(0.25)
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )
    if run.status == "queued":
      print("in queue...")
    elif run.status == "in_progress":
      print("running...")
    elif run.status == "cancelled":
      print("cancelled")
      return run
    elif run.status == "cancelling":
      print("cancelling")
    elif run.status == "completed":
      print("completed run, sending outputs")
      return run
    elif run.status == "requires_action":
      print("requires action, getting info")
      outputs = {}
      actions = run.required_action.submit_tool_outputs.tool_calls
      for action in actions:
        actionid = action.id
        funcname = action.function.name
        print(funcname)
        print("arguments: " + action.function.arguments)
        if funcname == "today":
          print("getting current date")
          currentdate = time.strftime("%a, %m/%d/%Y %I:%M:%S %p", time.localtime(time.time()))
          outputs[actionid] = currentdate
        if funcname == "get_menu":
          print("getting menu")
          date = json.loads(action.function.arguments)["date"]
          menu = getmenu(date)
          outputs[actionid] = menu
          print(type(menu))
        if funcname == "get_weather":
          print("getting weather")
          date = json.loads(action.function.arguments)["date"]
          weather = getweather(date)
          outputs[actionid] = weather
        if funcname == "get_schedule":
          print("getting schedule")
          date = json.loads(action.function.arguments)["date"]
          schedule = getscheduletemplate(date)
          schedule = betterschedule(schedule)
          outputs[actionid] = schedule
      print("got info, sending outputs")
      outputssubmit = []
      for output in outputs:
        outputssubmit.append({
          "tool_call_id": output,
          "output": outputs[output]
        })
      run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=outputssubmit
      )
      print("sent outputs, awaiting completion")
    else:
      print("unknown status")
      print(run.status)
  return run