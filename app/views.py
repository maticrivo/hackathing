from app import app, settings, email, send_hipchat_msg
from flask import render_template, url_for, redirect, request
from models import *
from login import requires_login


@app.route('/')
@app.route('/projects')
def projects():
    ctx = {
        'skills': Skills.get_all_in_projects(),
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
    project = Projects.by_id(id)
    skills = ProjectsSkills.get_by_project(project)
    joined = ProjectsHackers.by_project(id)

    ctx = {
        'project': project,
        'skills': [s.skill for s in skills],
        'all_skills': Skills.get_all(),
        'joined': joined
    }

    return render_template('project.html', ctx=ctx)

@app.route('/projects/new')
@requires_login
def new_project():
    ctx = {
        'skills': Skills.get_all()
    }
    return render_template('new_project.html', ctx=ctx)

@app.route('/api/projects/new', methods=['POST'])
@requires_login
def api_new_project():
    # create project
    project = Projects.add(title=request.form['title'], description=request.form['description'])
    Skills.add(project_id=project.id, *request.form['skills'].split(','))
    return redirect(url_for('project', id=project.id))

@app.route('/api/join/<int:project_id>')
@requires_login
def api_leave(project_id):
    ProjectsHackers.add(project_id, current_user.id)
    return redirect(url_for('project', id=project_id))

@app.route('/api/leave/<int:project_id>')
@requires_login
def api_join(project_id):
    ProjectsHackers.remove(project_id, current_user.id)
    return redirect(url_for('project', id=project_id))


@app.route('/api/projects/<int:project_id>/skills/add', methods=['POST'])
def api_new_project_skill(project_id):
    Skills.add(project_id=project_id, *request.form['skills'].split(','))
    return redirect(url_for('project', id=project_id))


@app.route('/api/projects/<int:project_id>/skills/remove/<int:skill_id>')
def api_remove_project_skill(project_id, skill_id):
    ProjectsSkills.remove(project_id, skill_id)
    return redirect(url_for('project', id=project_id))

@app.route('/api/projects/<int:project_id>/edit', methods=['POST'])
def api_edit_project(project_id):
    return redirect(url_for('project', id=project_id))

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
    joined = [x.project for x in ProjectsHackers.by_hacker(hacker)]
    suggested = Projects.suggest_by_hacker(hacker)

    ctx = {
        'name': hacker.name,
        'email': hacker.user+'@everything.me',
        'user': hacker.user,
        'skills': [s.skill for s in skills],
        'all_skills': Skills.get_all(),
        'pitched': pitched,
        'joined': joined,
        'suggested': suggested
    }

    return render_template('hacker.html', ctx=ctx)


@app.route('/api/hackers/<hacker>/skills/add', methods=['POST'])
def api_new_hacker_skill(hacker):
    hacker = Hackers.by_user(hacker)
    Skills.add(hacker_id=hacker.id, *request.form['skills'].split(','))
    return redirect(url_for('hacker', hacker=hacker.user))


@app.route('/api/hackers/<hacker>/skills/remove/<int:skill_id>')
def api_remove_hacker_skill(hacker, skill_id):
    hacker = Hackers.by_user(hacker)
    HackersSkills.remove(hacker.id, skill_id)
    return redirect(url_for('hacker', hacker=hacker.user))


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


