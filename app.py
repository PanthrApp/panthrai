import json
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, make_response
import assistants
import datetime, time
from authlib.common.security import generate_token
from authlib.integrations.flask_client import OAuth
import os
import sqlite3
import base64
import base58check
from config import g_client_id, g_client_secret
import random

app = Flask(__name__)
app.secret_key = os.urandom(12)

oauth = OAuth(app)

con = sqlite3.connect("main.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(id text, pwhash text, email text, name text, pictureurl text, permissionid int)")
cur.execute("CREATE TABLE IF NOT EXISTS threads(id text, userid text, name text, lastmessage datetime)")
con.commit()

daysofweek = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

tokens = {"adam": "115001961098923012957"}

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
    response = make_response(render_template("index.html"))
    # response.set_cookie('token', 'adam')
    return response
  else:
    return redirect('/user')

betausers = {
  "XjN9QEmm3GwGWpNTCGXp45te": ["XjN9QEmm3GwGWpNTCGXp45te", "", "betauser@panthr.ai", "Beta User", "https://panthr.app/static/resources/default-profile.png", 0],
  "C9xpUdNGdpLSDzPmxLNC2ZA6": ["C9xpUdNGdpLSDzPmxLNC2ZA6", "", "betauser@panthr.ai", "Beta User", "https://panthr.app/static/resources/default-profile.png", 0],
  "y9rqZCkGEPmsZxadZeAfMJyq": ["y9rqZCkGEPmsZxadZeAfMJyq", "", "betauser@panthr.ai", "Beta User", "https://panthr.app/static/resources/default-profile.png", 0],
  "xuv8I8bUwnCodLvNBiAjkdmT": ["xuv8I8bUwnCodLvNBiAjkdmT", "", "betauser@panthr.ai", "Beta User", "https://panthr.app/static/resources/default-profile.png", 0],
  "qpDbEG6uPKw4DemhLavoFf6H": ["qpDbEG6uPKw4DemhLavoFf6H", "", "betauser@panthr.ai", "Beta User", "https://panthr.app/static/resources/default-profile.png", 0],
  "DfFGuEmSongCGkKaoolIBiao": ["DfFGuEmSongCGkKaoolIBiao", "", "betauser@panthr.ai", "Beta User", "https://panthr.app/static/resources/default-profile.png", 0],
  "8kJYdbfHSh9qSNOnNSHHSjis": ["8kJYdbfHSh9qSNOnNSHHSjis", "", "betauser@panthr.ai", "Beta User", "https://panthr.app/static/resources/default-profile.png", 0],
  "QXITlX4jYAdnuGal8R6xSMVy": ["QXITlX4jYAdnuGal8R6xSMVy", "", "betauser@panthr.ai", "Beta User", "https://panthr.app/static/resources/default-profile.png", 0],
  "U7WwLO3Cpl7wi2vtCqTGxzVG": ["U7WwLO3Cpl7wi2vtCqTGxzVG", "", "betauser@panthr.ai", "Beta User", "https://panthr.app/static/resources/default-profile.png", 0],
  "uIdXdeV2RrXNtmYBOjlGyRgQ": ["uIdXdeV2RrXNtmYBOjlGyRgQ", "", "betauser@panthr.ai", "Beta User", "https://panthr.app/static/resources/default-profile.png", 0],
  "cMT9fmvAsnhLieUtU4WKDFqk": ["cMT9fmvAsnhLieUtU4WKDFqk", "", "betauser@panthr.ai", "Beta User", "https://panthr.app/static/resources/default-profile.png", 0],
}

@app.route("/beta")
def beta():
  betaid = request.args.get("ref")
  con = sqlite3.connect("main.db")
  cur = con.cursor()
  cur.execute("SELECT * FROM users WHERE id=?", (betaid,))
  result = cur.fetchall()
  if len(result) == 0:
    if betaid in betausers:
      cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (betausers[betaid][0], betausers[betaid][1], betausers[betaid][2], betausers[betaid][3], betausers[betaid][4], betausers[betaid][5]))
      con.commit()
    else:
      return redirect('/404?page=' + request.path)
  response = make_response(redirect('/'))
  random = os.urandom(32)
  randomb58 = base58check.b58encode(random).decode('utf-8')
  useridb58 = base58check.b58encode(betaid.encode('utf-8')).decode('utf-8')
  currentdate = datetime.datetime.now()
  currentdate = currentdate.strftime("%a, %m/%d/%Y %H:%M:%S")
  timeb58 = base58check.b58encode(currentdate.encode('utf-8')).decode('utf-8')
  token = f"{str(useridb58)}.{str(timeb58)}.{str(randomb58)}"
  tokens[token] = betaid
  response.set_cookie('token', token, expires=datetime.datetime.now() + datetime.timedelta(days=7))
  return response

