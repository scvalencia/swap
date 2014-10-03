######################## DJANGO IMPORTS ########################
from django.db import connection
from django.shortcuts import render, redirect

######################## CUSTOM IMPORTS ########################
from genericusers.views import get_user
import solicitude
from vals import val
from vals.views import get_all_vals
import random


################################################################
######################## VIEW FUNCTIONS ########################
################################################################


def new_solicitude(request):
    '''Returns the respective response to the new_solicitude url call.'''
    username, user_type = check_username(request)
    if not username or user_type != '1':
        return redirect('/users/home/')
    vals = get_all_vals()
    params = {
        'pk_id': '',
        'vals': vals,
        'quantity': '',
        'message': '',
    }
    if request.method == 'POST':
        valid, error = is_valid_new_solicitude(username, request.POST)
        if valid:
            params['message'] = 'Tu solicitud fue creada satisfactoriamente!'
        else:
            params['pk_id'] = request.POST.get('pk_id')
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
    params = {
        'solicitudes': [],
        'message': ''
    }
    if request.method == 'POST':
        valid, error = is_valid_cancel(request.POST)
        if valid:
            params['message'] = 'Solicitudes canceladas correctamente'
        else:
            params['message'] = error
    solicitudes = get_active_solicitudes(username)
    params['solicitudes'] = solicitudes
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
        elif val == '-1':
            return False, 'Debe seleccional algun valor'
        elif quantity_type != '1' and quantity_type != '2':
            return False, 'El tipo de cantidad no es valido'
        else:
            return insert_solicitude(username, operation_type, val,
                                    quantity, quantity_type)
    else:
        return False, 'Todos los campos deben estar completos'

def is_valid_pending_solicitudes(form_data):
    to_aprove = form_data.getlist('to_aprove')
    if to_aprove and len(to_aprove) > 0:
        return activate_pending_solicitudes(to_aprove)
    else:
        return False, 'Debes seleccionar al menos una solicitud'

def is_valid_cancel(form_data):
    to_cancel = form_data.getlist('to_cancel')
    if to_cancel and len(to_cancel) > 0:
        return cancel_pending_solicitude(to_cancel)
    else:
        return False, 'Debes seleccionar al menos una solicitud'


################################################################
################### LOW LEVEL AUX FUNCTIONS ####################
################################################################


def insert_solicitude(username, operation_type, val, quantity, quantity_type):
    flag, error_message = False, ''
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
    cursor = connection.cursor()
    ans = []
    query = "SELECT * FROM solicitude WHERE active_login = %s AND solved = %s ORDER BY time_created DESC"
    collection = cursor.execute(query, [username, "0"])
    lst = [i for i in cursor.fetchall()]
    for itm in lst:
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
    ans = []
    cursor = connection.cursor()
    query = ("SELECT DISTINCT * FROM solicitude INNER JOIN active ON "
             "active.login = solicitude.active_login "
             "WHERE passive = %s AND is_active = %s")
    cursor.execute(query, [username, '0'])
    lst = [i for i in cursor.fetchall()]
    if len(lst) != 0:
        for i in lst:
            pk_id = i[0]
            operation_type = i[1]
            value = i[2]
            query = "SELECT * FROM val WHERE pk_id = %s"
            parameters = [value]
            cursor.execute(query, parameters)
            dependant_values = [j for j in cursor.fetchall()]
            val_ = populate_value(dependant_values[0])
            '''
            for dp_val in dependant_values:
                val_id = dp_val[0]
                name = dp_val[1]
                price = dp_val[2]
                quantity = dp_val[3]
                offerant = dp_val[4]
                val_ = val.Val(val_id, name, price, quantity, offerant)
            '''
            quantity = i[3]
            quantity_type = i[4]
            time_created = i[5]
            active_login = i[6]
            solved = i[7]
            is_active = i[8]
            itm = solicitude.Solicitude(pk_id, operation_type, val_, quantity, 
                quantity_type, time_created, active_login, solved, is_active)
            ans.append(itm)
    connection.close()             
    return ans

