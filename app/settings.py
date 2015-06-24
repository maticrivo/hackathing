import os, datetime


def load_settings(prefix, defaults):
    for k, v in defaults.iteritems():
        env_name = '%s_%s' % (prefix, k.upper())
        defaults[k] = os.environ.get(env_name, v)

    return defaults

DATABASE = load_settings('DATABASE', {
    'class': 'MySQLDatabase',
    'name': 'hackathing',
    'host': '',
    'user': 'root',
    'password': ''
})

LOG = load_settings('LOG', {
    'level': 'DEBUG'
})

HIPCHAT = load_settings('HIPCHAT', {
    'token': ''
})

CURRENT_HACKATHING = 7

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
                'and log in NOW: http://hackathing.p.doit9.com/login',
    'not_registered': 'Hey Jon Doe, nice to meet you, Jon Doe. Oh, you\'re not Jon Doe? '
                      'Well, I just saw you did not have a name in this HackAthing.. http://hackathing.p.doit9.com/login',
    'no_pitch': 'Hi, me again. Remember that cool idea you thought of a while ago? '
                'The one with that stuff that could really improve the thing? Plz rite it heer: '
                'http://hackathing.p.doit9.com/pitch WUV U <3 :* )',
    'no_team_0_sugg': 'Ummm.. you didn\'t join a team yet for the HackAthing :/ Pick one here: '
               'http://hackathing.p.doit9.com/projects OR pitch an idea of your own http://hackathing.p.doit9.com/pitch',
    'no_team_1_sugg': 'The bat signal is up! There\'s 1 idea that needs your e-x-a-c-t skillset! Click here: '
               'http://hackathing.p.doit9.com/projects/{id}',
    'no_team_much_sugg': 'The bat signal is up! There are {count} ideas that need your exact skillset! Full list here: '
               'http://hackathing.p.doit9.com/hacker/{hacker}',
    'pitch_much': 'OMG, just wanted to say I LOVED your ideas. Loved \'em. LOVEM! But {count} is a bit much, '
                  'get your act together and pick one: http://hackathing.p.doit9.com/hacker/{hacker}',
    'team_much': 'Hey, it\'s not that I don\'t believe that you can\'t deliver {count} different ideas.. '
                 'Wait. That\'s exactly it. Narrow it down, dear: http://hackathing.p.doit9.com/hacker/{hacker}',
    'freeze': 'Honey, the ideas are getting frozen. Last chance to change \'em: http://hackathing.p.doit9.com/hacker/{hacker}',
    'new_team_member': 'Guess wat! {name} just joined in on {project.name}! http://hackathing.p.doit9.com/hacker/{hacker}'

}

