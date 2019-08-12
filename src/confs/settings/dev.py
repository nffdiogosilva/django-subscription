from .base import *

ALLOWED_HOSTS = [
    '0.0.0.0',
]

INSTALLED_APPS += (
    # 'debug_toolbar',
)

LOGGING['loggers']['django'] = {
    'handlers': ['console'],
    'propagate': True,
    'level': 'INFO',
}