from nestor.app import app
from nestor.routes import routes
from nestor.logger import logger

def create_app(testing=False):

    app.config.update(
        TESTING=testing
    )

    app.register_blueprint(routes)
    return app
