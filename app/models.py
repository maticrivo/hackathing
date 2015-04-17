import peewee
from db import db


class DatabaseModel(peewee.Model):
    class Meta:
        database = db.database


class Persons(DatabaseModel):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(unique=True, null=False)
    user = peewee.CharField(unique=True, null=False)

    @classmethod
    def by_user(cls, user):
        try:
            return cls.get(cls.user == user)
        except peewee.DoesNotExist:
            return None

    @classmethod
    def non_active(cls):
        return cls.select().where(~cls.id << Ideas.select(Ideas.pitcher))

    @classmethod
    def pitched_over_one(cls):
        return cls.select(cls.id, cls.user, peewee.fn.Count(1).alias('count'))\
                   .join(Ideas)\
                   .group_by(cls)\
                   .having(peewee.fn.Count(1) > 1)

    @classmethod
    def teamed_over_one(cls):
        return cls.select(cls.id, cls.user, peewee.fn.Count(1).alias('count'))\
               .join(TeamUps)\
               .group_by(cls)\
               .having(peewee.fn.Count(1) > 1)

    @classmethod
    def by_skill(cls, skill_id):
        return cls.select(cls, PersonsSkills)\
                  .join(PersonsSkills, on=(cls.id == PersonsSkills.person))\
                  .where(PersonsSkills.skill == skill_id)


class Skills(DatabaseModel):
    id = peewee.IntegerField(primary_key=True)
    title = peewee.CharField(unique=True, null=False)

    @classmethod
    def by_id(cls, id):
        return cls.get(cls.id == id)

    @classmethod
    def get_all(cls):
        return cls.select(cls.id, cls.title, peewee.fn.Count(1).alias('count'))\
                           .join(Ideas)\
                           .group_by(cls)\
                           .having(peewee.fn.Count(1) > 1)


class PersonsSkills(DatabaseModel):
    person = peewee.ForeignKeyField(Persons)
    skill = peewee.ForeignKeyField(Skills)

    class Meta:
        db_table = 'persons_skills'

    @classmethod
    def by_person(cls, person):
        return cls.select(cls.person, Skills.title)\
                  .join(Skills, on=(cls.skill == Skills.id))\
                  .where(cls.person == person.id)\
                  .select()


class Ideas(DatabaseModel):
    id = peewee.PrimaryKeyField()
    hackathing_id = peewee.IntegerField()
    title = peewee.CharField()
    pitcher = peewee.ForeignKeyField(Persons)
    description = peewee.TextField()

    @classmethod
    def get_all(cls):
        return cls.select(cls.title, cls.title, cls.description, Persons.id, Persons.name)\
               .join(Persons, on=(cls.pitcher == Persons.id))\
               .select()

    @classmethod
    def by_person(cls, person):
        return cls.select(cls.id, cls.title, cls.description).where(cls.pitcher == person.id)

    @classmethod
    def by_id(cls, id):
        return cls.get(cls.id== id)

    @classmethod
    def suggest_by_person(cls, person):
        # ideas person already joined
        already_joined = TeamUps.select(TeamUps.idea).where(TeamUps.person == person.id)
        # ideas that require skills that match at least one of person's skills
        match_skills = cls.select(cls.id)\
                       .join(IdeasSkills, on=(cls.id == IdeasSkills.idea))\
                       .join(PersonsSkills, on=(IdeasSkills.skill == PersonsSkills.skill))\
                       .where(PersonsSkills.person == person.id)
        # add them up
        return cls.select(cls.id, cls.title).where(~cls.id << already_joined).where(cls.id << match_skills)

    @classmethod
    def get_by_skill(cls, skill_id):
        return cls.select(cls.id, cls.title, IdeasSkills.idea).join(IdeasSkills).where(IdeasSkills.skill == skill_id)


class TeamUps(DatabaseModel):
    person = peewee.ForeignKeyField(Persons)
    idea = peewee.ForeignKeyField(Ideas)

    class Meta:
        db_table = 'team_ups'
        primary_key = peewee.CompositeKey('person', 'idea')

    @classmethod
    def by_person(cls, person):
        return cls.select(cls.idea, cls.person, Ideas.title)\
                  .join(Ideas, on=(cls.idea == Ideas.id))\
                  .where(cls.person == person.id)\
                  .select()

    @classmethod
    def by_idea(cls, id):
        return cls.select(cls.idea, Persons.name, Persons.id, Persons.user)\
                  .join(Persons, on=(Persons.id == cls.person))\
                  .where(cls.idea == id)


class IdeasSkills(DatabaseModel):
    idea = peewee.ForeignKeyField(Ideas)
    skill = peewee.ForeignKeyField(Skills)
    quantity = peewee.IntegerField()

    class Meta:
        db_table = 'ideas_skills'
        primary_key = peewee.CompositeKey('idea', 'skill')

    @classmethod
    def get_by_idea(cls, idea):
        return cls.select(cls.idea, Ideas.title)\
                   .join(Ideas, on=(cls.idea == Ideas.id))\
                   .where(cls.idea == idea.id)\
                   .select()