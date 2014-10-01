######################## DJANGO IMPORTS ########################
from django.db import connection
from django.shortcuts import render, redirect

######################## CUSTOM IMPORTS ########################
from genericusers.views import get_user
import random, string


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
        return render(request, 'new_solicitude', params)

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
    params = {}
    if request.method == 'POST':
        valid, error = is_valid_pending_solicitudes(request.POST)
        if valid:
            params['message'] = 'Solicitudes activadas correctamente!'
        else:
            params['message'] = error
    solicitudes = get_passive_pending_solicitudes(username)
    params['solicitudes'] = solicitudes
    if len(solicitudes) == 0:
        params['message'] = 'No tienes solicitudes pendientes!'
    return render(request, 'active_solicitudes.html', params)

def passive_solicitudes(request):
    '''Returns the respective response to the passive_pending_solicitudes url call.'''
    username = check_username(request)
    if not username:
        return redirect('/users/home/')


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


################################################################
################### LOW LEVEL AUX FUNCTIONS ####################
################################################################

