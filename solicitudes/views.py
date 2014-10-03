######################## DJANGO IMPORTS ########################
from django.db import connection
from django.shortcuts import render, redirect

######################## CUSTOM IMPORTS ########################
from genericusers.views import get_user
from solicitude import Solicitude
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

def solicitude(request, sol_id):
    '''Returns the respective response to the solicitude url call.'''
    username, user_type = check_username(request)
    solicitude = get_solicitude(sol_id)
    if not username or user_type != '2' or not solicitude:
        return redirect('/users/home/')
    params = {
        'possible_transactions': [],
        'message': '',
    }
    if request.method == 'POST':
        valid, error = is_valid_transaction(sol_id, request.POST)
        if valid:
            params['message'] = 'Transaccion realizada correctamente'
        else:
            params['message'] = error
    possible_transactions = get_all_possible_transactions(sol_id)
    params['possible_transactions'] = possible_transactions
    if len(possible_transactions) == 0:
        params['message'] = 'No hay solicitudes negociables!'
    return render(request, 'solicitude.html', params)


################################################################
################## HIGH LEVEL AUX FUNCTIONS ####################
################################################################


def check_username(request):
    ''' Revisa la validez de un usuario '''
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
    ''' Revisa la validez de una solicitud nueva '''
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
    ''' Revisa si es valida la seleccion '''
    to_aprove = form_data.getlist('to_aprove')
    if to_aprove and len(to_aprove) > 0:
        return activate_pending_solicitudes(to_aprove)
    else:
        return False, 'Debes seleccionar al menos una solicitud'

def is_valid_cancel(form_data):
    ''' Revisa la validez dela cancelacion '''
    to_cancel = form_data.getlist('to_cancel')
    if to_cancel and len(to_cancel) > 0:
        return cancel_pending_solicitude(to_cancel)
    else:
        return False, 'Debes seleccionar al menos una solicitud'

def is_valid_transaction(sol_id, form_data):
    ''' Revisa la validez de la transaccion '''
    other_id = form_data.get('other_id')
    if sol_id and other_id:
        return create_transaction(sol_id, other_id)
    elif not other_id:
        return False, 'Debes seleccionar una solicitud'
    else:
        return False, 'Solicitud no valida'


################################################################
################### LOW LEVEL AUX FUNCTIONS ####################
################################################################


def insert_solicitude(username, operation_type, val, quantity, quantity_type):
    ''' Inserta una nueva solicitud dados los parametros de insercion '''
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
    ''' Obtiene una lista de objetos solicitudo cuyo estado este activo '''
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
        element = Solicitude(pk, operation_type, value_object, quantity,
            quantity_type, time_created, active_login, solved, is_active)
        ans.append(element)

    connection.close()
    return ans

def populate_value(value_tuple):
    ''' Crea un valor a partir de una tupla de una relacion '''
    ans = None
    pk_id = value_tuple[0]
    name = value_tuple[1]
    price = value_tuple[2]
    quantity = value_tuple[3]
    offerant = value_tuple[4]
    ans = val.Val(pk_id, name, price, quantity, offerant)
    return ans

def get_passive_pending_solicitudes(username):
    ''' Obtiene las solicitudes pendientes de un usuario intermediario '''
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
            itm = Solicitude(pk_id, operation_type, val_, quantity, 
                quantity_type, time_created, active_login, solved, is_active)
            ans.append(itm)
    connection.close()             
    return ans

def get_passive_solicitudes(username):
    ''' Obtiene todas las solicitudes de un intermediario '''
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
            itm = Solicitude(pk_id, operation_type, val_, quantity, 
                quantity_type, time_created, active_login, solved, is_active)
            ans.append(itm)
    connection.close()             
    return ans

def activate_pending_solicitudes(to_aprove):
    ''' Activa las solicitudes pendientes, dada una lista de identificadores '''
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
    ''' Cacela las solicitudes dada una lisa de identificadores de solicitudes '''
    cursor = connection.cursor()
    for pk in to_remove:
        query = "DELETE FROM solicitude WHERE (pk_id = %s AND solved = %s)"
        lst = [pk, '0']
        cursor.execute(query, lst)
    connection.close()
    return True, 'Solicitud cancelada'

