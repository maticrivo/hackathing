import logging
from flask import Flask
from flask_googlelogin import GoogleLogin
from app import settings
from app.db import db
from app.jinja import setup_jinja


def setup_app():
    app = Flask(__name__)
    app.config.update(
        GOOGLE_LOGIN_CLIENT_ID=settings.GOOGLE_LOGIN['CLIENT_ID'],
        GOOGLE_LOGIN_CLIENT_SECRET=settings.GOOGLE_LOGIN['CLIENT_SECRET'],
        GOOGLE_LOGIN_REDIRECT_URI=settings.GOOGLE_LOGIN['REDIRECT_URI'],
        GOOGLE_LOGIN_SCOPES='email',
        SECRET_KEY='hackathing_secret'
    )
    db.init_app(app)
    return app, GoogleLogin(app=app)


def setup_logging():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s][PID:%(process)d][%(levelname)s][%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(settings.LOG['level'])
    logging.getLogger("passlib").setLevel("ERROR")

    return logging.getLogger(__name__)

def email(name):
    return name+'@everything.me'

logger = setup_logging()
app, auth = setup_app()
setup_jinja(app)


# from hypchat import HypChat
# from settings import HIPCHAT

# hc = HypChat(HIPCHAT['token'], endpoint="https://evme.hipchat.com")

# def send_hipchat_msg(user, msg):
#     if user == 'ran@everything.me':
#         hc.get_user(user).message(msg)


