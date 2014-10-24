from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from dao import GenericUserDao
from actives.dao import ActiveDao
from passives.dao import PassiveDao
from offerants.dao import OfferantDao
from investors.dao import InvestorDao
from portfolios.dao import PortfolioDao
from vals.dao import RentDao
from vals.dao import ValDao
from .forms import LoginForm, SignupForm
import json


class APIView(View):
    """
    The API from passives
    """
    def get(self, request, *args, **kwargs):
        param = kwargs.get('param')
        data = get_data(param)
        print 'DATAAA', data
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

    def get(self, request, *args, **kwargs):
        if request.session.get('user') and request.session.get('type'):
            return render(request, 'genericusers/profile.html')
        else:
            params = {
                'login_form': LoginForm(),
                'signup_form': SignupForm(),
            }
            return render(request, 'genericusers/userzone.html', params)

    def post(self, request, *args, **kwargs):
        in_data = json.loads(request.body)
        if in_data.get('form_type') == 'login':
            valid = validate_login(request, in_data)
            if valid:
                for i in request.session.keys(): print i, '->', request.session[i]
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=403)
        elif in_data.get('form_type') == 'signup':
            valid = validate_signup(request, in_data)
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


def validate_login(request, in_data):
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
        request.session['user'] = user_login
        request.session['type'] = tipo_usuario
        return True
    else:
        return False


def validate_signup(request, in_data):
    generic_users = GenericUserDao()
    users_with_such_login = generic_users.find_by_login(user_login)
    if len(users_with_such_login) == 0:
        arg_login = in_data['login']
        arg_user_id = in_data['id']
        arg_user_pass = in_data['password']
        arg_first_name = in_data['first_name']
        arg_last_name = in_data_['last_name']
        arg_email = in_data['email']
        arg_phone = in_data['phone']
        request.session['login'] = user_login
        request.session['type'] = tipo_usuario
        generic_users.insert(arg_login, arg_user_id, arg_user_pass, 
            arg_first_name, arg_last_name, arg_email, arg_phone)
        request.session['login'] = user_login
        request.session['type'] = tipo_usuario
        return True
    else:
        return False


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
    # bolsa y portafolio.

    # Si es investor, los valores que tiene en la bolsa y 
    # portafolio.
    ans = {}
    if param == 'passives':
        ans = get_passives()
    elif param == 'offerants':
        ans = get_offerants()
    elif param == 'investors':
        ans = get_investors()
    return ans

def get_passives():
    pass

def process_passive(passive_object):
    bare_sct = offerant_object.__dict__
    passive_register = bare_sct['passive_register']
    user_login = bare_sct['user_login']
    bare_sct['investors'] = []
    bare_sct['solicitudes'] = []
    bare_sct['transaction'] = []

    def process_active_for_passive():
        pass

    def process_solicitude():
        pass

    def process_transaction():
        pass

def get_offerants():
    ans = {'offerants' : []}
    offerants = OfferantDao()
    all_offerants = offerants.find_all()
    for itm in all_offerants:
        print itm
        ans['offerants'].append(process_offerant(itm))
    return ans

def get_investors():
    ans = {'investors' : []}
    investors = InvestorDao()
    all_investors = investors.find_all()
    for itm in all_investors:
        print itm
        ans['investors'].append(process_investor(itm))
    print ans
    return ans

def process_investor(investor_object):
    bare_sct = offerant_object.__dict__
    user_login = bare_sct['user_login']
    is_enterprise = bare_sct['is_enterprise']
    bare_sct['portfolios'] = []

    def get_portfolios_per_investor(user_login):
        ans = []
        portfolios = PortfolioDao().find_by_user_login(user_login)
        for itm in portfolios:
            ans.append(itm)
        return ans

    for itm in get_portfolios_per_investor(user_login):
        bare_sct['portfolios'].append(process_portfolio(itm))

    print bare_sct
    return bare_sct

def process_offerant(offerant_object):
    bare_sct = offerant_object.__dict__
    user_login = bare_sct['user_login']
    offerant_type = bare_sct['offerant_type']
    bare_sct['portfolios'] = []

    def get_portfolios_per_offerant(user_login):
        ans = []
        print user_login
        portfolios = PortfolioDao().find_by_user_login(user_login)
        print 'WE GTOT IT BRO'
        for itm in portfolios:
            print itm, '---------------'
            ans.append(itm)
        print 'AND THIS IS THE END'
        return ans

    for itm in get_portfolios_per_offerant(user_login):
        bare_sct['portfolios'].append(process_portfolio(itm))
    print 'OFFERANT'
    print bare_sct
    return bare_sct    

def process_portfolio(portfolio_object):
    bare_sct = portfolio_object.__dict__
    pk_id = bare_sct['pk_id']
    user_login = bare_sct['user_login']
    risk = bare_sct['risk']
    bare_sct['values'] = []

    def get_values_on_portfolio(pk_portfolio):
        from django.db import connection
        ans = []
        cursor = connection.cursor()
        query = "SELECT * FROM portfolios_vals WHERE pk_portfolio = %s"
        params = [pk_portfolio]
        cursor.execute(query, params)
        items = [itm for itm in cursor.fetchall()]
        for item in items:
            ans.append(ValDao().process_row(item))
        connection.close()
        return ans

    values_on_portfolio = get_values_on_portfolio(pk_id)
    for value_object in values_on_portfolio:
        bare_sct['values'].append(process_value(value_object))
    print 'POTFOLIO'
    print bare_sct
    return bare_sct

def process_value(val_object):
    bare_sct = val_object.__dict__
    pk_id = bare_sct['pk_id']
    val_name = bare_sct['val_name']
    description = bare_sct['description']
    val_type = bare_sct['val_type']
    amount = bare_sct['amount']
    price = bare_sct['price']
    rent_id = bare_sct['rent_id']
    rent_object = RentDao().find_by_id(rent_id)
    to_append = None
    if len(rent_object) == 1:
        to_append = process_rent(rent_object[0])
    bare_sct['rent_id'] = to_append
    print 'VALUE'
    print bare_sct
    return bare_sct

def process_rent(rent_object):
    print 'RENT'
    print rent_object.__dict__
    return rent_object.__dict__
