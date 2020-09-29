import os

from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from helpers import apology, login_required
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


txt = {"General": ['Start of messages in this channel'],
       "Engineering": ['Start of messages in this channel'],
       "Support": ['Start of messages in this channel']}
active_users = []

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template('index.html', items=txt["General"], channel="General", channels=txt.keys())

@app.route("/<string:channel>", methods=["GET", "POST"])
@login_required
def channel(channel):
    if channel in txt:
        return render_template('index.html', items=txt[channel], channel=channel, channels=txt.keys())
    else:
        return apology("no channel by that name {}".format(channel), 404)


@app.route("/add/", methods=["POST"])
@login_required
def add():
    channel = request.form.get("addchannel")
    if channel in txt:
        return apology("channel already exists", 400)
    else:
        txt[channel] = ["Start of messages in this channel"]
        return render_template('index.html', items=txt[channel], channel=channel, channels=txt.keys())

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "GET":
        return render_template('register.html')

    else:
        session["name"] = request.form.get("register")
        if session["name"] in active_users:
            return apology("username taken", 400)
        else:    
            active_users.append(session["name"])
            return index()


@socketio.on("submit text")
def vote(data):
    data["info"] = session["name"] + " " + data["info"]
    txt[data["channel"]].append(data["info"])
    emit("channel text", data, broadcast=True)


@app.route("/redirect/<string:channel>", methods=["GET"])
@login_required
def redirect(channel):
    print(channel)
    if channel in txt:
        print("yay")
        return render_template('index.html', items=txt[channel], channel=channel, channels=txt.keys())
    else:
        return apology("no channel by that name -- {}".format(channel), 404)