from flask.ext.security import RoleMixin, UserMixin
from sqlalchemy_defaults import Column

from .core import db


roles_users = db.Table(
    'roles_users',
    Column('user_id', db.Integer, db.ForeignKey('user.id')),
    Column('role_id', db.Integer, db.ForeignKey('role.id')),
)


class Role(db.Model, RoleMixin):
    """Flask-Security Role model."""
    id = Column(db.Integer, primary_key=True)
    created = Column(db.DateTime, auto_now=True)
    name = Column(db.Unicode, unique=True)
    description = Column(db.UnicodeText)


class User(db.Model, UserMixin):
    """Flask-Security User model."""
    id = Column(db.Integer, primary_key=True)
    created = Column(db.DateTime, auto_now=True)
    email = Column(db.Unicode)
    password = Column(db.String(255))
    active = Column(db.Boolean, default=True, nullable=False)
    confirmed_at = Column(db.DateTime)
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'),
    )


class Actor(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.Unicode)


class Series(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.Unicode)
    debut_year = Column(db.Integer, min=1936)  # min = first broadcast date


class Character(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.Unicode)

    actor_id = Column(db.Integer, db.ForeignKey('actor.id'))
    actor = db.relationship(
        'Actor',
        backref=db.backref('actors', lazy='dynamic'),
    )
    series_id = Column(db.Integer, db.ForeignKey('series.id'))
    series = db.relationship(
        'Series',
        backref=db.backref('characters', lazy='dynamic'),
    )
