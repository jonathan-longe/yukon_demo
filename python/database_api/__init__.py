from flask import Flask
from python.database_api.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(config_class=Config):
    application = Flask(__name__)
    application.config.from_object(config_class)

    db.init_app(application)
    ma.init_app(application)
    migrate.init_app(application, db, directory=Config.MIGRATION_DIRECTORY)

    from python.database_api import routes
    application.register_blueprint(routes.bp)

    return application
