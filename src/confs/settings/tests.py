from .base import *

SECRET_KEY='lHnABhdr8+:WUDV{P5g|dA%dl[K3w#,2/7EpC3br2o`5uHNZfa'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'memory:'
    }
}
