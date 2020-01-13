import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ADMINS = os.environ.get("ADMINS")
ADMINS = ADMINS.strip('][').split(', ')

FLASK_ENVIRONMENT = os.environ.get("FLASK_ENVIRONMENT")
FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.environ.get("DISCORD_REDIRECT_URI")