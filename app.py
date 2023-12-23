import json
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, make_response
import assistants
import datetime, time
from authlib.common.security import generate_token
from authlib.integrations.flask_client import OAuth
import os
import sqlite3
import base64
import openai
import base58check

app = Flask(__name__)
app.secret_key = os.urandom(12)

oauth = OAuth(app)

con = sqlite3.connect("main.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(id text, pwhash text, email text, name text, pictureurl text, permissionid int)")
cur.execute("CREATE TABLE IF NOT EXISTS threads(id text, user text, name text, lastmessage datetime)")
con.commit()

daysofweek = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

tokens = {"adam": "116249552855903019643"}

def getuseridfromtoken(token):
  try:
    return tokens[token]
  except:
    return None

def getuserinfofromid(userid):
  con = sqlite3.connect("main.db")
  cur = con.cursor()
  cur.execute("SELECT * FROM users WHERE id=?", (userid,))
  result = cur.fetchall()
  if len(result) == 0:
    return None
  else:
    return result[0]
  
def getuserinfofromtoken(token):
  userid = getuseridfromtoken(token)
  return getuserinfofromid(userid)

@app.route("/")
def index():
  token = request.cookies.get('token')
  if getuseridfromtoken(token) == None:
    return render_template("index.html")
  else:
    return redirect('/user')

@app.route("/api/message", methods=["POST"])
def message():
  token = request.form.get("authorization")
  print(token)
  if token == "":
    return "Your session has expired, please refresh the page."
  userid = getuseridfromtoken(token)
  if userid == "":
    return "Your session has expired, please refresh the page."
  # check if matches userid in database
  con = sqlite3.connect("main.db")
  cur = con.cursor()
  cur.execute("SELECT * FROM threads WHERE id=?", (request.form.get("threadid"),))
  result = cur.fetchall()
  if len(result) == 0:
    return "Thread not found."
  # if result[0][1] != userid:
  #   return "You do not have permission to access this thread."
  # update lastmessage datetime
  cur.execute("UPDATE threads SET lastmessage=? WHERE id=?", (datetime.datetime.now(), request.form.get("threadid")))
  con.commit()
  messagecontent = request.form.get("message")
  # messagecontent += f"\ncurrent datetime: {time.strftime('%a %m/%d/%Y %H:%M:%S')}"
  threadid = request.form.get("threadid")
  print(messagecontent + " " + threadid)
  response = assistants.message(messagecontent, threadid)
  # response = "# [click me](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
  return response

@app.route("/api/getmessages", methods=["POST"])
def fetch():
  token = request.form.get("authorization")
  print(token)
  if token == "":
    return jsonify({})
  userid = getuseridfromtoken(token)
  if userid == None:
    return jsonify({})
  # check if matches userid in database
  con = sqlite3.connect("main.db")
  cur = con.cursor()
  cur.execute("SELECT * FROM threads WHERE id=?", (request.form.get("threadid"),))
  result = cur.fetchall()
  if len(result) == 0:
    return jsonify({})
  if result[0][1] != userid:
    return jsonify({})
  con.commit()
  threadid = request.form.get("threadid")
  response = assistants.getmessagesjson(threadid)
  return jsonify(response)

@app.route('/thread/<threadid>')
def thread(threadid):
  token = request.cookies.get('token')
  userid = getuseridfromtoken(token)
  if userid == None:
    return redirect('/google')
  con = sqlite3.connect("main.db")
  cur = con.cursor()
  cur.execute("SELECT * FROM threads WHERE id=?", (threadid,))
  result = cur.fetchall()
  if len(result) == 0:
    return redirect('/404?page=' + request.path)
  if result[0][1] != userid:
    return redirect('/404?page=' + request.path)
  return render_template("thread.html", threadid=threadid)

@app.route('/thread')
def threadredirect():
  token = request.cookies.get('token')
  userid = getuseridfromtoken(token)
  if userid == None:
    return redirect('/google')
  con = sqlite3.connect("main.db")
  cur = con.cursor()
  threadid = assistants.createnewthread()
  cur.execute("INSERT INTO threads VALUES (?, ?, ?, ?)", (threadid, userid, "Chat", datetime.datetime.now()))
  con.commit()
  return redirect(f'thread/{threadid}')

@app.route('/api/getthreads', methods=["POST"])
def getthreads():
  token = request.form.get("authorization")
  userid = getuseridfromtoken(token)
  con = sqlite3.connect("main.db")
  cur = con.cursor()
  cur.execute("SELECT * FROM threads WHERE user=?", (userid))
  result = cur.fetchall()
  print(jsonify(result))
  return jsonify(result)

@app.route('/api/threadinfo', methods=["POST"])
def threadinfo():
  token = request.form.get("authorization")
  userid = getuseridfromtoken(token)
  con = sqlite3.connect("main.db")
  cur = con.cursor()
  cur.execute("SELECT * FROM threads WHERE id=?", (request.form.get("threadid"),))
  result = cur.fetchall()
  if len(result) == 0:
    return "Error"
  if result[0][1] != userid:
    return "Error"
  return jsonify(result[0])

