######################## DJANGO IMPORTS ########################
from django.shortcuts import render
from django.db import connection

######################## CUSTOM IMPORTS ########################
from genericusers.views import get_user
from swaptransaction import Swaptransaction


################################################################
######################## VIEW FUNCTIONS ########################
################################################################


def active_transactions(request):
    '''Returns the respective response to the active_solicitudes url call.'''
    username, user_type = check_username(request)
    if not username or user_type != '1':
        return redirect('/users/home/')
    transactions = get_active_transactions(username)
    params = {
        'transactions': transactions,
        'message': ''
    }
    if len(transactions) == 0:
        params['message'] = 'Actualemente no tienes transacciones, vuelve mas tarde!'
    return render(request, 'active_transactions.html', params)


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

################################################################
################### LOW LEVEL AUX FUNCTIONS ####################
################################################################


def get_active_transactions(username):
    # TODO scvalencia
    # igual que el get active solicitudes pero pues
    # paseme las transacciones que ha realizado este usuario
    # es decir que como transaccion tiene una solicitud de compra
    # y una de venta entonces si ese username esta como active_login
    # en alguna de las dos, pues esa transaccion cuenta para este activo
    # retorneme uan lista de objetos swaptransaction
    objects = []
    msg = 'Proceso exitoso'
    cursor = connection.cursor()
    query = ("SELECT * FROM swaptransaction, solicitude, active "
             "WHERE (swaptransaction.sell_solicitude = solicitude.pk_id "
             "OR swaptransaction.buy_solicitude = solicitude.pk_id) "
             "AND active.login = %s")
    cursor.execute(query, [username])
    result_set = [i for i in cursor.fetchall()]
    if len(result_set) == 0:
        msg = 'No hay tales transacciones'
    for itm in result_set:
        pk_id = itm[0]
        time_created = itm[1]
        sell_solicitude = itm[2]
        buy_solicitude = itm[3]
        obj = Swaptransaction(pk_id, time_created, sell_solicitude, buy_solicitude)
        objects.append(obj)
    connection.close()
    ans = (objects, msg)
    return ans