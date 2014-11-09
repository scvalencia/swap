from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import transaction, connection
from django.views.generic import View

from dao import GenericUserDao
from actives.dao import ActiveDao
from passives.dao import PassiveDao
from offerants.dao import OfferantDao
from investors.dao import InvestorDao
from portfolios.dao import PortfolioDao
from solicitudes.dao import SolicitudeDao
from genericusers.dao import GenericUserDao
from swaptransactions.dao import SwapTransactionDao
from vals.dao import RentDao
from vals.dao import ValDao
from .forms import LoginForm, SignupForm
import json
import random


############################################################################
################################## VIEWS ###################################
############################################################################


class RetireView(View):
    def get(self, request, *args, **kwargs):
        num = get_register(request.session['user'])
        if num: 
            remove_passive(num)
            request.session.flush()
        return redirect('/')


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


class SearchView(View):
    """
    The view endpoint of the search url.
    """
    template_name = 'genericusers/search.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UserZoneView(View):
    """
    The view endpoint of the userzone url.
    """

    def get(self, request, *args, **kwargs):
        if request.session.get('user') and request.session.get('type'):
            if request.session.get('type') == 'activo':
                return render(request, 'genericusers/active.html')
            elif request.session.get('type') == 'pasivo':
                return render(request, 'genericusers/passive.html')
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


class LogoutView(View):
    """
    The view endpoint of the logout url.
    """
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return redirect('/')


class MovView(View):
    """
    The view endpoint for Mov.
    """
    def post(self, request, *args, **kwargs):
        info = json.loads(request.body)
        inicio = info['inicio']
        fin = info['fin']
        criType = info['criType']
        num = criType['num']
        criVal = info['criVal']
        follow = info['follow']
        data = getMovViewInfo(inicio, fin, num, criVal, follow)
        return HttpResponse(json.dumps(data), content_type="application/json")


class PorView(View):
    """
    The view endpoint for Por.
    """
    def post(self, request, *args, **kwargs):
        info = json.loads(request.body)
        valType = info['valType']
        minVal = info['minVal']
        data = getPorViewInfo(valType, minVal)
        return HttpResponse(json.dumps(data), content_type="application/json")


class IdView(View):
    """
    The view endpoint for Id.
    """
    def post(self, request, *args, **kwargs):
        info = json.loads(request.body)
        idVal = info['idVal']
        data = getIdViewInfo(idVal)
        return HttpResponse(json.dumps(data), content_type="application/json")


############################################################################
################################ FUNCTIONS #################################
############################################################################

 
def getMovViewInfo(inicio, fin, num, criVal, follow):
    # TODO
    # ACA DEBE RETORNAR UN ARREGLO DE DICCIONARIOS QUE YO CONVERTIRE ARRIBA A JSON
    # DONDE DADO UNA FECHA DE INICIO, UN FECHA FIN (RANGO DE FECHAS), UN TIPO DE
    # CRITERIO (NUM) QUE USTED DECIDE COMO MANEJAR PERO DOCUMENTE COMO MANEJO
    # (EJEMPLO PUEDE DECIRME QUE num=1 ES TIPO DE VALOR, num=2 ES TIPO DE RENTA Y ASI),
    # UN VALOR PARA ESE CRITERIO (cryVal) Y UNA OPCION FOLLOW QUE PUEDE SER SI O NO,
    # ESA OPCION FOLLOW SIGNIFICA QUE SI ESTA PUESTA CON VALOR "Si", ENTONCES BUSCARA
    # LOS MOVIMIENTOS DE VALORES (TRANSACCIONES) QUE HAYAN SIDO REALIZADOS EN ESE RANGO
    # DE FECHA Y TENGAN VALORES CON ESE CRITERIO, EN CASO DE QUE FOLLOW SEA "No", SERA
    # IGUAL PERO SERAN VALORES QUE NO TENGAN ESE CRITERIO.
    return []


def getPorViewInfo(valType, minVal):
    # TODO
    # ACA DEBE RETORNAR UN ARREGLO DE DICCIONARIOS QUE YO CONVERTIRE ARRIBA A JSON
    # DONDE DADO EL TIPO DEL VALOR (USTED DECIDA QUE TIPOS DEBEN LLEGARLE) Y UN
    # MONTO MINIMO, DEVUELVA LA LOS PORTAFOLIOS QUE CONTIENEN VALORES DE ESE TIPO
    # Y QUE HAN TENIDO OPERACIONES CON MONTO MAYOR A ESE MONTO.
    return []


def getIdViewInfo(idVal):
    # TODO
    # ACA DEBE RETORNAR UN ARREGLO DE DICCIONARIOS QUE YO CONVERTIRE ARRIBA A JSON
    # DONDE DADO EL ID DEL VALOR, DEVUELVA LA INFORMACION DE LOS PORTAFOLIOS EN LOS 
    # QUE HA ESTADO INVOLUCRADO.
    return []


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


