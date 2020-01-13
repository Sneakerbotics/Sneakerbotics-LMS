from flask import Flask, redirect, url_for, render_template, request
from flask_discord import DiscordOAuth2Session
from settings import *

app = Flask(__name__)

if FLASK_ENVIRONMENT == 'development':
    app.secret_key = b"DEV_ENV"
    app.config["DISCORD_REDIRECT_URI"] = "http://localhost:5000/callback"
else:
    app.secret_key = FLASK_SECRET_KEY
    app.config["DISCORD_REDIRECT_URI"] = "http://localhost:5000/callback"

app.config["DISCORD_CLIENT_ID"] = DISCORD_CLIENT_ID
app.config["DISCORD_CLIENT_SECRET"] = DISCORD_CLIENT_SECRET

def getUserIP():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

def isLoggedIn():
    # noinspection PyBroadException
    try:
        user = discord.fetch_user()
    except:
        user = None

    return user

discord = DiscordOAuth2Session(app)

@app.route("/login/")
def login():
    return discord.create_session()

@app.route("/logout/")
def logout():
    discord.revoke()

    return redirect(url_for(".index"))

@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for(".index"))

@app.route("/admin/")
def admin():
    user = isLoggedIn()

    if not user:
        return redirect(url_for(".index"))
    elif user.id in ADMINS:
        return "Hey admin"
    else:
        return redirect(url_for(".index"))

@app.route("/watch/<video>")
def watch(video):
    pass

@app.route("/")
def index():
    user = isLoggedIn()

    return render_template('index.html', user=user, ip=getUserIP())

if __name__ == '__main__':
    app.run()
