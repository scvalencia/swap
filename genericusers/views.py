######################## DJANGO IMPORTS ########################
from django.db import connection
from django.shortcuts import render, redirect

######################## CUSTOM IMPORTS ########################
import genericuser
import random, string


################################################################
######################## VIEW FUNCTIONS ########################
################################################################


def login(request):
    '''Returns the respective response to the login url call.'''
    if request.method == 'POST':
        valid, error = is_valid_login(request.POST)        
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
        username = request.session.get('username')
        if username:
            user = get_user(username)[0]
            if user:
                return redirect('/users/home/')
            del request.session['username']
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
            request.session['username'] = request.POST.get('username')
            return redirect('/users/home/')
        else:
            params = {
                'username': request.POST.get('username'),
                'error': error,
            }
            return render(request, 'signup.html', params)
    else:
        username = request.session.get('username')
        if username:
            user = get_user(username)[0]
            if user:
                return redirect('/users/home/')
            del request.session['username']
        params = {
            'username': '',
            'error': '',
        }
        return render(request, 'signup.html', params)

def logout(request):
    '''Returns the respective response to the logout url call.'''
    name = ''
    username = request.session.get('username')
    if username:
        name = ' %s' % username
        del request.session['username']
    params = {
        'name': name,
    }
    return render(request, 'logout.html', params)

def home(request):
    '''Returns the respective response to the home url call.'''
    username = request.session.get('username')
    if username:
        user = get_user(username)[0]
        if user:
            params = {'username': user.login}
            user_type = get_user_type(username)
            if user_type == '1': # is an active user!
                return render(request, 'active_home.html', params)
            elif user_type == '2': # is a passive user!
                return render(request, 'passive_home.html', params)
        del request.session['username']
    return render(request, 'home.html')

def search(request):
    pass
    #TODO


################################################################
################## HIGH LEVEL AUX FUNCTIONS ####################
################################################################


def is_valid_login(form_data):
    '''Validates the login form returning true or false, and if
    it's the case, the corresponding error message.'''
    username = form_data.get('username')
    password = form_data.get('password')
    if username and password:
        return validate_user(username, password)
    else:
        return False, 'Todos los campos deben estar completos.'

def is_valid_signup(form_data):
    '''Validates the signup form returning true or false, and if
    it's the case, the corresponding error message.'''
    username = form_data.get('username')
    password = form_data.get('password')
    repeat_password = form_data.get('repeat_password')
    user_type = form_data.get('user_type')
    print username, password, repeat_password, user_type
    print username and password and repeat_password and user_type
    if username and password and repeat_password and user_type:
        if password != repeat_password:
            return False, 'Las claves deben coincidir.'
        elif user_type != '1' and user_type != '2':
            return False, 'El tipo de usuario no es valido.'
        else:
            return register_user(username, password, user_type)
    else:
        return False, 'Todos los campos deben estar completos.'


################################################################
################### LOW LEVEL AUX FUNCTIONS ####################
################################################################


def validate_user(username, password):
    '''Validates the login user checking it's existante in the
    database and checking that the values are legit, it returns
    a boolean, and if it's the case, it's corresponding message.'''
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
    '''Validates the signingup user checking it's not already in
    the database, and checking that the values are legit, it returns
    a boolean, and if it's the case, it's corresponding message.'''
    flag = False
    msg = ''
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM genericuser WHERE login = %s;", [username])
    if len(cursor.fetchall()) != 0:
        # Un usuario con este nombre ya existe
        flag = False
        msg = 'Ya existe un usuario con el mismo nombre de usuario.'
    else:
        values = [username, password]
        # Active -> 1, Passive -> 2
        # cursor.execute("START TRANSACTION")
        cursor.execute("INSERT INTO genericuser (login, password, time_created) VALUES (%s, %s, Current_Timestamp);", values)
        if user_type == '1':
            print 'Active'
            cursor.execute("SELECT login, COUNT(login) AS freq FROM passive GROUP BY login")
            tuples = cursor.fetchall()
            minimum = min([freq for (login, freq) in tuples])
            candidates = filter(lambda a : a[1] == minimum, [i for i in tuples])
            lazy = random.choice(candidates)
            lazy_name = lazy[0]
            my_passive = [i for i in cursor.execute("SELECT reg_num FROM passive WHERE login = %s", [lazy_name])][0][0]
            print my_passive
            a = cursor.execute("SELECT * FROM genericuser WHERE login = %s", [username])
            print [i for i in a]
            b = cursor.execute("SELECT * FROM passive WHERE reg_num = %s", [my_passive])
            print [i for i in b]
            query = ("INSERT INTO active (login, passive)" 
                     "SELECT A.login, B.reg_num "
                     "FROM (SELECT login FROM genericuser WHERE login = %s) A, " 
                     "(SELECT reg_num FROM passive WHERE reg_num = %s) B")
            try:
                cursor.execute(query, [username, my_passive])
            except Exception, e:
                print 'Fuck'
            finally:
                pass
            
        elif user_type == '2':
            # Es pasivo
            seed_digits = string.digits
            seed_upper = string.ascii_uppercase
            seed = seed_digits + seed_upper
            generator = lambda s, n : ''.join(random.choice(s) for i in range(n))
            register = generator(seed, 25)
            cursor.execute("INSERT INTO passive (login, reg_num) VALUES (%s, %s);", [username, register])
            cursor.execute("SELECT * FROM passive WHERE login = %s;",  [username])
        flag = True
        msg = 'Transaccion exitosa'
    # cursor.execute("COMMIT;")
    connection.commit()
    connection.close()
    return flag, msg

def get_user(username):
    '''Get the corresponding user for the database that match
    the given username PK, it returns a user object with it's
    respective user's type.'''
    ans = None
    user_type = ''
    cursor = connection.cursor()
    lst = [username]
    uname, password, timestamp = None, None, None
    cursor.execute("SELECT * FROM genericuser WHERE login = %s;", lst)
    if len(cursor.fetchall()) == 0:
        # not exist!
        return None, '0'
    else:
        cursor.execute("SELECT * FROM genericuser WHERE login = %s;", lst)
        user_object = cursor.fetchone()
        uname = user_object[0]
        password = user_object[1]
        timestamp = user_object[2]
        real_user = genericuser.Genericuser(uname, password, timestamp)
        cursor.execute("SELECT * FROM passive WHERE login = %s", lst)
        if len(cursor.fetchall()) != 0:
            # is passive!
            return  real_user, '2'
        cursor.execute("SELECT * FROM active WHERE login = %s", lst)
        if len(cursor.fetchall()) != 0:
            # is active!
            return real_user, '1'
        else:
            return None, '0'
    connection.close()
    return ans, user_type # non-reacheable code!!!

def get_user_type(username):
    return get_user(username)[1]
