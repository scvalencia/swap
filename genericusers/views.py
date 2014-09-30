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
            # TODO add user to session. *
            request.session['username'] = request.POST.get('username') # *
            return redirect('/users/home/')
        else:
            params = {
                'username': request.POST.get('username'),
                'password': request.POST.get('password'),
                'error': error,
            }
            return render(request, 'login.html', params)
    else:
        # TODO get the username from session *
        username = request.session.get('username') # *
        # TODO check user existance in session. *
        # if it exist, do the indented below. *
        if username: # *
            user = get_user('genericuser', username)
            if user:
                return redirect('/users/home/')
            # TODO remove the user session in case of a corrupted one *
            del request.session['username'] # *
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
            # TODO add user to session. *
            request.session['username'] = request.POST.get('username') # *
            return redirect('/users/home/')
        else:
            params = {
                'username': request.POST.get('username'),
                'error': error,
            }
            return render(request, 'signup.html', params)
    else:
        # TODO get the username from session *
        username = request.session.get('username') # *
        # TODO check user existance in session *
        # if it exist, do the indented below *
        if username: # *
            user = get_user('genericuser', username)
            if user:
                return redirect('/users/home/')
            # TODO remove the user session in case of a corrupted one *
            del request.session['username'] # *
        params = {
            'username': '',
            'error': '',
        }
        return render(request, 'signup.html', params)

def logout(request):
    '''Returns the respective response to the logout url call.'''
    name = ''
    # TODO get the username from session *
    username = request.session.get('username') # *
    # TODO check user existance in session *
    # if it exist, do the indented below *
    if username: # *
        name = ' %s' % username
        # TODO remove the user session *
        del request.session['username'] # *
    params = {
        'name': name,
    }
    return render(request, 'logout.html', params)

def home(request):
    '''Returns the respective response to the home url call.'''
    # TODO get the username from session *
    username = request.session.get('username') # *
    # TODO check user existance in session *
    # if it exist, do the indented below *
    if username: # *
        user = get_user('genericuser', username)
        if user:
            # TODO get the user type *
            user_type = get_user_type(username) # *
            if user_type == '1': # is an active user!
                return render(request, 'active_home.html')
            elif user_type == '2': # is a passive user!
                return render(request, 'passive_home.html')
        # TODO remove the user session *
        del request.session['username'] # *
    return render(request, 'home.html')


################################################################
######################## AUX FUNCTIONS #########################
################################################################


def is_valid_login(form_data):
    username = form_data.get('username')
    password = form_data.get('password')
    if username and password:
        return validate_user(username, password)
    else:
        return False, 'Todos los campos deben estar completos.'

def is_valid_signup(form_data):
    username = form_data.get('username')
    password = form_data.get('password')
    repeat_password = form_data.get('repeat_password')
    user_type = form_data.get('user_type')
    if username and password and repeat_password and user_type:
        if password != repeat_password:
            return False, 'Las claves deben coincidir.'
        elif user_type != '1' and user_type != '2':
            return False, 'El tipo de usuario no es valido.'
        else:
            return register_user(username, password, user_type)
    else:
        return False, 'Todos los campos deben estar completos.'

def validate_user(username, password):
    username = 'luisa'
    flag = False
    msg = 'Bad coders!!!'
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM genericuser WHERE login = %s", [username])
    if len(cursor.fetchall()) == 0:
        flag = False
        msg = 'No existe el usuario %s.' % username
    else:
        result_set = cursor.execute("SELECT * FROM genericuser WHERE login = %s;", [username])
        user_password = [itm[1] for itm in result_set][0]
        if password != str(user_password):
            flag = False
            msg = 'Clave invalida.'
        else:
            flag = True
            msg = 'Best coders ever!!!'
    connection.close()
    return flag, msg

def register_user(username, password, user_type):
    flag = False
    msg = ''
    cursor = connection.cursor()
    usernames = cursor.execute("SELECT * FROM genericuser WHERE login = %s;", [username])
    if usernames.rowcount != 0:
        # Un usuario con este nombre ya existe
        flag = False
        msg = 'Ya existe un usuario con el mismo nombre de usuario.'
    else:
        values = [username, password]
        # Active -> 1, Passive -> 2
        # cursor.execute("START TRANSACTION")
        cursor.execute("INSERT INTO genericuser (login, password, time_created) VALUES (%s, %s, Current_Timestamp);", values)
        if user_type == '1':
            # TODO es activo, entonce, crea el activo, y revisa la tabla de pasivos
            # si esta vacio, por asignar (dafult). sino, agragar el pasivo con
            # menos activos
            cursor.execute("INSERT INTO active (login, passive) VALUES (%s, %s);", [username, 'pending'])
        elif user_type == '2':
            seed_digits = string.digits
            seed_upper = string.ascii_uppercase
            seed = seed_digits + seed_upper
            generator = lambda s, n : ''.join(random.choice(s) for i in range(n))
            register = generator(seed, 25)
            cursor.execute("INSERT INTO passive (login, register) VALUES (%s, %s);", [username, register])
            # TODO: Revisar si hay activos pendientes y asignarlo
        flag = True
        msg = 'Transaccion exitosa'
    # cursor.execute("COMMIT;")
    connection.close()
    return flag, msg

def get_user(table, username):
    ans = None
    cursor = connection.cursor()
    result_set = cursor.execute("SELECT * FROM %s WHERE login = %s;", [table, username])
    for item in result_set:
        ans = genericuser.Genericuser(item[0], item[1], item[2])
        break
    connection.close()
    return ans

def get_user_type(username):
    if get_user('active', username):
        return '1'
    elif get_user('passive', username):
        return '2'
    else:
        return '-1'