import os

ENVIRONMENT = os.getenv('FLASK_ENVIRONMENT', 'development')
PORT = os.getenv('PORT', 5000)
