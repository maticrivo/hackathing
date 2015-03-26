import os, datetime


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

HIPCHAT = load_settings('HIPCHAT', {
    'token': ''
})

SCHEDULE = {
    'announce': datetime.datetime(2015, 3, 25, 14, 00),
    'freeze': datetime.datetime(2015, 4, 18, 9, 00),
    'the_day': datetime.datetime(2015, 4, 25, 9, 00)
}
DIGEST_SCHEDULE = {
    '1w_to_freeze': SCHEDULE['freeze'] - datetime.timedelta(7),
    '3d_to_freeze': SCHEDULE['freeze'] - datetime.timedelta(3),
    '1d_to_freeze': SCHEDULE['freeze'] - datetime.timedelta(1),
    '2d_to_the_day': SCHEDULE['the_day'] - datetime.timedelta(2),
    '1d_to_the_day': SCHEDULE['the_day'] - datetime.timedelta(1)
}

MESSAGES = {
    'announce': 'HackAthing #{hackathing_num} is on!\nStop whatever it is you\'re doing '
                'and log in NOW: http://teamster.p.doit9.com/login',
    'not_registered': 'Hey Jon Doe, nice to meet you, Jon Doe. Oh, you\'re not Jon Doe? '
                      'Well, I just saw you did not have a name in this HackAthing.. http://teamster.p.doit9.com/login',
    'no_pitch': 'Hi, me again. Remember that cool idea you thought of a while ago? '
                'The one with that stuff that could really improve the thing? Plz rite it heer: '
                'http://teamster.p.doit9.com/pitch WUV U <3 :* )',
    'no_team_0_sugg': 'Ummm.. you didn\'t join a team yet for the HackAthing :/ Pick one here: '
               'http://teamster.p.doit9.com/ideas OR pitch an idea of your own http://teamster.p.doit9.com/pitch',
    'no_team_1_sugg': 'The bat signal is up! There\'s 1 idea that needs your e-x-a-c-t skillset! Click here: '
               'http://teamster.p.doit9.com/ideas/{id}',
    'no_team_much_sugg': 'The bat signal is up! There are {count} ideas that need your exact skillset! Full list here: '
               'http://teamster.p.doit9.com/user/{user}',
    'pitch_much': 'OMG, just wanted to say I LOVED your ideas. Loved \'em. LOVEM! But {count} is a bit much, '
                  'get your act together and pick one: http://teamster.p.doit9.com/user/{user}',
    'team_much': 'Hey, it\'s not that I don\'t believe that you can\'t deliver {count} different ideas.. '
                 'Wait. That\'s exactly it. Narrow it down, dear: http://teamster.p.doit9.com/user/{user}',
    'freeze': 'Honey, the ideas are getting frozen. Last chance to change \'em: http://teamster.p.doit9.com/user/{user}',
    'new_team_member': 'Guess wat! {name} just joined in on {idea.name}! http://teamster.p.doit9.com/user/{user}'

}