def get_register(user_login):
    ans = None
    cursor = connection.cursor()
    query = "SELECT passive_register FROM passives WHERE user_login = %s"
    cursor.execute(query, [user_login])
    items = [_ for _ in cursor.fetchall()]
    if len(items) != 0:
        ans = items.pop()[0]
    return ans


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
    ans = {}
    if param == 'passives':
        ans = get_passives()
    elif param == 'offerants':
        ans = get_offerants()
    elif param == 'investors':
        ans = get_investors()
    elif param == 'actives':
        ans = get_most_active_actives()
    elif param == 'vals':
        ans = get_most_active_values()
    return ans


def get_passives():
    ans = {'passives' : []}
    passives = PassiveDao()
    all_passives = passives.find_all()
    for itm in all_passives:
        ans['passives'].append(process_passive(itm))
    return ans


def get_offerants():
    ans = {'offerants' : []}
    offerants = OfferantDao()
    all_offerants = offerants.find_all()
    for itm in all_offerants:
        ans['offerants'].append(process_offerant(itm))
    return ans

def get_investors():
    ans = {'investors' : []}
    investors = InvestorDao()
    all_investors = investors.find_all()
    for itm in all_investors:
        ans['investors'].append(process_investor(itm))
    return ans

def process_passive(passive_object):
    bare_sct = passive_object.__dict__
    passive_register = bare_sct['passive_register']
    user_login = bare_sct['user_login']
    bare_sct['investors'] = []
    bare_sct['solicitudes'] = []
    bare_sct['transaction'] = []

    def process_actives_for_passive(passive_register):
        from django.db import connection
        ans = []
        cursor = connection.cursor()
        query = "SELECT * FROM activespassives WHERE passive_register = %s"
        params = [passive_register]
        cursor.execute(query, params)
        elements = [_ for _ in cursor.fetchall()]
        for itm in elements:
            active_login = itm[0]
            active_object = ActiveDao().find_by_login(active_login)[0]
            ans.append(active_object)
        connection.close()
        return ans

    def process_solicitudes(active_login):
        from django.db import connection
        ans = []
        cursor = connection.cursor()
        query = "SELECT * FROM solicitudes WHERE active_login = %s"
        params = [active_login]
        cursor.execute(query, params)
        elements = [_ for _ in cursor.fetchall()]
        for itm in elements:
            solicitude_object = SolicitudeDao().process_row(itm)
            ans.append(solicitude_object)
        connection.close()
        return ans

    def process_transactions(solicitude_pk):
        from django.db import connection
        ans = []
        cursor = connection.cursor()
        query = "SELECT * FROM swap_transactions WHERE solicitude_1_pk = %s OR solicitude_2_pk = %s"
        params = [solicitude_pk, solicitude_pk]
        cursor.execute(query, params)
        elements = [_ for _ in cursor.fetchall()]
        for itm in elements:
            transaction_object = SwapTransactionDao().process_row(itm)
            ans.append(transaction_object)
        connection.close()
        return ans

    actives_objects = process_actives_for_passive(passive_register)
    for itm in actives_objects:
        bare_sct['investors'].append(process_active(itm))
    active_logins = [i.user_login for i in actives_objects]
    solicitudes = []
    for active_login in active_logins:
        solicitudes_for_active = process_solicitudes(active_login)
        solicitudes.extend(solicitudes_for_active)
    for itm in solicitudes:
        bare_sct['solicitudes'].append(process_solicitude(itm))
    solicitude_ids = [i.pk_id for i in solicitudes]
    transactions = []
    for solicitude_id in solicitude_ids:
        transactions_for_such_id = process_transactions(solicitude_id)
        transactions.extend(transactions_for_such_id)
    for itm in transactions:
        bare_sct['transaction'].append(process_transaction(itm))

    return bare_sct

def process_solicitude(solicitude_object):
    dct = solicitude_object.__dict__
    dct['created_at'] = str(dct['created_at'])
    return dct

def process_transaction(transaction_object):
    dct = transaction_object.__dict__
    dct['created_at'] = str(dct['created_at'])
    return dct

def process_investor(investor_object):
    bare_sct = investor_object.__dict__
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

    return bare_sct


