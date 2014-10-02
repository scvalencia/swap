######################## DJANGO IMPORTS ########################
from django.db import connection
from django.shortcuts import render, redirect

######################## CUSTOM IMPORTS ########################
from genericusers.views import get_user
import solicitude
from vals import val
import random


################################################################
######################## VIEW FUNCTIONS ########################
################################################################


def new_solicitude(request):
    '''Returns the respective response to the new_solicitude url call.'''
    username, user_type = check_username(request)
    if not username or user_type != '1':
        return redirect('/users/home/')
    params = {
        'pk_id': '',
        'val': '',
        'quantity': '',
        'message': '',
    }
    if request.method == 'POST':
        valid, error = is_valid_new_solicitude(username, request.POST)
        if valid:
            params['message'] = 'Tu solicitud fue creada satisfactoriamente!'
        else:
            params['pk_id'] = request.POST.get('pk_id')
            params['val'] = request.POST.get('val')
            params['quantity'] = request.POST.get('quantity')
            params['message'] = error
        return render(request, 'new_solicitude.html', params)
    else:
        return render(request, 'new_solicitude.html', params)

def active_solicitudes(request):
    '''Returns the respective response to the active_solicitudes url call.'''
    username, user_type = check_username(request)
    if not username or user_type != '1':
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
    if not username or user_type != '2':
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
    if not username or user_type != '2':
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
            return username, user_type
        else:
            del request.session['username']
            return None, '0'
    else:
        return None, '0'

def is_valid_new_solicitude(username, form_data):
    operation_type = form_data.get('operation_type')
    val = form_data.get('val')
    quantity = form_data.get('quantity')
    quantity_type = form_data.get('quantity_type')
    if operation_type and val and quantity and quantity_type:
        if operation_type != '1' and operation_type != '2':
            return False, 'El tipo de operacion no es valido'
        elif quantity_type != '1' and quantity_type != '2':
            return False, 'El tipo de cantidad no es valido'
        else:
            return insert_solicitude(username, operation_type, val,
                                    quantity, quantity_type)
    else:
        return False, 'Todos los campos deben estar completos'

def is_valid_pending_solicitudes(form_data):
    to_aprove = form_data.get('to_aprove')
    if to_aprove and len(to_aprove) > 0:
        return activate_pending_solicitudes(to_aprove)
    else:
        return False, 'Debes seleccionar al menos una solicitud'


################################################################
################### LOW LEVEL AUX FUNCTIONS ####################
################################################################


def insert_solicitude(username, operation_type, val, quantity, quantity_type):
    flag, error_message = False, ''
    # Necesito que inserte la nueva solicitud a la tabla, en caso
    # de problemas como por ejemplo una PK duplicada, retornaria 
    # False y un mensaje de error, si todo sale bien, retorne 
    # True y mensaje de error vacio.
    cursor = connection.cursor()
    pk = random.choice(range(5, 30000))
    is_invalid = True;
    while is_invalid:
        cursor.execute("SELECT * FROM solicitude WHERE  pk_id = %s", [pk])
        lst = [i for i in cursor.fetchall()]
        if len(lst) == 0:
            is_invalid = False 
        else:
             pk = random.choice(range(5, 30000))
    cursor.execute("SELECT * FROM val WHERE pk_id = %s", [val])
    lst = [i for i in cursor.fetchall()]
    if len(lst) == 0:
        flag = False
        error_message = 'El valor no existe'
    else:
        default_value = '0'
        params = [pk, operation_type, val, quantity, quantity_type, username, default_value, default_value]
        query = "INSERT INTO solicitude VALUES (%s, %s, %s, %s, %s, Current_Timestamp, %s, %s, %s)"
        cursor.execute(query, [pk, operation_type, val, quantity, quantity_type, username, default_value, default_value])
        connection.close()
        flag = True
        error_message = ''
    return flag, error_message

def get_active_solicitudes(username):
    # Necesito todas las solicitudes que ha hecho este activo
    # que figuran como NOT SOLVED porque si estan en SOLVED la
    # idea es mostrarlas en la parte de transactions, pero debe
    # retornar un arreglo de objectos tipo solicitud osea usando
    # la clase de solicitud.py.
    cursor = connection.cursor()
    ans = []
    query = "SELECT * FROM solicitude WHERE active_login = %s AND solved = %s ORDER BY time_created DESC"
    collection = cursor.execute(query, [username, "0"])
    lst = [i for i in cursor.fetchall()]
    for itm in lst:
        print 'a'
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
        ans.append(element)

    connection.close()
    print ans
    return ans

def populate_value(value_tuple):
    ans = None
    pk_id = value_tuple[0]
    name = value_tuple[1]
    price = value_tuple[2]
    quantity = value_tuple[3]
    offerant = value_tuple[4]
    ans = val.Val(pk_id, name, price, quantity, offerant)
    return ans


def get_passive_pending_solicitudes(username):
    # Necesito todas las solicitudes que han hecho los activos
    # que tienen asignado a este pasivo y que ademas figuran
    # como NOT IS ACTIVE,
    # pero debe retornar un arreglo de objectos tipo solicitud
    # osea usando la clase de solicitud.py.
    ans = []
    cursor = connection.cursor()
    query = ("SELECT * FROM solicitude INNER JOIN active ON "
             "active.passive = solicitude.active_login "
             "WHERE passive = %s")
    cursor.execute(query, [username])
    lst = [i for i in cursor.fetchall()]
    if len(lst) != 0:
        for i in lst:
            pk_id = lst[0]
            operation_type = lst[1]
            val = lst[2]
            quantity = last[3]
            quantity_type = lst[4]
            time_created = lst[5]
            active_login = lst[6]
            solved = lst[7]
            is_active = lst[8]
            itm = solicitude.Solicitude(pk_id, operation_type, val, quantity, 
                quantity_type, time_created, active_login, solved, is_active)
            ans.append(itm)
    connection.close()             
    return ans

def get_passive_solicitudes(username):
    # TODO scvalencia
    # Necesito todas las solicitudes han hecho los activos
    # que tienen asignado a este pasivo y que ademas figuran
    # como IS ACTIVE pues son las que ya estan activadas, por
    # ende ademas deben aparecer como NOT SOLVED pues son las
    # que queremos negociar por asi decirlo, pero debe retornar
    # un arreglo de objectos tipo solicitud osea usando la
    # clase de solicitud.py.
    ans = []
    return ans

def activate_pending_solicitudes(to_aprove):
    # TODO scvalencia
    # Necesito que dado ese to_aprove que es un arreglo de
    # pk_id de las solicitudes, les ponga IS ACTIVE en 1,
    # es decir en verdadero, si todo sale bien retorne True
    # y el mensaje de error vacio, en caso de algun error,
    # retorne False y el mensaje de error correpondiente
    return True, ''
