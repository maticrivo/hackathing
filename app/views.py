from app import app, settings, email, send_hipchat_msg
from models import *
from flask import render_template

@app.route('/ranbena')
def hello_world():
    return 'Hello World!'

@app.route('/hackers/<hacker>')
def hacker(hacker):
    person = Persons.by_user(hacker)
    skills = PersonsSkills.by_person(person)
    pitched = Ideas.by_person(person)
    joined = [x.idea for x in TeamUps.by_person(person)]
    suggested = Ideas.suggest_by_person(person)

    ctx = {
        'name': person.name,
        'email': person.user+'@everything.me',
        'skills': [s.skill for s in skills],
        'pitched': pitched,
        'joined': joined,
        'suggested': suggested
    }

    return render_template('hacker.html', ctx=ctx)

@app.route('/')
@app.route('/projects')
def projects():
    ctx = []
    projects =  Ideas.get_all()
    for project in projects:
        skills = IdeasSkills.get_by_idea(project)
        ctx.append({
            'idea': project,
            'skills': [s.skill for s in skills]
        })

    return render_template('projects.html', ctx=ctx)


@app.route('/projects/<int:id>')
def project(id):
    project =  Ideas.by_id(id)
    skills = IdeasSkills.get_by_idea(project)
    joined = TeamUps.by_idea(id)

    ctx = {
        'idea': project,
        'skills': [s.skill for s in skills],
        'joined': joined
    }

    return render_template('project.html', ctx=ctx)

@app.route('/skills/<id>')
def skill(id):
    ctx = {
        'ideas': Ideas.get_by_skill(id),
        'skill': Skills.by_id(id),
        'skilled': Persons.by_skill(id)
    }

    return render_template('skill.html', ctx=ctx)

@app.route('/projects/<project_id>/join')
def join(project_id):
    pass

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