def get_passive_solicitudes(username):
    ans = []
    cursor = connection.cursor()
    query = ("SELECT DISTINCT * FROM solicitude INNER JOIN active ON "
             "active.login = solicitude.active_login "
             "WHERE passive = %s AND solved = %s AND is_active = %s")
    cursor.execute(query, [username, '0', '1'])
    lst = [i for i in cursor.fetchall()]
    if len(lst) != 0:
        for i in lst:
            pk_id = i[0]
            operation_type = i[1]
            query = "SELECT * FROM val WHERE pk_id = %s"
            parameters = [i[2]]
            cursor.execute(query, parameters)
            dependant_values = [j for j in cursor.fetchall()]
            val_ = populate_value(dependant_values[0])
            quantity = i[3]
            quantity_type = i[4]
            time_created = i[5]
            active_login = i[6]
            solved = i[7]
            is_active = i[8]
            itm = solicitude.Solicitude(pk_id, operation_type, val_, quantity, 
                quantity_type, time_created, active_login, solved, is_active)
            ans.append(itm)
    connection.close()             
    return ans

def activate_pending_solicitudes(to_aprove):
    cursor = connection.cursor()
    for pk in to_aprove:
        cursor.execute("UPDATE solicitude SET is_active = %s WHERE pk_id = %s", ['1', pk])
    connection.close()
    return True, ''

def filter_values(value_type, rent_type, id_offerant, id_passive, id_active, 
    ordering_flag, active_solicitude = True, desc = True):
    
    '''
    Consultar valores filtrados por tipo valor, tipo rentabilidad, 
    si hay solicitudes de esos valores, id oferente, id intermediario, 
    id inversionista, ordenar respuesta segun intereses del usuario que consulta
    '''

    ordering_parameters = ['name', 'price', 'quantity', 'offerant', 'rent_type', 'value_type']
    sorting_parameters = ['ASC', 'DESC']

    
    cursor = connection.cursor()
    general_query = ("SELECT DISTINCT pk_id, name, price, quantity, offerant, rent_type, val_type FROM "
                     "      (SELECT * FROM ownerval INNER JOIN val ON val.pk_id = ownerval.val) owners "
                     "  INNER JOIN "
                     "      (SELECT * FROM active WHERE passive = %s) employees "
                     "  ON owners.owner = employees.login "
                     "WHERE "
                     "  (val_type = %s OR rent_type = %s OR offerant = %s OR login = %s)"
                     "ORDER BY "
                    )
    params = [id_passive, value_type, rent_type, id_offerant, id_active]
    params = map(lambda a : "NULL" if a == None else a , params)
    if ordering_flag not in ordering_parameters:
        return [], 'Error en la solicitud'
    else:
        ans = []
        general_query += ordering_flag + ' '
        if desc:
            general_query += sorting_parameters[1] #DESC
        else:
            general_query += sorting_parameters[0] #ASC
        cursor.execute(general_query, params)
        resulting_set = [i for i in cursor.fetchall()]
        for value_ in resulting_set:
            pk_id = value[0] 
            name = value[1] 
            price = value[2] 
            quantity = value[3]
            offerant = value[4]
            value_object = val.Val(pk_id, name, price, quantity, offerant)
            new_query = "SELECT * FROM solicitude WHERE val = %s AND is_Active = %s"
            cursor.execute(new_query, [pk_id, '1'])
            length = len([i for i in cursor.fetchall()])
            if active_solicitude:
                if length != 0:
                    ans.append(value_object)
            else:
                if length == 0:
                    ans.append(value_object)

    connection.close()
    return ans, 'Proceso exitoso'

def cancel_pending_solicitude(to_remove):
    cursor = connection.cursor()
    for pk in to_aprove:
        query = "DELETE FROM solicitude WHERE (pk_id = %s AND solved = %s)"
        lst = [pk, '0']
        cursor.execute(query, lst)
    connection.close()
    return True, 'Solicitud cancelada'

def create_transaction(transaction_pk):
    cursor = connection.cursor()
    query = "SELECT * FROM solicitude WHERE pk_id = %s"
    cursor.execute(query, [transaction_pk])
    result_set = [i for i in cursor.fetchall()]
    if len(result_set) == 0:
        return False, 'No existe tal solicitud'
    else:
        query = "UPDATE solicitude SET solved = %s WHERE pk_id = %s"
        cursor.execute(query, ['1', transaction_pk])
    connection.close()
    return True, 'Transaccion exitosa'




