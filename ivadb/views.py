from functools import wraps

from flask import Blueprint, render_template, request
from flask.ext.restful import abort, fields, reqparse, marshal_with, Resource
from flask.ext.security import current_user

from .core import api, db
from .models import Actor, Character, Series
from .utils import fields_from_model


bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return render_template('index/index.html')


actor_fields = fields_from_model(Actor)
series_fields = fields_from_model(Series)
character_fields = fields_from_model(Character)
character_fields['actor'] = fields.Nested(actor_fields)
character_fields['series'] = fields.Nested(series_fields)

actor_parser = reqparse.RequestParser()
actor_parser.add_argument('name', type=str, required=True)

series_parser = reqparse.RequestParser()
series_parser.add_argument('name', type=str, required=True)
series_parser.add_argument('debut_year', type=int, required=True)

character_parser = reqparse.RequestParser()
character_parser.add_argument('name', type=str, required=True)
character_parser.add_argument('actor_id', type=int, required=True)
character_parser.add_argument('series_id', type=int, required=True)


def auth_to_modify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if (request.method in ('POST', 'PUT', 'DELETE') and
                not current_user.is_authenticated()):
            abort(401)
        return func(*args, **kwargs)
    return wrapper


class ActorDetailResource(Resource):
    method_decorators = [marshal_with(actor_fields), auth_to_modify]

    def get(self, actor_id):
        return Actor.query.get_or_404(actor_id)

    def delete(self, actor_id):
        actor = Actor.query.get(actor_id)
        if actor:
            db.session.delete(actor)
            db.session.commit()
        return '', 204

    def put(self, actor_id):
        args = actor_parser.parse_args()
        actor = Actor.query.get(actor_id)
        if not actor:
            actor = Actor(id=actor_id)
            db.session.add(actor)
        actor.name = args['name']
        db.session.commit()
        return actor


class ActorListResource(Resource):
    method_decorators = [marshal_with(actor_fields), auth_to_modify]

    def get(self):
        return Actor.query.all()

    def post(self):
        args = actor_parser.parse_args()
        actor = Actor(**args)
        db.session.add(actor)
        db.session.commit()
        return actor


class SeriesDetailResource(Resource):
    method_decorators = [marshal_with(series_fields), auth_to_modify]

    def get(self, series_id):
        return Series.query.get_or_404(series_id)

    def delete(self, series_id):
        series = Series.query.get(series_id)
        if series:
            db.session.delete(series)
            db.session.commit()
        return '', 204

    def put(self, series_id):
        args = series_parser.parse_args()
        series = Series.query.get(series_id)
        if not series:
            series = Series(id=series_id)
            db.session.add(series)
        series.name = args['name']
        series.debut_year = args['debut_year']
        db.session.commit()
        return series


class SeriesListResource(Resource):
    method_decorators = [marshal_with(series_fields), auth_to_modify]

    def get(self):
        return Series.query.all()

    def post(self):
        args = series_parser.parse_args()
        series = Series(**args)
        db.session.add(series)
        db.session.commit()
        return series


class CharacterDetailResource(Resource):
    method_decorators = [marshal_with(character_fields), auth_to_modify]

    def get(self, character_id):
        return Character.query.get_or_404(character_id)

    def delete(self, character_id):
        character = Character.query.get(character_id)
        if character:
            db.session.delete(character)
            db.session.commit()
        return '', 204

    def put(self, character_id):
        args = character_parser.parse_args()
        character = Character.query.get(character_id)
        if not character:
            character = Character(id=character_id)
            db.session.add(character)
        character.name = args['name']
        character.actor_id = args['actor_id']
        character.series_id = args['series_id']
        db.session.commit()
        return character


class CharacterListResource(Resource):
    method_decorators = [marshal_with(character_fields), auth_to_modify]

    def get(self):
        return Character.query.all()

    def post(self):
        args = character_parser.parse_args()
        character = Character(**args)
        db.session.add(character)
        db.session.commit()
        return character


api.add_resource(ActorListResource, '/actors/')
api.add_resource(ActorDetailResource, '/actors/<int:actor_id>/')
api.add_resource(SeriesListResource, '/series/')
api.add_resource(SeriesDetailResource, '/series/<int:series_id>/')
api.add_resource(CharacterListResource, '/characters/')
api.add_resource(CharacterDetailResource, '/characters/<int:character_id>/')
