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
    if request.method == 'POST':
        valid, error = is_valid_new_solicitude(request.POST)
        params = {
            #TODO insert post form inputs
            'message': error,
        }
        if valid:
            params = {
                #TODO insert blank form inputs
                'message': 'Tu solicitud fue creada satisfactoriamente!',
            }
        return render(request, 'new_solicitude.html', params)
    else:
        params = {
            #TODO insert blank form inputs
        }
        return render(request, 'new_solicitude', params)

def active_solicitudes(request):
    pass
    #TODO

def passive_pending_solicitudes(request):
    pass
    #TODO

def passive_solicitudes(request):
    pass
    #TODO


################################################################
################## HIGH LEVEL AUX FUNCTIONS ####################
################################################################


def check_username(request):
    username = request.session.get('username')
    if username:
        user = get_user(username)[0]
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

