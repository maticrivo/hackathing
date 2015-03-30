import hashlib


def md5(txt):
    return hashlib.md5(txt).hexdigest()

def setup_jinja(app):
    app.jinja_env.filters['md5'] = md5