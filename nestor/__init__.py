from nestor.app import app
from nestor.db import db
from nestor.routes import routes
from nestor.logger import logger
from nestor.config import DATABASE_URI
from nestor.errors import NestorException

def create_app(testing=False):

    app.config.update(
        TESTING=testing,
        SQLALCHEMY_DATABASE_URI=DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=True
    )

    app.register_blueprint(routes)

    @app.errorhandler(NestorException)
    def error_handler(exception):
        return exception.unpack()

    db.init_app(app)
    app.app_context().push()

    return app
