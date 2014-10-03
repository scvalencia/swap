######################## DJANGO IMPORTS ########################
from django.shortcuts import render

######################## CUSTOM IMPORTS ########################
from genericusers.views import get_user


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
    return []