def create_transaction(sol_id, other_id):
    ''' Crea una transaccion entre dos solicitudes '''
    # TODO scvalencia
    # Necesito que dados estos dos ids de solicitudes verifique
    # primero que ninguna este resuelta, luego de esto, si ambas
    # son validas, restele las unidades de la solicitud con menos
    # unidades a la que tiene mayor numero de unidades y a la de menor
    # dejela en 0, la o las solicitudes que queden en 0, marquelas como
    # resueltas, mientras que si la otra no queda en 0 pues sigue sin
    # estar resuelta, tenga cuidado restar el ismo tipo de unidades, sino
    # pues tiene que convertir de una unidad a otra con el costo del valor
    # regreseme true y mensaje vacio o false con mensaje de error.
    PESOS = '1'
    UNIDADES = '2'
    cursor = connection.cursor()
    query = "SELECT * FROM solicitude WHERE pk_id = %s OR pk_id = %s"
    cursor.execute(query, [sol_id, other_id])
    result_set = [i for i in cursor.fetchall()]
    if len(result_set) != 2:
        return False, 'No por lo menos alguna de las transacciones'
    else:
        first_solicitude_tuple = result_set[0]
        secnd_solicitude_tuple = result_set[1]
        first_state = first_solicitude_tuple[7]
        secnd_state = secnd_solicitude_tuple[7]
        if first_state != '0' or secnd_state != '0':
            return False, 'Alguna de las transacciones ya fue resuelta'
        else:
            minimum = lambda a, b : a if a[3] < b[3] else b # With minimum quantity
            maximum = lambda a, b : b if a[3] < b[3] else a # With maximum quantity
            minimum_object = minimum(first_solicitude_tuple, secnd_solicitude_tuple)
            maximum_object = maximum(first_solicitude_tuple, secnd_solicitude_tuple)
            first_quant_type = first_solicitude_tuple[4]
            secnd_quant_Type = secnd_solicitude_tuple[4]
            if first_quant_type == secnd_solicitude_tuple == PESOS:
                final_quantity = maximum_object[3] - minimum_object[3]
                query_1 = ("UPDATE solicitude "
                           "SET solved = %s, quantity = %s "
                           "WHERE pk_id = %s")
                params_1 = ['1', final_quantity, maximum_object[0]]
                query_2 = ("UPDATE solicitude "
                           "SET solved = %s, quantity = %s "
                           "WHERE pk_id = %s")
                params_2 = ['0', 0, minimum_object[0]]
                cursor.execute(query_1, params_1)
                cursor.execute(query_2, params_2)

            else:
                standard_type_1 = standard_type(first_solicitude_tuple[4])
                standard_type_2 = standard_type(secnd_solicitude_tuple[4])
                # TODO (si el tipo es distinto, pasar todo a una estandar)
    connection.close()
    return True, 'Transaccion exitosa'

def standard_type(sol_type):
    PESOS = '1'
    UNIDADES = '2'
    pass

def get_all_possible_transactions(solicitude_pk):
    ''' Obtiene todas las solicitudes que pueden llegar a ser transacciones '''
    # TODO scvalencia
    # Necesito que dado el pk de una solicitud,
    # me regrese todas las solicitudes sin resolver
    # que tengan el tipo de operacion contrario al de la 
    # solicitud que le di, tengan el mismo valor, y una
    # cantidad mayor o igual de valores a la del a solicitud
    # dada.
    ans = []
    cursor = connection.cursor()
    query = "SELECT * FROM solicitude WHERE pk_id = %s"
    cursor.execute(query, [solicitude_pk])
    result_set = [i for i in cursor.fetchall()]
    current_solicitude = None
    for i in result_set:
        pk_id = i[0]
        operation_type = i[1]
        val = i[2]
        quantity = i[3]
        quantity_type = i[4]
        time_created = i[5]
        active_login = i[6]
        solved = i[7]
        is_active = i[8]
        current_solicitude = Solicitude(pk_id, operation_type, val, quantity,
         quantity_type, time_created, active_login, solved, is_active)

    # Sin resolver
    current_operation_type = current_solicitude.operation_type
    current_value = current_solicitude.val
    current_quantity = current_solicitude.quantity

    params = ['0', current_operation_type, current_value, current_quantity]
    query = ("SELECT * FROM solicitude "
             "WHERE (solved = %s AND operation_type <> %s AND val = %s AND quantity >= %s)")
    cursor.execute(query, params)
    result_solicitudes = [i for i in cursor.fetchall()]
    if len(result_set) != 0:
        for itm in result_set:
            pk_id = itm[0] 
            operation_type = itm[1]
            val = itm[2] 
            quantity = itm[3]
            quantity_type = itm[4]
            time_created = itm[5]
            active_login = itm[6] 
            solved = itm[7] 
            is_active = itm[8]
            
            if current_solicitude.active_login != active_login:
                solicitude_object = Solicitude(pk_id, operation_type, val, 
                    quantity, quantity_type, time_created, active_login, solved, is_active)
                ans.append(solicitude_object)


    connection.close()
    msg = ''
    flag = len(ans) != 0
    if flag:
        msg = 'Transaccion exitosa'
    else:
        msg ='Error en transaccion'

    return ans, msg

