from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from dao import GenericUserDao
from actives.dao import ActiveDao
from .forms import LoginForm, SignupForm
import json


class APIView(View):
    """
    The API from passives
    """
    def get(self, request, *args, **kwargs):
        param = kwargs.get('param')
        data = get_data(param)
        return HttpResponse(json.dumps(data), content_type="application/json")


class AdminView(View):
    """
    The view endpoint of the home url.
    """
    template_name = 'genericusers/admin.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class HomeView(View):
    """
    The view endpoint of the home url.
    """
    template_name = 'genericusers/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UserZoneView(View):
    """
    The view endpoint of the userzone url.
    """
    template_name = 'genericusers/userzone.html'

    def get(self, request, *args, **kwargs):
        params = {
            'login_form': LoginForm(),
            'signup_form': SignupForm(),
        }
        return render(request, self.template_name, params)

    def post(self, request, *args, **kwargs):
        in_data = json.loads(request.body)
        if in_data.get('form_type') == 'login':
            valid = validate_login(in_data)
            if valid:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=403)
        elif in_data.get('form_type') == 'signup':
            valid = validate_signup(in_data)
            if valid:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=403)
        else:
            return HttpResponse(status=404)


class SearchView(View):
    """
    The view endpoint of the search url.
    """
    template_name = 'genericusers/search.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def validate_login(in_data):
    # TODO
    # Dado un diccionario con valores para
    # user y password, verificar si el usuario
    # existe, en caso de existir, agregar las
    # respectivas cookies (usuario y tipo_usuario)
    # y retornar True, de lo contrario, False.
    user_login = in_data['user']
    user_password = in_data['password']
    generic_users = GenericUserDao()
    users_with_such_login = generic_users.find_by_login(user_login)
    tipo_usuario = None
    if len(users_with_such_login) == 1:
        if_active = ActiveDao()
        active_users = if_active.find_by_login(user_login)
        if len(active_users) == 1:
            tipo_usuario = 'activo'
        else:
            tipo_usuario = 'pasivo'
        return True
    else:
        return False



    return in_data.get('user') == 'juan'


def validate_signup(in_data):
    # TODO
    # Dado un diccionario con valores para
    # nuevo usuario (login, user_id, user_pass,
    # first_name, last_name, email, phone),
    # verificar si el usuario existe, en caso
    # de existir, retornar False, de lo contrario,
    # agregar las respectivas cookies (usuario
    # y tipo_usuario) y retornar True.
    return True


def get_data(param):
    # TODO
    # Dado un parametro (passives, offerants o investors)
    # devolver la tabla en forma de diccionario con los
    # datos de todas las filas de la misma, en caso de 
    # no haber resultados, retornar un diccionario vacio.

    # Si es passive, incluir inversionistas, portafolios
    # valores en negociacion, solicitudes y transacciones
    # y portafolio.

    # Si es offerant, incluir los valores que tiene en la
    # bolsa y como estan distribuidos (portafolio).

    # Si es investor, los valores que tiene en la bolsa y 
    # como estan distribuidos (portafolio).
    return {}