@app.route('/admin')
def admin():
  token = request.cookies.get('token')
  if getuseridfromtoken(token) == None:
    return redirect('/404?page=' + request.path)
  if getuserinfofromtoken(token)[5] == 10:
    return render_template("page.html", content="<h1>Admin Panel</h1><h2>Actions:</h2><ul><li><a href='/admin/allthreads'>View all threads</a></li></ul>")
  else:
    return redirect('/404?page=' + request.path)

@app.route('/admin/allthreads')
def viewallthreads():
  token = request.cookies.get('token')
  if getuseridfromtoken(token) == None:
    return redirect('/404?page=' + request.path)
  if getuserinfofromtoken(token)[5] == 10:
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM threads")
    result = cur.fetchall()
    result = sorted(result, key=lambda x: x[3], reverse=True)
    returner = ""
    for thread in result:
      newdatetime = datetime.datetime.strptime(thread[3], "%Y-%m-%d %H:%M:%S.%f")
      newdatetime = newdatetime.strftime("%m/%d/%Y %I:%M %p")
      userid = thread[1]
      print(userid)
      username = getuserinfofromid(userid)[3]
      returner += "<li><b><a href='/thread/" + thread[0] + "'>" + thread[2] + "</a></b> Last modified: " + newdatetime + " by " + username + " (" + userid + ")</li>"
    return render_template("page.html", content="<h1>Admin Panel</h1><h2>All Threads:</h2><ul>" + returner + "</ul>")
  else:
    return redirect('/404?page=' + request.path)

@app.route('/beta/<betaid>')
def betatest(betaid):
  print(betaid)
  return redirect('/')

@app.route('/feedback')
def feedbackform():
  return '<html><head><title>PantherAI Feedback</title></head><body><div data-tf-live="01HG6KRZK3SGG107Q5WNS32HH1"></div><script src="//embed.typeform.com/next/embed.js"></script></body></html>'

@app.route('/tours/chat')
def tourintro():
  return render_template("tour.html")

@app.route('/google')
def google():

    GOOGLE_CLIENT_ID = '1055892927108-1r2o4mhahko9ti4n97brdi1pkm3aka53.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    print(redirect_uri)
    session['nonce'] = generate_token()
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])

@app.route('/google/auth')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session['nonce'])
    session['user'] = user
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    email = user['email']
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    result = cur.fetchall()
    response = make_response(redirect(f'/user'))
    random = os.urandom(32)
    randomb58 = base58check.b58encode(random).decode('utf-8')
    useridb58 = base58check.b58encode(user['sub'].encode('utf-8')).decode('utf-8')
    currentdate = datetime.datetime.now()
    currentdate = currentdate.strftime("%a, %m/%d/%Y %H:%M:%S")
    timeb58 = base58check.b58encode(currentdate.encode('utf-8')).decode('utf-8')
    token = f"{str(useridb58)}.{str(timeb58)}.{str(randomb58)}"
    tokens[token] = user['sub']
    response.set_cookie('token', token, expires=datetime.datetime.now() + datetime.timedelta(days=7))
    if len(result) == 0:
      if "picture" in user:
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (user['sub'], "", email, user['given_name'] + " " + user['family_name'], user['picture'], 0))
      else:
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (user['sub'], "", email, user['given_name'] + " " + user['family_name'], "https://panthr.app/static/resources/images/default-profile.png", 0))
      con.commit()
      return response
    con.commit()
    return response

@app.route('/user')
def user():
  token = request.cookies.get('token')
  userid = getuseridfromtoken(token)
  if userid == None:
    return redirect('/google')
  userinfo = getuserinfofromid(userid)
  name = userinfo[3]
  # get user threads
  con = sqlite3.connect("main.db")
  cur = con.cursor()
  cur.execute("SELECT * FROM threads WHERE user=?", (userid,))
  result = cur.fetchall()
  threads = ""
  for thread in result:
    newdatetime = datetime.datetime.strptime(thread[3], "%Y-%m-%d %H:%M:%S.%f")
    newdatetime = newdatetime.strftime("%m/%d/%Y %I:%M %p")
    threads += "<li><b><a href='/thread/" + thread[0] + "'>" + thread[2] + "</a></b> Last modified: " + newdatetime + "</li>"
  return render_template("page.html", content=f"<h1>Welcome, {name}!</h1><p>Now that you're logged in, you can start chatting!</p>" + "<h2>Your Threads:</h2><ul>" + threads + "</ul>")

@app.errorhandler(404)
def error404(e):
  return redirect('/404?page=' + request.path)

@app.route('/404')
def error404page():
  if request.args.get("page") == None:
    return render_template("page.html", content="<h1>404</h1><p>What are you doing here? Are you actively trying to find the 404 page? If so, congratulations, you found it! If you're not, then you should probably contact me because the page you're looking for doesn't exist.</p>")
  return render_template("404.html", page=request.args.get("page"))

@app.route('/logout')
def logout():
  response = make_response(redirect('/'))
  response.set_cookie('token', '', expires=0)
  return response

if __name__ == "__main__":
  app.run(port=8080, debug=True)