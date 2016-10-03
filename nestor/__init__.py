from nestor.app import app
from nestor.routes import routes
from nestor.logger import logger

def create_app():
    app.register_blueprint(routes)
    return app
