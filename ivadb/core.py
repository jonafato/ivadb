from flask.ext.restful import Api
from flask.ext.security import Security
from flask.ext.sqlalchemy import SQLAlchemy


api = Api(prefix='/api/v1')
db = SQLAlchemy()
security = Security()
