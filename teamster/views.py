from teamster import app
from models import *
from flask import render_template

@app.route('/ranbena')
def hello_world():
    return 'Hello World!'

@app.route('/user/<user>')
def user(user):
    person = Persons.by_user(user)
    skills = PersonsSkills.by_person(person)
    pitches = Ideas.by_person(person)
    joined = TeamUps.by_person(person)

    ctx = {
        'name': person.name,
        'skills': [s.skill.title for s in skills],
        'pitches': pitches,
        'joined': [j.idea.title for j in joined]
    }

    return render_template('user.html', ctx=ctx)

@app.route('/ideas')
def ideas():
    ctx = []
    ideas =  Ideas.get_all()
    for idea in ideas:
        skills = IdeasSkills.get_by_idea(idea)
        ctx.append({
            'idea': idea,
            'skills': [s.skill.title for s in skills]
        })

    return render_template('ideas.html', ctx=ctx)


@app.route('/ideas/<int:id>')
def idea(id):
    idea =  Ideas.by_id(id)
    skills = IdeasSkills.get_by_idea(idea)
    ctx = {
        'idea': idea,
        'skills': [s.skill.title for s in skills]
    }

    return render_template('idea.html', ctx=ctx)