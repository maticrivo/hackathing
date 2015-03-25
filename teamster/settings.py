import os


def load_settings(prefix, defaults):
    for k, v in defaults.iteritems():
        env_name = '%s_%s' % (prefix, k.upper())
        defaults[k] = os.environ.get(env_name, v)

    return defaults

DATABASE = load_settings('DATABASE', {
    'class': 'MySQLDatabase',
    'name': 'Teamster',
    'host': '',
    'user': 'root',
    'password': ''
})