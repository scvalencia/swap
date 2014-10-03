######################## DJANGO IMPORTS ########################
from django.shortcuts import render
from django.db import connection

######################## CUSTOM IMPORTS ########################
import val


################################################################
######################## VIEW FUNCTIONS ########################
################################################################


def search(request):
    #filter_values(value_type, rent_type, id_offerant,
    #          id_passive, id_active, ordering_flag,
    #          active_solicitude = True, desc = True)
    '''Returns the respective response to the search url call.'''
    ordering_parameters = ['name', 'price', 'quantity', 'offerant', 'rent_type', 'value_type']
    results = filter_values(None, None, None, 'lulu', 'wer', 'name',
              active_solicitude = True, desc = True)
    params = { 'results': results }
    print results
    return render(request, 'search.html', params)


################################################################
################## HIGH LEVEL AUX FUNCTIONS ####################
################################################################



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
    general_query1 = ("SELECT DISTINCT pk_id, name, price, quantity, offerant, rent_type, val_type FROM "
                     "      (SELECT * FROM ownerval INNER JOIN val ON val.pk_id = ownerval.val) owners "
                     "  INNER JOIN "
                     "      (SELECT * FROM active WHERE passive = %s) employees "
                     "  ON owners.owner = employees.login "
                     "WHERE "
                     "  (val_type = %s OR rent_type = %s OR offerant = %s OR login = %s)"
                     "ORDER BY "
                    )
    general_query = ("SELECT DISTINCT pk_id, name, price, quantity, offerant, rent_type, val_type FROM val")
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
        cursor.execute(general_query1)
        resulting_set = [i for i in cursor.fetchall()]
        print resulting_set
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