import json
from flask import Flask, request, jsonify, render_template, redirect, url_for
import assistants
import datetime, time

app = Flask(__name__)

daysofweek = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/api/message", methods=["GET", "POST"])
def message():
  if request.method == "GET":
    messagecontent = request.args.get("message")
    # messagecontent += f"\ncurrent datetime: {time.strftime('%a %m/%d/%Y %H:%M:%S')}"
    threadid = request.args.get("threadid")
    response = assistants.message(messagecontent, threadid)
    return response
  else:
    messagecontent = request.form.get("message")
    # messagecontent += f"\ncurrent datetime: {time.strftime('%a %m/%d/%Y %H:%M:%S')}"
    threadid = request.form.get("threadid")
    print(messagecontent + " " + threadid)
    response = assistants.message(messagecontent, threadid)
    # response = "# [click me](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
    return response

@app.route("/api/getmessages", methods=["GET", "POST"])
def fetch():
  if request.method == "GET":
    threadid = request.args.get("threadid")
    response = assistants.getmessagesjson(threadid)
    return jsonify(response)
  else:
    threadid = request.form.get("threadid")
    response = assistants.getmessagesjson(threadid)
    return jsonify(response)

@app.route('/thread/<threadid>')
def thread(threadid):
  return render_template("thread.html", threadid=threadid)

@app.route('/thread')
def threadredirect():
  # with open('threads.txt', 'a') as file:
  #   file.write(assistants.createnewthread() + '\n')
  threadid = assistants.createnewthread()
  return redirect(f'thread/{threadid}')

@app.route('/admin/allthreads')
def viewallthreads():
  # adminid = request.args.get("adminidtokenkey")
  # if adminid == "1234512345adamisthebesttrust123451234876543234565tgfdswe4r56yuijhgfdsgiefiusdfiuadminkeysosecureidsjfoidsjfiojefioji0o3289rfew9w3":
  #   result = ""
  #   with open('threads.txt', 'r') as file:
  #     for line in file.readlines():
  #       result += "<a href='/thread/" + line.strip() + "'>" + line.strip() + "</a><br>"
  #   return result
  # else:
  return "Vercel :("

betas = {'test1': 'Person 1'}

@app.route('/beta/<betaid>')
def betatest(betaid):
  print(betaid)
  if betaid in betas:
    print(betas[betaid])
    return redirect('/')
  else:
    return "Invalid beta key"

@app.route('/feedback')
def feedbackform():
  return '<html><head><title>PantherAI Feedback</title></head><body><div data-tf-live="01HG6KRZK3SGG107Q5WNS32HH1"></div><script src="//embed.typeform.com/next/embed.js"></script></body></html>'

# if __name__ == "__main__":
#   app.run(port=80, debug=True)