COLORS = [
  {
    'name': 'red',
    'hues': {
      '50':  '#FFEBEE',
      '100': '#FFCDD2',
      '200': '#EF9A9A',
      '300': '#E57373',
      '400': '#EF5350',
      '500': '#F44336',
      '600': '#E53935',
      '700': '#D32F2F',
      '800': '#C62828',
      '900': '#B71C1C',
    }
  },
  {
    'name': 'pink',
    'niceName': 'Pink',
    'hues': {
      '50':  '#fce4ec',
      '100': '#f8bbd0',
      '200': '#f48fb1',
      '300': '#f06292',
      '400': '#ec407a',
      '500': '#e91e63',
      '600': '#d81b60',
      '700': '#c2185b',
      '800': '#ad1457',
      '900': '#880e4f',
    }
  },
  {
    'name': 'purple',
    'niceName': 'Purple',
    'hues': {
      '50':  '#f3e5f5',
      '100': '#e1bee7',
      '200': '#ce93d8',
      '300': '#ba68c8',
      '400': '#ab47bc',
      '500': '#9c27b0',
      '600': '#8e24aa',
      '700': '#7b1fa2',
      '800': '#6a1b9a',
      '900': '#4a148c',
    }
  },
  {
    'name': 'deep-purple',
    'niceName': 'Deep Purple',
    'hues': {
      '50':  '#ede7f6',
      '100': '#d1c4e9',
      '200': '#b39ddb',
      '300': '#9575cd',
      '400': '#7e57c2',
      '500': '#673ab7',
      '600': '#5e35b1',
      '700': '#512da8',
      '800': '#4527a0',
      '900': '#311b92',
    }
  },
  {
    'name': 'indigo',
    'niceName': 'Indigo',
    'hues': {
      '50':  '#e8eaf6',
      '100': '#c5cae9',
      '200': '#9fa8da',
      '300': '#7986cb',
      '400': '#5c6bc0',
      '500': '#3f51b5',
      '600': '#3949ab',
      '700': '#303f9f',
      '800': '#283593',
      '900': '#1a237e',
    }
  },
  {
    'name': 'blue',
    'niceName': 'Blue',
    'hues': {
      '50':  '#E3F2FD',
      '100': '#BBDEFB',
      '200': '#90CAF9',
      '300': '#64B5F6',
      '400': '#42A5F5',
      '500': '#2196F3',
      '600': '#1E88E5',
      '700': '#1976D2',
      '800': '#1565C0',
      '900': '#0D47A1',
    }
  },
  {
    'name': 'light-blue',
    'niceName': 'Light Blue',
    'hues': {
      '50':  '#e1f5fe',
      '100': '#b3e5fc',
      '200': '#81d4fa',
      '300': '#4fc3f7',
      '400': '#29b6f6',
      '500': '#03a9f4',
      '600': '#039be5',
      '700': '#0288d1',
      '800': '#0277bd',
      '900': '#01579b',
    }
  },
  {
    'name': 'cyan',
    'niceName': 'Cyan',
    'hues': {
      '50':  '#e0f7fa',
      '100': '#b2ebf2',
      '200': '#80deea',
      '300': '#4dd0e1',
      '400': '#26c6da',
      '500': '#00bcd4',
      '600': '#00acc1',
      '700': '#0097a7',
      '800': '#00838f',
      '900': '#006064',
    }
  },
  {
    'name': 'teal',
    'niceName': 'Teal',
    'hues': {
      '50':  '#e0f2f1',
      '100': '#b2dfdb',
      '200': '#80cbc4',
      '300': '#4db6ac',
      '400': '#26a69a',
      '500': '#009688',
      '600': '#00897b',
      '700': '#00796b',
      '800': '#00695c',
      '900': '#004d40',
    }
  },
  {
    'name': 'green',
    'niceName': 'Green',
    'hues': {
      '50':  '#E8F5E9',
      '100': '#C8E6C9',
      '200': '#A5D6A7',
      '300': '#81C784',
      '400': '#66BB6A',
      '500': '#4CAF50',
      '600': '#43A047',
      '700': '#388E3C',
      '800': '#2E7D32',
      '900': '#1B5E20',
    }
  },
  {
    'name': 'light-green',
    'niceName': 'Light Green',
    'hues': {
      '50':  '#f1f8e9',
      '100': '#dcedc8',
      '200': '#c5e1a5',
      '300': '#aed581',
      '400': '#9ccc65',
      '500': '#8bc34a',
      '600': '#7cb342',
      '700': '#689f38',
      '800': '#558b2f',
      '900': '#33691e',
    }
  },
  {
    'name': 'lime',
    'niceName': 'Lime',
    'hues': {
      '50':  '#f9fbe7',
      '100': '#f0f4c3',
      '200': '#e6ee9c',
      '300': '#dce775',
      '400': '#d4e157',
      '500': '#cddc39',
      '600': '#c0ca33',
      '700': '#afb42b',
      '800': '#9e9d24',
      '900': '#827717',
    }
  },
  {
    'name': 'yellow',
    'niceName': 'Yellow',
    'hues': {
      '50':  '#fffde7',
      '100': '#fff9c4',
      '200': '#fff59d',
      '300': '#fff176',
      '400': '#ffee58',
      '500': '#ffeb3b',
      '600': '#fdd835',
      '700': '#fbc02d',
      '800': '#f9a825',
      '900': '#f57f17',
    }
  },
  {
    'name': 'amber',
    'niceName': 'Amber',
    'hues': {
      '50':  '#fff8e1',
      '100': '#ffecb3',
      '200': '#ffe082',
      '300': '#ffd54f',
      '400': '#ffca28',
      '500': '#ffc107',
      '600': '#ffb300',
      '700': '#ffa000',
      '800': '#ff8f00',
      '900': '#ff6f00',
    }
  },
  {
    'name': 'orange',
    'niceName': 'Orange',
    'hues': {
      '50':  '#fff3e0',
      '100': '#ffe0b2',
      '200': '#ffcc80',
      '300': '#ffb74d',
      '400': '#ffa726',
      '500': '#ff9800',
      '600': '#fb8c00',
      '700': '#f57c00',
      '800': '#ef6c00',
      '900': '#e65100',
    }
  }
]
