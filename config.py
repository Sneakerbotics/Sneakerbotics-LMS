import os
from os.path import join, dirname
from dotenv import load_dotenv

# VdoCipher Secret: xSyKGczUqGIRzc6vdpqLDO2R2zcYtPfZIoJImwTbeTDvD3px9Slmd4geUTvFWRqw

if os.environ.get("ENVIRO") != "prod":
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

ADMIN = os.environ.get("ADMIN")

VDOCIPHER_SECRET = os.environ.get("VDOCIPHER_SECRET")

FLASK_ENVIRONMENT = os.environ.get("FLASK_ENVIRONMENT")
FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.environ.get("DISCORD_REDIRECT_URI")
