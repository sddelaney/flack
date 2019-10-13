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


txt = {"engineering": ['test']}

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template('index.html', items=txt["engineering"])
    else:
        #add li to page
        return render_template('index.html', items=txt["engineering"])



@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "GET":
        return render_template('register.html')

    else:
        session["name"] = request.form.get("register")
        return redirect("/")


@socketio.on("submit text")
def vote(data):
    txt[data["channel"]].append(data["info"])
    emit("channel text", data, broadcast=True)
