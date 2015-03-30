import hashlib


def md5(txt):
    return hashlib.md5(txt).hexdigest()

def prefix(list, prefix):
    return map(lambda x: prefix+str(x), list)

def setup_jinja(app):
    app.jinja_env.filters['md5'] = md5
    app.jinja_env.filters['prefix'] = prefix