def get_solicitude(sol_id):
    ''' Devuelve un objeto solicitud dado un identificador '''
    # TODO scvalencia
    # Igual que el get_user, necesito que compruebe si ese 
    # pk esta asignado a una solicitud, es decir, si esa 
    # solicitud existe
    cursor = connection.cursor()
    lst = [sol_id]
    cursor.execute("SELECT * FROM solicitude WHERE pk_id = %s;", lst)
    ans = [i for i in cursor.fetchall()]
    if len(ans) == 0:
        return False, None, 'No existen solicitudes con tal ID'
    sol_object = None
    for i in ans:
        pk_id = i[0]
        operation_type = i[1]
        val = i[2]
        quantity = i[3]
        quantity_type = i[4] 
        time_created = i[5] 
        active_login = i[6] 
        solved = i[7]
        is_active = i[8]

        sol_object = Solicitude(pk_id, operation_type, val, 
                quantity, quantity_type, time_created, active_login, solved, is_active)
        break   

    return True, sol_object, ""

def get_best_values_date_range(date1, date2, sorting_criteria = 'DESC'):
    ''' Obtiene una lista de valores transados en un rango de fecha '''
    # date format : YYYY-MON-DD '2008-JUN-01'
    objects = []
    values_types = []
    message = ''
    cursor = connection.cursor()
    # Possible bug, timestamp comparisson
    query = ("SELECT val.pk_id, val.name, val.price, val.quantity, val.offerant, "
             "val.rent_type, val.val_type, COUNT(val.pk_id) AS freq "
             "FROM solicitude INNER JOIN val ON solicitude.val = val.pk_id "
             "WHERE solicitude.time_created BETWEEN TO_DATE(%s, 'YYYY-MON-DD') "
             "AND TO_DATE(%s, 'YYYY-MON-DD') "
             "GROUP BY freq "
             "ORDER BY val.val_type, val.name ")
    query += sorting_criteria
    parameters = [date1, date2]
    cursor.execute(query, parameters)
    ans = [i for i in cursor.fetchall()]
    if len(ans) == 0:
        objects = None
        message = 'Lo sentimos, la busqueda no produjo resultados'
    else:
        for item in ans:
            pk_id = item[0]
            name = item[1]
            price = item[2] 
            quantity = item[3] 
            offerant = item[4]
            rent_type = item[5]
            val_type = item[6]
            to_add = val.Val(pk_id, name, price, quantity, offerant)

            objects.append(to_add)
            values_types.append(val_type)


    ans = (objects, values_types, message)
    return ans

def best_employees(value_type, value_name):
    objects = []
    msg = ''
    cursor = connection.cursor()
    sell_query = ("SELECT DISTINCT pk_id, name, price, quantity, offerant, rent_type, val_type FROM "
                     "      (SELECT * FROM ownerval INNER JOIN val ON val.pk_id = ownerval.val) owners "
                     "  INNER JOIN "
                     "      (SELECT * FROM active WHERE passive = %s) employees "
                     "  ON owners.owner = employees.login "
                     "WHERE "
                     "  (val_type = %s OR rent_type = %s OR offerant = %s OR login = %s)"
                     "ORDER BY "
                 )

    buy_query = ("SELECT DISTINCT pk_id, name, price, quantity, offerant, rent_type, val_type FROM "
                     "      (SELECT * FROM ownerval INNER JOIN val ON val.pk_id = ownerval.val) owners "
                     "  INNER JOIN "
                     "      (SELECT * FROM active WHERE passive = %s) employees "
                     "  ON owners.owner = employees.login "
                     "WHERE "
                     "  (val_type = %s OR rent_type = %s OR offerant = %s OR login = %s)"
                     "ORDER BY "
                 )

    connection.close()
    ans = (objects, msg)
    return ans



