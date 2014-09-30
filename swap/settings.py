"""
Django settings for swap project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6*8olp0r1(&%f+9)r&%wr&^6mmsv(w#6-kfa&twq52$ys4x#&)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

#{'ISIS2304361420' : 'entrambac1ddf', 'ISIS2304031420' : 'ciertib4789'}

USER_SC = ('ISIS2304361420', 'entrambac1ddf')
USER_JC = ('ISIS2304031420', 'ciertib4789')
CURRENT_USER = USER_JC

ALLOWED_USERS = {'sc.valencia' : USER_SC, 'jc.bages' : USER_JC}


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'actives',
    'genericusers',
    'passives',
    'solicitudes',
    'swaptransactions',
    'vals',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'swap.urls'

WSGI_APPLICATION = 'swap.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default' : {
        'AUTOCOMMIT': False,
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'prod',
        'USER': USER_JC[0],
        'PASSWORD': USER_JC[1],
        'HOST': 'prod.oracle.virtual.uniandes.edu.co',
        'PORT': '1531',
    },
    'scvalencia': {
        'AUTOCOMMIT': False,
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'prod',
        'USER': USER_SC[0],
        'PASSWORD': USER_SC[1],
        'HOST': 'prod.oracle.virtual.uniandes.edu.co',
        'PORT': '1531',
    },
    'jcbages': {
        'AUTOCOMMIT': False,
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'prod',
        'USER': USER_JC[0],
        'PASSWORD': USER_JC[1],
        'HOST': 'prod.oracle.virtual.uniandes.edu.co',
        'PORT': '1531',
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Cache config

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Session config

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'