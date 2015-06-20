from app import app, settings, email, send_hipchat_msg
from models import *
from flask import render_template


@app.route('/')
@app.route('/projects')
def projects():
    ctx = {
        'skills': Skills.get_all(),
        'projects': []
    }
    for project in Projects.get_all():
        ctx['projects'].append({
            'project': project,
            'skills': [s.skill for s in ProjectsSkills.get_by_project(project)]
        })

    return render_template('projects.html', ctx=ctx)


@app.route('/projects/<int:id>')
def project(id):
    project =  Projects.by_id(id)
    skills = ProjectsSkills.get_by_project(project)
    joined = TeamUps.by_project(id)

    ctx = {
        'project': project,
        'skills': [s.skill for s in skills],
        'joined': joined
    }

    return render_template('project.html', ctx=ctx)

@app.route('/projects/<project_id>/join')
def join(project_id):
    pass

@app.route('/hackers')
def hackers():
    ctx = {
        'hackers': Hackers.get_all()
    }

    return render_template('hackers.html', ctx=ctx)

@app.route('/hackers/<hacker>')
def hacker(hacker):
    hacker = Hackers.by_user(hacker)
    skills = HackersSkills.by_hacker(hacker)
    pitched = Projects.by_hacker(hacker)
    joined = [x.project for x in TeamUps.by_hacker(hacker)]
    suggested = Projects.suggest_by_hacker(hacker)

    ctx = {
        'name': hacker.name,
        'email': hacker.user+'@everything.me',
        'skills': [s.skill for s in skills],
        'pitched': pitched,
        'joined': joined,
        'suggested': suggested
    }

    return render_template('hacker.html', ctx=ctx)


@app.route('/skills/<id>')
def skill(id):
    ctx = {
        'projects': Projects.get_by_skill(id),
        'skill': Skills.by_id(id),
        'skilled': Hackers.by_skill(id)
    }

    return render_template('skill.html', ctx=ctx)


@app.route('/api/digest')
def digest():
    items = []

    # no pitch, no team
    for user in Hackers.non_active():
        suggested = Projects.suggest_by_hacker(user)
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
    for user in Hackers.pitched_over_one():
        msg = settings.MESSAGES['pitch_much'].format(user=user.user, count=user.count)
        items.append((email(user.user), msg))

    # much joins
    for user in Hackers.teamed_over_one():
        msg = settings.MESSAGES['team_much'].format(user=user.user, count=user.count)
        items.append((email(user.user), msg))

    for msg in items:
        send_hipchat_msg(*msg)

    return render_template('digest.html', ctx=items)