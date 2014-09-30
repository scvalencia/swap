from django.shortcuts import render, redirect

import os
import hashlib
import datetime
import genericuser
from django.db import connection
from swap import settings
from swap.settings import SECRET_KEY
from datetime import datetime


def home(request):
    user = get_user(request.session.get('username'))
    print user
    if user:
        params = {'user': user}
        return render(request, 'user_home.html', params)
    else:
        remove_user_session(request)
        return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_again = request.POST.get('repeat_password')
        valid, error = register_user(username, password, password_again)
        if valid:
            request.session['username'] = username
            return redirect('/users/home/')
        else:
            params = {
                'username': username,
                'error': error,
            }
            return render(request, 'signup.html', params)
    else:
        print 'user', request.session.get('username')
        if request.session.get('username'):
            user = get_user(request.POST.get('username'))
            if user: return redirect('/users/home/')
        remove_user_session(request)
        params = {
            'username': '',
            'password': '',
            'error': '',
        }
        return render(request, 'signup.html', params)

def login(request):
    if request.method == 'POST':
        valid, error = is_valid_form(request.POST)
        if valid:
            request.session['username'] = request.POST.get('username')
            return redirect('/users/home/')
        else:
            params = {
                'username': request.POST.get('username'),
                'password': request.POST.get('password'),
                'error': error,
            }
            return render(request, 'login.html', params)
    else:
        print 'user', request.session.get('username')
        if request.session.get('username'):
            user = get_user(request.POST.get('username'))
            if user: return redirect('/users/home/')
        remove_user_session(request)
        params = {
            'username': '',
            'password': '',
            'error': '',
        }
        return render(request, 'login.html', params)

def remove_user_session(request):
    if 'username' in request: del request.session['username']

def validate_user(username, password):
    flag = False
    msg = 'Bad coders!!!'
    cursor = connection.cursor()
    result_set = cursor.execute("SELECT * FROM genericuser WHERE login = %s", [username])
    dictfetchall(cursor)
    if result_set.rowcount != 1:
        flag = False; msg = 'No existe el usuario ' + username
    else:
        result_set = cursor.execute("SELECT * FROM genericuser WHERE login = %s", [username])
        user_password = [itm[1] for itm in result_set][0]
        if password != str(user_password):
            flag = False; msg = 'Clave invalida'
        else:
            flag = True
            msg = 'Best coders ever!!'
    connection.close()
    return flag, msg

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

def register_user(username, password, password_again):
    flag = False
    msg = ''
    cursor = connection.cursor()
    usernames = cursor.execute("SELECT * FROM genericuser WHERE login = %s", [username])
    if usernames.rowcount != 0:
        # Un usuario con este nombre ya existe
        flag = False
        msg = 'Ya existe un usuario con el mismo nombre de usuario'
    else:
        if password != password_again:
            flag = False
            msg = 'Las contrasenias no coinciden'
        else:
            timestamp = datetime.now
            values = [username, password, timestamp]
            cursor.execute("INSERT INTO genericuser (login, password, time_created) VALUES (%s, %s, %s)", values)
    cursor.execute("COMMIT;")
    connection.close()
    return flag, msg

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def get_user(username):
    ans = None
    cursor = connection.cursor()
    result_set = cursor.execute("SELECT * FROM genericuser WHERE login = %s", [username])
    if result_set.rowcount != 0:
        name = [itm[0] for itm in result_set][0]
        password = [itm[1] for itm in result_set][0]
        timestamp = [itm[2] for itm in result_set][0]
        ans = genericuser.Genericuser(name, password, timestamp)
    ans = genericuser.Genericuser('reactive', 'bages', 'sdsfdfs')
    connection.close()
    return ans
