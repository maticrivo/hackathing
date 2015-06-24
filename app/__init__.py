import os, logging
from flask import Flask
from flask_googlelogin import GoogleLogin

from app import settings

logger = logging.getLogger(__name__)

def setup_logging():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s][PID:%(process)d][%(levelname)s][%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(settings.LOG['level'])
    logging.getLogger("passlib").setLevel("ERROR")

setup_logging()

app = Flask(__name__)
app.config.update(
    GOOGLE_LOGIN_CLIENT_ID=os.environ['GOOGLE_LOGIN_CLIENT_ID'],
    GOOGLE_LOGIN_CLIENT_SECRET=os.environ['GOOGLE_LOGIN_CLIENT_SECRET'],
    GOOGLE_LOGIN_REDIRECT_URI='http://127.0.0.1:5000/oauth2callback',
    GOOGLE_LOGIN_SCOPES='email',
    SECRET_KEY='hackathing_secret'
)
auth = GoogleLogin(app=app)


from hypchat import HypChat
from settings import HIPCHAT
hc = HypChat(HIPCHAT['token'], endpoint="https://evme.hipchat.com")

from app.jinja import setup_jinja
setup_jinja(app)

def send_hipchat_msg(user, msg):
    if user == 'ran@everything.me':
        hc.get_user(user).message(msg)

def email(name):
    return name+'@everything.me'