@app.route("/api/message", methods=["POST"])
def message():
  token = request.form.get("authorization")
  print(token)
  if token == "":
    return "Your session has expired, please refresh the page."
  userid = getuseridfromtoken(token)
  if userid == "":
    return "Your session has expired, please refresh the page."
  con = sqlite3.connect("main.db")
  cur = con.cursor()
  cur.execute("SELECT * FROM threads WHERE id=?", (request.form.get("threadid"),))
  result = cur.fetchall()
  if len(result) == 0:
    return "Thread not found."
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
  response = assistants.getmessagesjson(threadid, result[0][2])
  return jsonify(response)

@app.route('/api/renamethread', methods=["POST"])
def renamethread():
  token = request.form.get("authorization")
  userid = getuseridfromtoken(token)
  if userid == None:
    return "Error"
  con = sqlite3.connect("main.db")
  cur = con.cursor()
  cur.execute("SELECT * FROM threads WHERE id=?", (request.form.get("threadid"),))
  result = cur.fetchall()
  if len(result) == 0:
    return "Error"
  if result[0][1] != userid:
    return "Error"
  print("Thread ID: " + request.form.get("threadid"))
  print("New Name: " + request.form.get("newname"))
  cur.execute("UPDATE threads SET name=? WHERE id=?", (request.form.get("newname"), request.form.get("threadid")))
  con.commit()
  return "Success"

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
  cur.execute("INSERT INTO threads VALUES (?, ?, ?, ?)", (threadid, userid, "Untitled thread", datetime.datetime.now()))
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

@app.route('/tours/update')
def updatemodal():
  return render_template("updatemodal.html")

@app.route('/google')
def google():

    GOOGLE_CLIENT_ID = g_client_id
    GOOGLE_CLIENT_SECRET = g_client_secret

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
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (user['sub'], "", email, user['given_name'] + " " + user['family_name'], "https://panthr.app/static/resources/default-profile.png", 0))
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
  cur.execute("SELECT * FROM threads WHERE userid=?", (userid,))
  result = cur.fetchall()
  threads = ""
  for thread in result:
    newdatetime = datetime.datetime.strptime(thread[3], "%Y-%m-%d %H:%M:%S.%f")
    newdatetime = newdatetime.strftime("%m/%d/%Y %I:%M %p")
    threads += "<li><b><a href='/thread/" + thread[0] + "'>" + thread[2] + "</a></b> Last message: " + newdatetime + "</li>"
  if threads == "":
    threads = "<li>Looks like you don't have any threads yet. <a href='/thread'>Create</a> your first one now!</li>"
  return render_template("user.html", content=threads, name=name, picture=userinfo[4])

@app.route('/settings')
def settings():
  token = request.cookies.get('token')
  userid = getuseridfromtoken(token)
  if userid == None:
    return redirect('/google')
  userinfo = getuserinfofromid(userid)
  name = userinfo[3]
  email = userinfo[2]
  return render_template("settings.html", name=name, email=email, picture=userinfo[4])

@app.route('/settings/update', methods=["POST"])
def updatesettings():
  token = request.cookies.get('token')
  userid = getuseridfromtoken(token)
  if userid == None:
    return redirect('/google')
  userinfo = getuserinfofromid(userid)
  name = request.form.get("name")
  email = request.form.get("email")
  con = sqlite3.connect("main.db")
  cur = con.cursor()
  cur.execute("UPDATE users SET name=?, email=? WHERE id=?", (name, email, userid))
  con.commit()
  return redirect('/user')

@app.route('/accountdeletion', methods=["GET", "POST"])
def accountdeletion():
  if request.method == "GET":
    return render_template("page.html", content="<h1>Delete your account</h1><p>We're sad to see you go. To delete your account, just check the box and hit the delete button.</p><form method='post'><input type='checkbox' name='confirm' value='yes' required><label for='confirm'>I understand that by deleting my account, all of my data will be immediately wiped from PantherAI's servers. There is no reversal as the deletion occurs immediately.</label><br><input type='submit' value='Delete'></form>")
  else:
    token = request.cookies.get('token')
    userid = getuseridfromtoken(token)
    if userid == None:
      return redirect('/google')
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (userid,))
    con.commit()
    # delete all threads
    cur.execute("DELETE FROM threads WHERE userid=?", (userid,))
    con.commit()
    response = make_response(render_template("page.html", content="<h1>Account Deleted</h1><p>Your account has been successfully deleted along with all of your threads and chat history.</p><a href='/'><button>Return to Home</button></a><a href='/user'><button>Get Started</button></a>"))
    response.set_cookie('token', '', expires=0)
    return response

@app.route('/super-secret/starfield/pirated-from-replit/inspect')
def inspect():
  return render_template("starfield.html")

@app.errorhandler(404)
def error404(e):
  return redirect('/404?page=' + request.path)

@app.route('/404')
def error404page():
  if request.args.get("page") == None:
    return render_template("page.html", content="<h1>404</h1><p>What are you doing here? Are you trying to find the 404 page? If so, congratulations, you found it! If you're not, then the page you're looking for doesn't exist.</p>")
  return render_template("404.html", page=request.args.get("page"))

@app.route('/logout')
def logout():
  response = make_response(redirect('/'))
  response.set_cookie('token', '', expires=0)
  return response

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)