def process_offerant(offerant_object):
    bare_sct = offerant_object.__dict__
    user_login = bare_sct['user_login']
    offerant_type = bare_sct['offerant_type']
    bare_sct['portfolios'] = []

    def get_portfolios_per_offerant(user_login):
        ans = []
        portfolios = PortfolioDao().find_by_user_login(user_login)
        for itm in portfolios:
            ans.append(itm)
        return ans

    for itm in get_portfolios_per_offerant(user_login):
        bare_sct['portfolios'].append(process_portfolio(itm))
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
        query = ("SELECT vals.pk_id, vals.val_name, vals.description, "
                 "vals.val_type, vals.amount, vals.price, vals.rent_id FROM "
                 "portfolios_vals INNER JOIN vals ON portfolios_vals.pk_val = "
                 "vals.pk_id WHERE portfolios_vals.pk_portfolio = %s")
        params = [pk_portfolio]
        cursor.execute(query, params)
        items = [itm for itm in cursor.fetchall()]
        for item in items:
            pk_val = item[0]
            val_object = ValDao().find_by_id(pk_val).pop()
            ans.append(val_object)
        connection.close()
        return ans

    values_on_portfolio = get_values_on_portfolio(pk_id)
    for value_object in values_on_portfolio:
        bare_sct['values'].append(process_value(value_object))
    return bare_sct

def process_active(active_object):
    return active_object.__dict__


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
    return bare_sct


def process_rent(rent_object):
    return rent_object.__dict__

def get_random_objects(obj):
    ans = []
    if obj == 'actives':
        ans = get_most_active_actives()
    elif obj == 'values':
        ans = get_most_active_values()
    return ans

def get_most_active_values():
    ans = []
    values = ValDao().find_all()
    values = [_.__dict__ for _ in values]
    return values
    '''
    random_length = random.randrange(len(values))
    i = 0
    while(i < random_length):
        choice = random.choice(values)
        if choice not in ans:
            ans.append(choice)
        i += 1
    return ans
    '''

def get_most_active_actives():
    ans = []
    actives = ActiveDao().find_all()
    actives = [_.__dict__ for _ in actives]
    print actives
    return actives
    '''
    random_length = random.randrange(len(actives))
    i = 0
    while(i < random_length):
        choice = random.choice(actives)
        if choice not in ans:
            ans.append(choice)
        i += 1
    return ans
    '''

@transaction.commit_manually
def remove_passive(num_register):
    ans = True
    obj = PassiveDao().find_by_register(num_register)
    try:
        # Remove from activespassives DONE
        # Pass to other pasivo from solicitude
        # Remove from passive
        # Si tiene mas pasivos, adicionar a esos, de otra forma adicionarle al de menor carga
        cursor = connection.cursor()
        lazy_passive_query = ("SELECT PASSIVES.* "
                              "FROM PASSIVES "
                              "INNER JOIN "
                                "(SELECT * FROM "
                                    "(SELECT passive_register, COUNT(passive_register) AS freq "
                                     "FROM ACTIVESPASSIVES GROUP BY passive_register) "
                                     "WHERE freq = "
                                        "(SELECT MIN(freq) "
                                         "FROM "
                                            "(SELECT passive_register, COUNT(passive_register) AS freq "
                                             "FROM ACTIVESPASSIVES GROUP BY passive_register) "
                                     ")) "
                              "T ON T.PASSIVE_REGISTER = PASSIVES.PASSIVE_REGISTER")
        cursor.execute(lazy_passive_query)
        lazy_passive = PassiveDao().process_row([itm for itm in cursor.fetchall()][0])
        

        # Si el activo tiene mas pasivos no hacer nada, de otra forma poner a lazy_passive
        passives_actives_freq = ("SELECT x.ACTIVE_LOGIN, freq FROM "
                                "       (SELECT active_login, COUNT(active_login) AS freq "
                                "       FROM ACTIVESPASSIVES GROUP BY(ACTIVE_LOGIN)) x "
                                "   INNER JOIN "
                                "       (SELECT * FROM ACTIVESPASSIVES WHERE PASSIVE_REGISTER = %s) t "
                                "   ON t.ACTIVE_LOGIN = x.active_login")

        cursor.execute(passives_actives_freq, [num_register])
        lazy_passive_login = lazy_passive.user_login 
        lazy_passive_regis = lazy_passive.passive_register

        items = [_ for _ in cursor.fetchall()]
        print items
        for item in items:
            active_login = item[0]
            freq = int(item[1])
            try:
                remover_query = "DELETE * FROM activespassives WHERE passive_register = %s"
                cursor.execute(remover_query, [num_register])
            except Exception as e:
                print e
            PassiveDao().remove(lazy_passive_regis)
            GenericUserDao().remove(lazy_passive_login)


            if freq == 1:                
                insert_query = "INSERT INTO ACTIVESPASSIVES VALUES(%s, %s)"
                cursor.execute(insert_query, [active_login, lazy_passive_regis])
            else:
                continue

    except:
        ans = False
        transaction.rollback()        
    else:
        transaction.commit()

    return ans

