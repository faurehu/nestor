import os

ENVIRONMENT = os.getenv('FLASK_ENVIRONMENT', 'dev')

POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'admin')
POSTGRES_HOSTNAME = os.getenv('POSTGRES_HOSTNAME', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(POSTGRES_USER,
                                                    POSTGRES_PASSWORD,
                                                    POSTGRES_HOSTNAME,
                                                    POSTGRES_PORT,
                                                    ENVIRONMENT)
