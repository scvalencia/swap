######################## DJANGO IMPORTS ########################
from django.db import connection
from django.shortcuts import render, redirect

######################## CUSTOM IMPORTS ########################
from genericusers.views import get_user
from solicitude import Solicitude


################################################################
######################## VIEW FUNCTIONS ########################
################################################################


def new_solicitude(request):
    '''Returns the respective response to the new_solicitude url call.'''
    username = check_username(request)
    if not username:
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
    username = check_username(request)
    if not username:
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
    username = check_username(request)
    if not username:
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
    username = check_username(request)
    if not username:
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

def is_valid_pending_solicitudes(form_data):
    # TODO jcbages
    return True, ''


################################################################
################### LOW LEVEL AUX FUNCTIONS ####################
################################################################


def get_active_solicitudes(username):
    # TODO scvalencia
    # Necesito todas las solicitudes que ha hecho este activo
    # que figuran como NOT SOLVED porque si estan en SOLVED la
    # idea es mostrarlas en la parte de transactions, pero debe
    # retornar un arreglo de objectos tipo solicitud osea usando
    # la clase de solicitud.py.
    return []

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