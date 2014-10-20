#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Django settings for swap project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import User
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SERVER = 'prod.oracle.virtual.uniandes.edu.co'
PORT = '1531'
SID = 'prod'
BACKEND = 'django.db.backends.oracle'
allowed_users = ('ISIS2304361420', 'ISIS2304031420') # Me: 361420, JC: 031420
passwords = {'ISIS2304361420' : 'entrambac1ddf', 'ISIS2304031420' : 'ciertib4789'}

current_user = None
user_code = None
user_flag = '03'

if user_flag == '36':
    #Sebastián Valencia Calderón
    username = allowed_users[0]
    password = passwords[allowed_users[0]]
    current_user = User.User(username, password)
elif user_flag == '03':
    # Juan Bages Prada
    username = allowed_users[1]
    password = passwords[allowed_users[1]]
    current_user = User.User(username, password)

print current_user

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q@y-&8v7qic+9ghr4tecg7rb(^r#^6y7ht*3bjoh^t!#x$5hi_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


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
    'investors',
    'news',
    'offerants',
    'passives',
    'portfolios',
    'rest_framework',
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
        'AUTOCOMMIT': True,
        'ENGINE': BACKEND,
        'NAME': SID,
        'USER': current_user.username,
        'PASSWORD': current_user.password,
        'HOST': SERVER,
        'PORT': PORT,
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

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Session config

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers

ALLOWED_HOSTS = ['*']