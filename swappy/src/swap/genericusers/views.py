from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from .forms import LoginForm, SignupForm
import json


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


def validate_login(in_data):
    # TODO
    # Dado un diccionario con valores para
    # user y password, verificar si el usuario
    # existe, en caso de existir, agregar las
    # respectivas cookies (usuario y tipo_usuario)
    # y retornar True, de lo contrario, False.
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