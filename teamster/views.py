from teamster import app, settings, email, send_hipchat_msg
from models import *
from flask import render_template

@app.route('/ranbena')
def hello_world():
    return 'Hello World!'

@app.route('/user/<user>')
def user(user):
    person = Persons.by_user(user)
    skills = PersonsSkills.by_person(person)
    pitched = Ideas.by_person(person)
    joined = [x.idea for x in TeamUps.by_person(person)]
    suggested = Ideas.suggest_by_person(person)

    ctx = {
        'name': person.name,
        'skills': [s.skill for s in skills],
        'pitched': pitched,
        'joined': joined,
        'suggested': suggested
    }

    return render_template('user.html', ctx=ctx)

@app.route('/')
@app.route('/ideas')
def ideas():
    ctx = []
    ideas =  Ideas.get_all()
    for idea in ideas:
        skills = IdeasSkills.get_by_idea(idea)
        ctx.append({
            'idea': idea,
            'skills': [s.skill for s in skills]
        })

    return render_template('ideas.html', ctx=ctx)


@app.route('/ideas/<int:id>')
def idea(id):
    idea =  Ideas.by_id(id)
    skills = IdeasSkills.get_by_idea(idea)
    joined = TeamUps.by_idea(id)

    ctx = {
        'idea': idea,
        'skills': [s.skill for s in skills],
        'joined': joined
    }

    return render_template('idea.html', ctx=ctx)

@app.route('/skills/<id>')
def skill(id):
    ctx = {
        'ideas': Ideas.get_by_skill(id),
        'skill': Skills.by_id(id),
        'skilled': Persons.by_skill(id)
    }

    return render_template('skill.html', ctx=ctx)

@app.route('/api/digest')
def digest():
    items = []

    # no pitch, no team
    for user in Persons.non_active():
        suggested = Ideas.suggest_by_person(user)
        suggested_count = len(list(suggested))
        params = dict(user=user.user, count=suggested_count)

        if suggested_count == 1:
            msg_type = 'no_team_1_sugg'
            params['id'] = suggested.get().id
        elif suggested_count > 1:
            msg_type = 'no_team_much_sugg'
        else:
            msg_type = 'no_team_0_sugg'

        msg = settings.MESSAGES[msg_type].format(**params)
        items.append((email(user.user), msg))

    # much pitches
    for user in Persons.pitched_over_one():
        msg = settings.MESSAGES['pitch_much'].format(user=user.user, count=user.count)
        items.append((email(user.user), msg))

    # much joins
    for user in Persons.teamed_over_one():
        msg = settings.MESSAGES['team_much'].format(user=user.user, count=user.count)
        items.append((email(user.user), msg))

    for msg in items:
        send_hipchat_msg(*msg)

    return render_template('digest.html', ctx=items)