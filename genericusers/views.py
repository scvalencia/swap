######################## DJANGO IMPORTS ########################
from django.db import connection
from django.shortcuts import render, redirect

######################## CUSTOM IMPORTS ########################
import genericuser
from swap import settings
from swap.settings import SECRET_KEY


################################################################
######################## VIEW FUNCTIONS ########################
################################################################


def login(request):
    '''Returns the respective response to the login url call.'''
    if request.method == 'POST':
        valid, error = is_valid_login(request.POST)
        if valid:
            # TODO add user to session.
            return redirect('/users/home/')
        else:
            params = {
                'username': request.POST.get('username'),
                'password': request.POST.get('password'),
                'error': error,
            }
            return render(request, 'login.html', params)
    else:
        # TODO check user existance in session.
        # if it exist, do the indented below.
            username = # TODO get the username from session
            user = get_user(username)
            if user:
                return redirect('/users/home/')
        # TODO remove the user session in case of a corrupted one
        params = {
            'username': '',
            'password': '',
            'error': '',
        }
        return render(request, 'login.html', params)

def signup(request):
    '''Returns the respective response to the signup url call.'''
    if request.method == 'POST':
        valid, error = is_valid_signup(request.POST)
        if valid:
            # TODO add user to session.
            return redirect('/users/home/')
        else:
            params = {
                'username': request.POST.get('username'),
                'error': error,
            }
            return render(request, 'signup.html', params)
    else:
        # TODO check user existance in session
        # if it exist, do the indented below
            username = # TODO get the username from session
            user = get_user(username)
            if user:
                return redirect('/users/home/')
        # TODO remove the user session in case of a corrupted one
        params = {
            'username': '',
            'error': '',
        }
        return render(request, 'signup.html', params)

def logout(request):
    '''Returns the respective response to the logout url call.'''
    username = ''
    # TODO check user existance in session
    # if it exist, do the indented below
        username = ' %s' % # TODO get the username from session
        # TODO remove the user session
    params = {
        'username': username,
    }
    return render(request, 'logout.html', params)

def home(request):
    '''Returns the respective response to the home url call.'''
    # TODO check user existance in session
    # if it exist, do the indented below
        username = # TODO get the username from session
        user = get_user(username)
        if user:
            user_type = # TODO get the user type
            if user_type == 1: # is an active user
                return render(request, 'active_home.html')
            else: # is a passive user
                return render(request, 'passive_home.html')
        else:
            # TODO remove the user session
    return render(request, 'home.html')


################################################################
######################## AUX FUNCTIONS #########################
################################################################


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

def is_valid_login(form_data):
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
    print cursor.fetchall()
    if usernames.rowcount != 0:
        # Un usuario con este nombre ya existe
        flag = False
        msg = 'Ya existe un usuario con el mismo nombre de usuario'
        #return flag, msg
    else:
        if password == '':
            flag = False
            msg = 'La clave no puede ser vacia'
        else:
            values = [username, password]
            cursor.execute("INSERT INTO genericuser (login, password, time_created) VALUES (%s, %s, Current_Timestamp)", values)
            if password != password_again:
                flag = False
                msg = 'Las claves no coinciden'
            else:
                values = [username, password]
                cursor.execute("INSERT INTO genericuser (login, password, time_created) VALUES (%s, %s, Current_Timestamp)", values)
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
    # username = 'scvalencia'
    ans = None
    cursor = connection.cursor()
    result_set = cursor.execute("SELECT * FROM genericuser WHERE login = %s", [username])
    for item in result_set:
        name = item[0]; password = item[1]; timestamp = item[2]
        ans = genericuser.Genericuser(name, password, timestamp)
        break
    #ans = genericuser.Genericuser('reactive', 'bages', 'sdsfdfs')
    connection.close()
    return ans