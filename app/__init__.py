from flask import Flask
app = Flask(__name__)

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

