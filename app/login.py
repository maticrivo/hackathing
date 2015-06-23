from functools import wraps
from flask_login import login_user, current_user
from flask import redirect, url_for, request
from models import Hackers
from app import app, auth, logger


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if current_user.is_anonymous():
                return redirect(url_for('login', next=request.url))
        except Exception as e:
            return f(*args, **kwargs)
    return decorated_function

@app.route('/login')
def login():
    return redirect(auth.login_url(params=dict(next=request.url, hd='everything.me')))


@app.route('/oauth2callback')
@auth.oauth2callback
def create_or_update_user(token, userinfo, **params):
    username = userinfo['email'].split('@')[0]

    try:
        logger.debug("Looking up user - %s", username)
        user_object = Hackers.get(Hackers.user == username)
    except Hackers.DoesNotExist:
        logger.debug("Creating user object for - %s", username)
        user_object = Hackers.create(name=userinfo['name'], user=username)

    login_user(user_object, force=True, remember=True)

    return redirect(request.args.get('next') or '/')

@auth.user_loader
def load_user(hacker_id):
    return Hackers.get(Hackers.id == hacker_id)