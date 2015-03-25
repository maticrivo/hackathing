import peewee
from db import db


class DatabaseModel(peewee.Model):
    class Meta:
        database = db.database


class Persons(DatabaseModel):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(unique=True, null=False)
    user = peewee.CharField(unique=True, null=False)
    hipchat_handle = peewee.CharField(unique=True, null=False)

    @classmethod
    def by_user(cls, user):
        try:
            return cls.get(cls.user == user)
        except peewee.DoesNotExist:
            return None


class Skills(DatabaseModel):
    id = peewee.IntegerField(primary_key=True)
    title = peewee.CharField(unique=True, null=False)


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
        return cls.select(cls.title, cls.description).where(cls.pitcher == person.id)

    @classmethod
    def by_id(cls, id):
        return cls.get(cls.id== id)


class TeamUps(DatabaseModel):
    person = peewee.ForeignKeyField(Persons)
    idea = peewee.ForeignKeyField(Ideas)

    class Meta:
        db_table = 'team_ups'
        primary_key = peewee.CompositeKey('person', 'idea')

    @classmethod
    def by_person(cls, person):
        return cls.select(cls.person, Ideas.title)\
                  .join(Ideas, on=(cls.idea == Ideas.id))\
                  .where(cls.person == person.id)\
                  .select()


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