import hashlib
from settings import COLORS


def md5(txt):
    return hashlib.md5(txt).hexdigest()

def prefix(list, prefix):
    return map(lambda x: prefix+str(x), list)

def colorize(str, hue='600'):
    color_node = COLORS[int(md5(str), 16) % len(COLORS)]
    return color_node['hues'][hue]

def rgb(hex):
    _NUMERALS = '0123456789abcdefABCDEF'
    _HEXDEC = {v: int(v, 16) for v in (x+y for x in _NUMERALS for y in _NUMERALS)}
    hex = hex[1:] # remove hash char

    return '{},{},{}'.format(_HEXDEC[hex[0:2]], _HEXDEC[hex[2:4]], _HEXDEC[hex[4:6]])

def setup_jinja(app):
    app.jinja_env.filters['md5'] = md5
    app.jinja_env.filters['prefix'] = prefix
    app.jinja_env.filters['colorize'] = colorize
    app.jinja_env.filters['rgb'] = rgb