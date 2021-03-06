from app import app
# from app import settings, email, send_hipchat_msg
from flask import render_template, url_for, redirect, request, flash
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
@requires_login
def api_new_project_skill(project_id):
    Skills.add(project_id=project_id, *request.form['skills'].split(','))
    return redirect(url_for('project', id=project_id))


@app.route('/api/projects/<int:project_id>/skills/remove/<int:skill_id>')
@requires_login
def api_remove_project_skill(project_id, skill_id):
    ProjectsSkills.remove(project_id, skill_id)
    return redirect(url_for('project', id=project_id))

@app.route('/api/projects/<int:project_id>/delete')
@requires_login
def api_delete_project(project_id):
    project = Projects.by_id(project_id)
    if project.hacker_id == current_user.id:
        Projects.remove(project_id)
        flash('Project %s deleted.' % project.title, 'success')
        return redirect(url_for('projects'))
    else:
        flash('Only %s is authorized to delete this project.' % project.hacker.name, 'error')
        return redirect(url_for('project', id=project_id))

@app.route('/api/projects/<int:project_id>/edit', methods=['POST'])
@requires_login
def api_edit_project(project_id):
    project = Projects.by_id(project_id)
    if project.hacker_id == current_user.id:
        q = Projects.update(title=request.form['title'], description=request.form['description']).where(Projects.id == project_id)
        q.execute()
        flash('Project was successfully updated.', 'success')
    else:
        flash('Only %s is authorized to delete this project.' % project.hacker.name, 'error')

    return redirect(url_for('project', id=project_id))


@app.route('/hackers')
def hackers():
    ctx = {
        'hackers': Hackers.get_all()
    }

    return render_template('hackers.html', ctx=ctx)

@app.route('/hackers/<hacker_user>')
def hacker(hacker_user):
    hacker = Hackers.by_user(hacker_user)
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
@requires_login
def api_new_hacker_skill(hacker):
    hacker = Hackers.by_user(hacker)
    Skills.add(hacker_id=hacker.id, *request.form['skills'].split(','))
    return redirect(url_for('hacker', hacker_user=hacker.user))


@app.route('/api/hackers/<hacker>/skills/remove/<int:skill_id>')
@requires_login
def api_remove_hacker_skill(hacker, skill_id):
    hacker = Hackers.by_user(hacker)
    HackersSkills.remove(hacker.id, skill_id)
    return redirect(url_for('hacker', hacker_user=hacker.user))


@app.route('/skills/<id>')
def skill(id):
    ctx = {
        'projects': Projects.get_by_skill(id),
        'skill': Skills.by_id(id),
        'skilled': Hackers.by_skill(id)
    }

    return render_template('skill.html', ctx=ctx)

@app.route('/agenda')
def agenda():
    return render_template('agenda.html', ctx={})

@app.route('/sessions')
@requires_login
def sessions():
    ctx = {
        'sessions': Sessions.get_all()
    }

    return render_template('sessions.html', ctx=ctx)

@app.route('/api/sessions/new', methods=['POST'])
@app.route('/api/sessions/edit', methods=['POST'])
@requires_login
def api_edit_session():
    session_id = request.form['session_id']
    if session_id:
        session = Sessions.by_id(int(session_id))
        if session.hacker_id is current_user.id:
            Sessions.edit(
                session_id=session_id,
                title=request.form['title'],
                description=request.form['description']
            )
    else:
        Sessions.add(
            title=request.form['title'],
            description=request.form['description']
        )

    return redirect(url_for('sessions'))

@app.route('/api/sessions/<int:session_id>/delete')
@requires_login
def api_delete_session(session_id):
    session = Sessions.by_id(int(session_id))
    if session.hacker_id is current_user.id:
        Sessions.remove(session_id)
        flash('Session %s deleted.' % session.title, 'success')
    else:
        flash('Only %s is authorized to delete this session.' % project.hacker.name, 'error')

    return redirect(url_for('sessions'))

@app.route('/api/vote/<int:session_id>')
@requires_login
def api_session_vote(session_id):
    SessionsHackers.vote(session_id)
    return redirect(url_for('sessions'))

@app.route('/api/unvote/<int:session_id>')
@requires_login
def api_session_unvote(session_id):
    SessionsHackers.unvote(session_id)
    return redirect(url_for('sessions'))


# @app.route('/api/digest')
# def digest():
#     items = []
#
#     # no pitch, no team
#     for user in Hackers.non_active():
#         suggested = Projects.suggest_by_hacker(user)
#         suggested_count = len(list(suggested))
#         params = dict(user=user.user, count=suggested_count)
#
#         if suggested_count == 1:
#             msg_type = 'no_team_1_sugg'
#             params['id'] = suggested.get().id
#         elif suggested_count > 1:
#             msg_type = 'no_team_much_sugg'
#         else:
#             msg_type = 'no_team_0_sugg'
#
#         msg = settings.MESSAGES[msg_type].format(**params)
#         items.append((email(user.user), msg))
#
#     # much pitches
#     for user in Hackers.pitched_over_one():
#         msg = settings.MESSAGES['pitch_much'].format(user=user.user, count=user.count)
#         items.append((email(user.user), msg))
#
#     # much joins
#     for user in Hackers.teamed_over_one():
#         msg = settings.MESSAGES['team_much'].format(user=user.user, count=user.count)
#         items.append((email(user.user), msg))
#
#     for msg in items:
#         send_hipchat_msg(*msg)
#
#     return render_template('digest.html', ctx=items)


