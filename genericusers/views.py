from django.shortcuts import render, redirect

import os
import hashlib
import datetime
from django.db import connection
from swap import settings
from swap.settings import SECRET_KEY


def home(request):
    key = 'username'
    value = request.COOKIES.get(key)
    key_check = '%s_check' % key
    value_check = request.COOKIES.get(key_check)
    if is_valid_cookie(value, value_check):
        return render(request, 'user_home.html')
    else:
        response = render(request, 'home.html')
        set_cookie(response, key, '')
        set_cookie(response, key_check, '')
        return response

def login(request):
    if request.method == 'POST':
        form_data = request.POST
        username = form_data.get('username')
        password = form_data.get('password')
        valid, error = is_valid_form(form_data)
        if valid:
            key = 'username'
            value = form_data.get(key)
            key_check = '%s_check' % key
            value_check = get_cookie_value(value)
            response = home(request)
            set_cookie(response, key, value)
            set_cookie(response, key_check, value_check)
            return response
        else:
            params = {
                'username': username,
                'password': password,
                'error': error,
            }
            return render(request, 'login.html', params)
    else:
        key = 'username'
        value = request.COOKIES.get(key)
        key_check = '%s_check' % key
        value_check = request.COOKIES.get(key_check)
        if is_valid_cookie(value, value_check):
            return home(request)
        else:
            params = {
                'username': '',
                'password': '',
                'error': '',
            }
            response = render(request, 'login.html', params)
            set_cookie(response, key, '')
            set_cookie(response, key_check, '')
            return response

def validate_user(username, password):
    flag = False
    msg = 'Bad coders!!!'
    cursor = connection.cursor()
    query = "SELECT * FROM genericuser WHERE login = %s", [username]
    result_set = cursor.execute("SELECT * FROM genericuser WHERE login = %s", [username])
    if result_set.rowcount != 1:
        flag = False; msg = 'No existe el usuario ' + username
    else:
        query = "SELECT * FROM genericuser WHERE login = %s and password = %s", [username, password]
        result_set = cursor.execute("SELECT * FROM genericuser WHERE login = %s and password = %s", [username, password])
        if result_set.rowcount != 1:
            flag = False; msg = 'Clave invalida'
        else:
            flag = True
            msg = 'Best coders ever!!'
    connection.close()
    return flag, msg # Should not happen

def is_valid_form(form_data):
    username = form_data.get('username')
    password = form_data.get('password')
    if username and password:
        return validate_user(username, password)
    elif not username and password:
        return False, 'El nombre de usuario no puede estar vacio.'
    elif username and not password:
        return False, 'La clave no puede estar vacia.'
    else:
        return False, 'Los campos no pueden estar vacios.'

def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60 
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() +
                  datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
        domain = settings.SESSION_COOKIE_DOMAIN
        secure = settings.SESSION_COOKIE_SECURE or None
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=domain, secure=secure)

def get_cookie_value(value):
    value = '%s%s' % (SECRET_KEY, value)
    value = hashlib.sha512(value).hexdigest()
    return value

def is_valid_cookie(value, value_check):
    this_value_check = get_cookie_value(value)
    return this_value_check == value_check