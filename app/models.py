import peewee
from db import db
from settings import CURRENT_HACKATHING
from flask_login import current_user


class DatabaseModel(peewee.Model):
    class Meta:
        database = db.database


class Hackers(DatabaseModel):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(unique=True, null=False)
    user = peewee.CharField(unique=True, null=False)
    active = peewee.BooleanField(default=1)

    @classmethod
    def get_all(cls):
        return cls.select().filter(cls.active == 1)

    @classmethod
    def by_user(cls, user):
        try:
            return cls.get(cls.user == user)
        except peewee.DoesNotExist:
            return None

    @classmethod
    def non_active(cls):
        return cls.select().where(~cls.id << Projects.select(Projects.hacker))

    @classmethod
    def pitched_over_one(cls):
        return cls.select(cls.id, cls.user, peewee.fn.Count(1).alias('count'))\
                   .join(Projects)\
                   .group_by(cls)\
                   .having(peewee.fn.Count(1) > 1)

    @classmethod
    def teamed_over_one(cls):
        return cls.select(cls.id, cls.user, peewee.fn.Count(1).alias('count'))\
               .join(ProjectsHackers)\
               .group_by(cls)\
               .having(peewee.fn.Count(1) > 1)

    @classmethod
    def by_skill(cls, skill_id):
        return cls.select(cls, HackersSkills)\
                  .join(HackersSkills, on=(cls.id == HackersSkills.hacker))\
                  .where(HackersSkills.skill == skill_id)



class Skills(DatabaseModel):
    id = peewee.IntegerField(primary_key=True)
    title = peewee.CharField(unique=True, null=False)

    @classmethod
    def by_id(cls, id):
        return cls.get(cls.id == id)

    @classmethod
    def get_all(cls):
        return cls.select()

    @classmethod
    def get_all_in_projects(cls):
        return cls.select()\
            .join(ProjectsSkills, on=(cls.id == ProjectsSkills.skill))\
            .group_by(cls.id)

    @classmethod
    def add(cls, *titles, **kwargs):
        # get ids (create if title not found)
        ids = []
        for title in titles:
            title = title.strip().lower()
            try:
                data = cls.get(title=title)
            except cls.DoesNotExist:
                cls.create(title=title)
                data = cls.get(title=title)
            ids.append(data.id)

        # attach to project
        project_id = kwargs.get('project_id', None)
        if project_id:
            ProjectsSkills.add(project_id, *ids)


class HackersSkills(DatabaseModel):
    hacker = peewee.ForeignKeyField(Hackers)
    skill = peewee.ForeignKeyField(Skills)

    class Meta:
        db_table = 'hackers_skills'

    @classmethod
    def by_hacker(cls, hacker):
        return cls.select(cls.hacker, Skills.title)\
                  .join(Skills, on=(cls.skill == Skills.id))\
                  .where(cls.hacker == hacker.id)\
                  .select()


class Projects(DatabaseModel):
    id = peewee.PrimaryKeyField()
    hackathing_id = peewee.IntegerField()
    title = peewee.CharField()
    hacker = peewee.ForeignKeyField(Hackers)
    description = peewee.TextField()

    @classmethod
    def get_all(cls):
        return cls.select(cls.title, cls.title, cls.description, Hackers.id, Hackers.name)\
               .where(cls.hackathing_id == CURRENT_HACKATHING)\
               .join(Hackers, on=(cls.hacker == Hackers.id))\
               .select()

    @classmethod
    def by_hacker(cls, hacker):
        return cls.select(cls.id, cls.title, cls.description)\
                .where(cls.hacker == hacker.id)\
                .where(cls.hackathing_id == CURRENT_HACKATHING)

    @classmethod
    def by_id(cls, id):
        return cls.get(cls.id == id)

    @classmethod
    def suggest_by_hacker(cls, hacker):
        # projects hacker already joined
        already_joined = ProjectsHackers.select(ProjectsHackers.project).where(ProjectsHackers.hacker == hacker.id)

        # projects that require skills that match at least one of hacker's skills
        match_skills = cls.select(cls.id)\
                       .join(ProjectsSkills, on=(cls.id == ProjectsSkills.project))\
                       .join(HackersSkills, on=(ProjectsSkills.skill == HackersSkills.skill))\
                       .where(HackersSkills.hacker == hacker.id)
        # add them up
        return cls.select(cls.id, cls.title)\
                    .where(cls.hackathing_id == CURRENT_HACKATHING)\
                    .where(~cls.id << already_joined)\
                    .where(cls.id << match_skills)

    @classmethod
    def get_by_skill(cls, skill_id):
        return cls.select(cls.id, cls.title, ProjectsSkills.project)\
                    .join(ProjectsSkills)\
                    .where(ProjectsSkills.skill == skill_id)

    @classmethod
    def add(cls, **kwargs):
        project = cls.create(
            title=kwargs.get('title'),
            description=kwargs.get('description'),
            hackathing_id=CURRENT_HACKATHING,
            hacker=current_user.id
        )
        project.save()
        return project


class ProjectsHackers(DatabaseModel):
    hacker = peewee.ForeignKeyField(Hackers)
    project = peewee.ForeignKeyField(Projects)

    class Meta:
        db_table = 'projects_hackers'
        primary_key = peewee.CompositeKey('hacker', 'project')

    @classmethod
    def by_hacker(cls, hacker):
        return cls.select(cls.project, cls.hacker, Projects.title)\
                  .join(Projects, on=(cls.project == Projects.id))\
                  .where(cls.hacker == hacker.id)\
                  .where(Projects.hackathing_id == CURRENT_HACKATHING)

    @classmethod
    def by_project(cls, id):
        return cls.select(cls.project, Hackers.name, Hackers.id, Hackers.user)\
                  .join(Hackers, on=(Hackers.id == cls.hacker))\
                  .where(cls.project == id)

    @classmethod
    def add(cls, project_id, hacker_id):
        return cls.create(project=project_id, hacker=hacker_id)

    @classmethod
    def remove(cls, project_id, hacker_id):
        return cls.delete().where(cls.project == project_id, cls.hacker == hacker_id).execute()

class ProjectsSkills(DatabaseModel):
    project = peewee.ForeignKeyField(Projects)
    skill = peewee.ForeignKeyField(Skills)

    class Meta:
        db_table = 'projects_skills'
        primary_key = peewee.CompositeKey('project', 'skill')

    @classmethod
    def get_by_project(cls, project):
        return cls.select(cls.project, Projects.title)\
                   .join(Projects, on=(cls.project == Projects.id))\
                   .where(cls.project == project.id)\
                   .select()

    @classmethod
    def add(cls, project_id, *skill_ids):
        for skill_id in skill_ids:
            cls.create(project=project_id, skill=skill_id)
