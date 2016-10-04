from nestor.app import app
from nestor.db import db
from nestor.routes import routes
from nestor.logger import logger
from nestor.config import DATABASE_URI

def create_app(testing=False):

    app.config.update(
        TESTING=testing,
        SQLALCHEMY_DATABASE_URI=DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=True
    )

    app.register_blueprint(routes)

    db.init_app(app)

    return app
