from django.shortcuts import render, redirect
from django.db import connection

import os
import datetime


def login(request):
    if request.method == 'POST':
        form_data = request.POST
        valid, error = is_valid(form_data)
        params = {'form_data': form_data, 'error': error}
        if valid:
            response = '#INSERT RESPONSE'
            set_cookie(response, key, value, days_expire=7)
        else:
            return render(request, 'login.html', params) 
    else:
        form_data = {}
        params = {'form_data': form_data}
        return render(request, 'login.html', params)

def validate_user(username, password):
    cursor = connection.cursor()
    query = "SELECT * FROM genericuser WHERE login = %s", [username]
    result_set = cursor.execute("SELECT * FROM genericuser WHERE login = %s", [username])
    if result_set.rowcount != 1:
        return False, 'No existe el usuario ' + username
    else:
        query = "SELECT * FROM genericuser WHERE login = %s and password = %s", [username, password]
        result_set = cursor.execute("SELECT * FROM genericuser WHERE login = %s and password = %s", [username, password])
        if result_set.rowcount != 1:
            return False, 'Contrasenia invalida'
        else:
            return True, ''
    return False, 'Bad coders!!' # Should not happen

def is_valid(form_data):
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

def set_cookie(response, key, value, days_expire = 7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60 
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() +
                  datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
        domain = settings.SESSION_COOKIE_DOMAIN
        secure = settings.SESSION_COOKIE_SECURE or None
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=domain, secure=secure)