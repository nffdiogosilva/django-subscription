from .base import *

ALLOWED_HOSTS = [
    '*',
]

INSTALLED_APPS += (
    # 'debug_toolbar',
)

LOGGING['loggers']['django'] = {
    'handlers': ['console'],
    'propagate': True,
    'level': 'INFO',
}