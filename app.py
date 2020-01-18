from flask import Flask, redirect, url_for, render_template, request
from flask_discord import DiscordOAuth2Session
from video_handler import *
from config import *
import requests

app = Flask(__name__)
vh = VideoHandler()

if FLASK_ENVIRONMENT == 'dev':
    app.secret_key = b"DEV_ENV"
    app.config["DISCORD_REDIRECT_URI"] = "http://localhost:5000/callback"
else:
    app.secret_key = FLASK_SECRET_KEY
    app.config["DISCORD_REDIRECT_URI"] = DISCORD_REDIRECT_URI

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

def userIsInSneakerbotics():
    guilds = discord.fetch_guilds()

    for guild in guilds:
        if guild.id == 642900909793345536:
            return True

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
        return "Not a user"

    elif user.id == int(ADMIN):
        return render_template('admin.html', user=user)

    else:
        return "Not an admin: " + str(user.id)

@app.route("/watch/<video>")
def watch(video):
     user = isLoggedIn()

     VdoCipherHeaders = {
         'Content-Type': 'application/json',
         'Accept': 'application/json',
         'Authorization': 'Apisecret ' + VDOCIPHER_SECRET,
     }

     VdoCipherParams  = {
        'ttl': '330'
     }

     VdoCipherURL = 'https://dev.vdocipher.com/api/videos/' + video + '/otp'

     response = requests.post(VdoCipherURL, headers=VdoCipherHeaders, params=VdoCipherParams)
     responseJSON = response.json()

     try:
         otp = str(responseJSON['otp'])
         playbackInfo = str(responseJSON['playbackInfo'])
         error=False
     except:
         error=True
         otp=None
         playbackInfo=None

     title = vh.getVideoTitle(video)

     return render_template('watch_video.html', user=user, otp=otp, playbackInfo=playbackInfo, title=title, error=error)

@app.route("/")
def index():
    user = isLoggedIn()

    if user:
        if userIsInSneakerbotics():
            weeks=json.dumps(vh.giveWeeks())
            loaded_weeks = json.loads(weeks)
            return render_template('index.html', user=user, ip=getUserIP(), weeks=loaded_weeks)

        else:
            return render_template('index.html', user=user, ip=getUserIP())
    else:
        return render_template('index.html', user=user, ip=getUserIP())

if __name__ == '__main__':
    app.run()
