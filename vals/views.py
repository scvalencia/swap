######################## DJANGO IMPORTS ########################
from django.shortcuts import render, redirect
from django.db import connection

######################## CUSTOM IMPORTS ########################
import val
from genericusers.views import get_user


################################################################
######################## VIEW FUNCTIONS ########################
################################################################   

def search(request):
    '''Returns the respective response to the search url call.'''
    username, user_type = check_username(request)
    if not username or (user_type != '1' and user_type != '2'):
        return redirect('/users/home/')
    passives = get_passives()
    actives = get_actives()
    ordering_parameters = ['name', 'price', 'quantity', 'offerant', 'rent_type', 'value_type']
    params = {
        'passives': passives,
        'actives': actives,
        'ordering_parameters': ordering_parameters,
        'results': [],
        'message': '',
    }
    if request.method == 'POST':
        request.POST['active_solicitude'] = False if '0' else True
        request.POST['desc'] = False if '0' else True
        results, error = is_valid_search(request.POST)
        if results:
            params['results'] = results
        else:
            params['message'] = error
        return render(request, 'search.html', params)
    else:
        return render(request, 'search.html', params)


################################################################
################## HIGH LEVEL AUX FUNCTIONS ####################
################################################################

def is_valid_search(form_data):
    '''Revisa validez de la busqueda'''
        #filter_values(value_type, rent_type, id_offerant,
    #          id_passive, id_active, ordering_flag,
    #          active_solicitude = True, desc = True)

    #search_params = ['bono', 'renta', 'Pepsi', 'lulu', 'wer', 'name',]
    # 
    value_type = form_data.get('value_type')
    rent_type = form_data.get('rent_type')
    id_offerant = form_data.get('id_offerant')
    id_passive = form_data.get('id_passive')
    id_active = form_data.get('id_active')
    ordering_flag = form_data.get('ordering_flag')
    active_solicitude = form_data.get('active_solicitude')
    desc = form_data.get('desc')
    search_params = [value_type, rent_type, id_offerant, id_passive,
                    id_active, ordering_flag, active_solicitude, desc]
    if (not_null(search_params)):
        return filter_values(*search_params)
    else:
        return 'False', 'Todos los campos deben ser validos'

def not_null(search_params):
    for itm in search_params:
        if not itm:
            return False
    return True

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

################################################################
################### LOW LEVEL AUX FUNCTIONS ####################
################################################################


def get_all_vals():
	ans = []
	cursor = connection.cursor()
	query = "SELECT * FROM val"
	cursor.execute(query)
	values = [itm for itm in cursor.fetchall()]
	for itm in values:
		pk_id = itm[0]
		name = itm[1]
		price = itm[2]
		quantity = itm[3]
		offerant = itm[4]
		to_Add = val.Val(pk_id, name, price, quantity, offerant)
		ans.append(to_Add)
	return ans

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
        for value in resulting_set:
            pk_id = value[0] 
            name = value[1] 
            price = value[2] 
            quantity = value[3]
            offerant = value[4]
            value_object = val.Val(pk_id, name, price, quantity, offerant)
            new_query = "SELECT * FROM solicitude WHERE val = %s AND is_active = %s"
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