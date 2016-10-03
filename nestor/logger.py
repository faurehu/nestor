import coloredlogs
import logging
from logging.config import dictConfig

logging_config = {
    "version": 1,
    "formatters": {
        'f': {'format':
              '%(asctime)s %(levelname)-8s %(message)s'}
    },
    "handlers": {
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
    },
    "root": {
        'handlers': ['h'],
        'level': logging.DEBUG
    }
}

dictConfig(logging_config)
coloredlogs.install(level='DEBUG')

logger = logging.getLogger('nestor')
