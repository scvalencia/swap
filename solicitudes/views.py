######################## DJANGO IMPORTS ########################
from django.db import connection
from django.shortcuts import render, redirect

######################## CUSTOM IMPORTS ########################
from genericusers.views import get_user
import solicitude
from vals import val


################################################################
######################## VIEW FUNCTIONS ########################
################################################################


def new_solicitude(request):
    '''Returns the respective response to the new_solicitude url call.'''
    username, user_type = check_username(request)
    if not username or user_type != 1:
        return redirect('/users/home/')
    params = {
        'pk_id': '',
        'val': '',
        'quantity': '',
        'message': '',
    }
    if request.method == 'POST':
        valid, error = is_valid_new_solicitude(request.POST)
        params['pk_id'] = request.POST.get('pk_id')
        params['val'] = request.POST.get('val')
        params['quantity'] = request.POST.get('quantity')
        params['message'] = error
        if valid:
            params['message'] = 'Tu solicitud fue creada satisfactoriamente!'
        return render(request, 'new_solicitude.html', params)
    else:
        return render(request, 'new_solicitude.html', params)

def active_solicitudes(request):
    '''Returns the respective response to the active_solicitudes url call.'''
    username, user_type = check_username(request)
    if not username or user_type != 1:
        return redirect('/users/home/')
    solicitudes = get_active_solicitudes(username)
    params = {
        'solicitudes': solicitudes,
        'message': ''
    }
    if len(solicitudes) == 0:
        params['message'] = 'Actualemente no tienes solicitudes, vuelve mas tarde!'
    return render(request, 'active_solicitudes.html', params)

def passive_pending_solicitudes(request):
    '''Returns the respective response to the passive_pending_solicitudes url call.'''
    username, user_type = check_username(request)
    if not username or user_type != 2:
        return redirect('/users/home/')
    params = {
        'solicitudes': [],
        'message': '',
    }
    if request.method == 'POST':
        valid, error = is_valid_pending_solicitudes(request.POST)
        if valid:
            params['message'] = 'Solicitudes activadas correctamente!'
        else:
            params['message'] = error
    pending_solicitudes = get_passive_pending_solicitudes(username)
    params['solicitudes'] = pending_solicitudes
    if len(pending_solicitudes) == 0:
        params['message'] = 'No tienes solicitudes pendientes!'
    return render(request, 'passive_pending_solicitudes.html', params)

def passive_solicitudes(request):
    '''Returns the respective response to the passive_pending_solicitudes url call.'''
    username, user_type = check_username(request)
    if not username or user_type != 2:
        return redirect('/users/home/')
    solicitudes = get_passive_solicitudes(username)
    params = {
    'solicitudes': solicitudes,
    'message': '',
    }
    if len(solicitudes) == 0:
        params['message'] = 'No tienes solicitudes de tus activos!'
    return render(request, 'passive_solicitudes.html', params)


################################################################
################## HIGH LEVEL AUX FUNCTIONS ####################
################################################################


def check_username(request):
    username = request.session.get('username')
    if username:
        user, user_type = get_user(username)
        if user:
            return username
        else:
            del request.session['username']
            return None
    else:
        return None

def is_valid_new_solicitude(form_data):
    # TODO jcbages
    return True

def is_valid_pending_solicitudes(form_data):
    # TODO jcbages
    return True, ''


################################################################
################### LOW LEVEL AUX FUNCTIONS ####################
################################################################


def insert_solicitude(username, operation_type, val, quantity, quantity_type):
    # TODO scvalencia
    # Necesito que inserte la nueva solicitud a la tabla, en caso
    # de problemas como por ejemplo una PK duplicada, retornaria 
    # False y un mensaje de error, si todo sale bien, retorne 
    # True y mensaje de error vacio.
    boolean, error = True, ''
    return boolean, error

def get_active_solicitudes(username):
    # TODO scvalencia
    # Necesito todas las solicitudes que ha hecho este activo
    # que figuran como NOT SOLVED porque si estan en SOLVED la
    # idea es mostrarlas en la parte de transactions, pero debe
    # retornar un arreglo de objectos tipo solicitud osea usando
    # la clase de solicitud.py.
    ans = []
    query = "SELECT * FROM solicitude WHERE active_login = %s AND solved = %s"
    collection = cursor.execute(query, [username, "0"])
    for itm in collection:
        assert len(itm) == 9
        pk = itm[0]
        operation_type = itm[1]
        val = itm[2]
        query = "SELECT * FROM val WHERE pk_id = %s"        
        cursor.execute(query, [val])
        value = cursor.fetchone()
        value_object = populate_value(value)
        quantity = itm[3]
        quantity_type = itm[4]
        time_created = itm[5]
        active_login = itm[6]
        solved = itm[7]
        is_active = itm[8]        
        element = solicitude.Solicitude(pk, operation_type, value_object, quantity,
            quantity_type, time_created, active_login, solved, is_active)
        ans.append(to_add)

    return ans

def populate_value(value_tuple):
    ans = None
    pk_id = value_tuple[0]
    name = value_tuple[1]
    price = value_tuple[2]
    quantity = value_tuple[3]
    offerant = value_tuple[4]
    ans = val.Val(pk_id, name, price, quantity, offerant)


def get_passive_pending_solicitudes(username):
    # TODO scvalencia
    # Necesito todas las solicitudes que han hecho los activos
    # que tienen asignado a este pasivo y que ademas figuran
    # como NOT IS ACTIVE pues son las que los oferentes 
    # hicieron al intermediario y este las tiene pendientes por
    # activar, por ende ademas deben aparecer como NOT SOLVED,
    # pero debe retornar un arreglo de objectos tipo solicitud
    # osea usando la clase de solicitud.py.
    return []

def get_passive_solicitudes(username):
    # TODO scvalencia
    # Necesito todas las solicitudes han hecho los activos
    # que tienen asignado a este pasivo y que ademas figuran
    # como IS ACTIVE pues son las que ya estan activadas, por
    # ende ademas deben aparecer como NOT SOLVED pues son las
    # que queremos negociar por asi decirlo, pero debe retornar
    # un arreglo de objectos tipo solicitud osea usando la
    # clase de solicitud.py.
    return []