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

import timeTracker


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


# R1
def get_movement_info1(value_id, val_type, rent_type, active_login, passive_login, date1, date2):
    # Formato fecha 'yyyy-mm-dd', cuidado con los rangos de fecha, cuidar bounds de cada dato
    # val_type es '0', o '1', punto, igual rent_type
    # los login son simplemente strings
    query = ''' SELECT SOLICITUDE, VAL, VAL_TYPE, CREATED_AT, ACTIVE_LOGIN, PASSIVE_REGISTER, USER_LOGIN, RENT_TYPE, VAL_NAME 
                FROM
                    (
                        SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVE_LOGIN, PASSIVES.PASSIVE_REGISTER, USER_LOGIN, VAL_NAME 
                        FROM  
                            (
                                SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVESPASSIVES.ACTIVE_LOGIN, PASSIVE_REGISTER, VAL_NAME
                                FROM
                                    (
                                        SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVE_LOGIN, VAL_NAME  
                                        FROM
                                            (
                                                SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVE_LOGIN, VAL_NAME 
                                                FROM 
                                                    (
                                                        SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, VAL_NAME
                                                        FROM
                                                        (
                                                            SOLICITUDES_VAL INNER JOIN VALS 
                                                            ON VALS.PK_ID = SOLICITUDES_VAL.VAL
                                                        )
                                                    ) 
                                                SOLICITUDES_INFO INNER JOIN SOLICITUDES 
                                                ON SOLICITUDES_INFO.SOLICITUDE = SOLICITUDES.PK_ID
                                            ) 
                                        INFO1 INNER JOIN ACTIVES 
                                        ON INFO1.ACTIVE_LOGIN = ACTIVES.USER_LOGIN
                                    ) 
                                INFO2 INNER JOIN ACTIVESPASSIVES 
                                ON ACTIVESPASSIVES.ACTIVE_LOGIN = INFO2.ACTIVE_LOGIN
                            ) 
                        INFO3 INNER JOIN PASSIVES 
                        ON PASSIVES.PASSIVE_REGISTER = INFO3.PASSIVE_REGISTER
                    ) 
                INFO4 INNER JOIN RENTS 
                ON INFO4.RENT_ID = RENTS.PK_ID
                WHERE   
                    val = %s AND 
                    VAL_TYPE = %s AND 
                    RENT_TYPE = %s AND
                    ACTIVE_LOGIN = %s AND
                    USER_LOGIN = %s AND 
                    CREATED_AT >= TO_TIMESTAMP(%s,'yyyy-mm-dd') AND 
                    CREATED_AT < TO_TIMESTAMP(%s,'yyyy-mm-dd')
        '''
    params = [value_id, val_type, rent_type, active_login, passive_login, date1, date2]
    cursor = connection.cursor()
    cursor.execute(query, params)
    ans = []
    result_set = [_ for _ in cursor.fetchall()]
    for itm in result_set:
        solicitude = itm[0]
        value_id = itm[1]
        val_type = itm[2] 
        created_at = itm[3]
        active_login = itm[4]
        passive_register = itm[5]
        user_login = itm[6]
        rent_type = itm[7]
        val_name = itm[8]

        dct = {'solicitude_id' : solicitude, 'value_id' : value_id, 'value_type' : val_type,
               'created_at' : created_at, 'active_login' : active_login, 'rent_type' : rent_type,
               'passive_register' : passive_register, 'user_login' : user_login, 'value_name' : val_name}

        ans.append(dct)

    return ans


# R2
def get_movement_info2(value_id, val_type, rent_type, active_login, passive_login, date1, date2):
    # Formato fecha 'yyyy-mm-dd', cuidado con los rangos de fecha, cuidar bounds de cada dato
    # val_type es '0', o '1', punto, igual rent_type
    # los login son simplemente strings
    query = ''' SELECT SOLICITUDE, VAL, VAL_TYPE, CREATED_AT, ACTIVE_LOGIN, PASSIVE_REGISTER, USER_LOGIN, RENT_TYPE, VAL_NAME 
                FROM
                    (
                        SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVE_LOGIN, PASSIVES.PASSIVE_REGISTER, USER_LOGIN, VAL_NAME 
                        FROM  
                            (
                                SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVESPASSIVES.ACTIVE_LOGIN, PASSIVE_REGISTER, VAL_NAME
                                FROM
                                    (
                                        SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVE_LOGIN, VAL_NAME  
                                        FROM
                                            (
                                                SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVE_LOGIN, VAL_NAME 
                                                FROM 
                                                    (
                                                        SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, VAL_NAME
                                                        FROM
                                                        (
                                                            SOLICITUDES_VAL INNER JOIN VALS 
                                                            ON VALS.PK_ID = SOLICITUDES_VAL.VAL
                                                        )
                                                    ) 
                                                SOLICITUDES_INFO INNER JOIN SOLICITUDES 
                                                ON SOLICITUDES_INFO.SOLICITUDE = SOLICITUDES.PK_ID
                                            ) 
                                        INFO1 INNER JOIN ACTIVES 
                                        ON INFO1.ACTIVE_LOGIN = ACTIVES.USER_LOGIN
                                    ) 
                                INFO2 INNER JOIN ACTIVESPASSIVES 
                                ON ACTIVESPASSIVES.ACTIVE_LOGIN = INFO2.ACTIVE_LOGIN
                            ) 
                        INFO3 INNER JOIN PASSIVES 
                        ON PASSIVES.PASSIVE_REGISTER = INFO3.PASSIVE_REGISTER
                    ) 
                INFO4 INNER JOIN RENTS 
                ON INFO4.RENT_ID = RENTS.PK_ID
                WHERE   
                    val <> %s AND 
                    VAL_TYPE <> %s AND 
                    RENT_TYPE <> %s AND
                    ACTIVE_LOGIN <> %s AND
                    USER_LOGIN <> %s AND 
                    CREATED_AT >= TO_TIMESTAMP(%s,'yyyy-mm-dd') AND 
                    CREATED_AT < TO_TIMESTAMP(%s,'yyyy-mm-dd')
        '''
    params = [value_id, val_type, rent_type, active_login, passive_login, date1, date2]
    cursor = connection.cursor()
    cursor.execute(query, params)

    ans = []
    result_set = [_ for _ in cursor.fetchall()]
    for itm in result_set:
        solicitude = itm[0]
        value_id = itm[1]
        val_type = itm[2] 
        created_at = itm[3]
        active_login = itm[4]
        passive_register = itm[5]
        user_login = itm[6]
        rent_type = itm[7]
        val_name = itm[8]

        dct = {'solicitude_id' : solicitude, 'value_id' : value_id, 'value_type' : val_type,
               'created_at' : created_at, 'active_login' : active_login, 'rent_type' : rent_type,
               'passive_register' : passive_register, 'user_login' : user_login, 'value_name' : val_name}

        ans.append(dct)

    return ans


# R3
def get_portfolio_bound(value_type, bound):
    # value_type in ['0', '1']
    # bound is a number bigger than or equal 0
    query = str(''' SELECT val, frequency, val_name, val_type, amount, price, pk_portfolio, user_login, risk
                    FROM 
                    (
                        SELECT * 
                        FROM
                            (
                                SELECT * 
                                FROM
                                    (
                                        (
                                            SELECT val, COUNT(val) AS Frequency 
                                            FROM SOLICITUDES_VAL 
                                            GROUP BY val 
                                            ORDER BY COUNT(val) DESC
                                        ) 
                                        FREQ INNER JOIN VALS 
                                        ON FREQ.val = VALS.PK_ID
                                    )   
                                WHERE VAL_TYPE = %s AND FREQUENCY > %s
                            ) 
                            VALORES INNER JOIN PORTFOLIOS_VALS
                            ON VALORES.VAL = PORTFOLIOS_VALS.PK_VAL
                    ) 
                    PORTFOLIO_INFO INNER JOIN PORTFOLIOS
                    ON PK_PORTFOLIO = PK_ID 
            ''')
    params = [val_type, bound]
    cursor = connection.cursor()
    cursor.execute(query, params)

    ans = []
    result_set = [_ for _ in cursor.fetchall()]
    for itm in result_set:
        val = itm[0] 
        frequency = itm[1]
        val_name = itm[2]
        val_type = itm[3]
        amount = itm[4]
        price = itm[5]
        pk_portfolio = itm[6]
        user_login = itm[7]
        risk = itm[8]

        dct = {'val' : val, 'frequency' : frequency, 'val_name' : val_name, 'val_type' : val_type, 
               'amount' : amount, 'price' : price, 'pk_portfolio' : pk_portfolio, 'user_login' : user_login, 
               'risk' : risk}

        ans.append(dct)

    return ans


# R4
def get_portfolios_value(value_id):
    # value_id is an id value
    # Take care if was present3
    query = ''' SELECT pk_portfolio, user_login, risk  
                FROM
                    (
                        SELECT PK_PORTFOLIO 
                        FROM 
                        PORTFOLIOS_VALS INNER JOIN VALS 
                        ON PORTFOLIOS_VALS.PK_VAL = VALS.PK_ID 
                        WHERE PK_VAL = %s
                    ) 
                INFO INNER JOIN PORTFOLIOS 
                ON INFO.PK_PORTFOLIO = PORTFOLIOS.PK_ID
            '''
    params = [val_id]
    cursor = connection.cursor()
    cursor.execute(query, params)
    dates = sorted([random_date() for _ in range(20)])

    ans = []
    result_set = [_ for _ in cursor.fetchall()]
    for itm in result_set:
        pk_portfolio = itm[0] 
        user_login = itm[1]
        risk = itm[2]
        active = random.choice([True, False, False])
        date1, date2 = '', ''
        if not active:
            date1 = random_date()
            date2 = random_date()

        dates = sorted([date1, date2])

        dct = {'pk_portfolio' : pk_portfolio, 'user_login' : user_login, 'risk' : risk,
               'active' : active, 'date1' : date1, 'date2' : date2}

        ans.append(dct)

    return ans

def random_date():
    ans = ''
    ans += '2014-'
    ans += str(random.choice(range(10, 12)))
    dates = map(lambda _ : '0' + str(_) if _ < 10 else str(_), [_ for _ in range(20)])
    ans += '-' + dates[random.choice(range(20))]
    return ans


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

def reset_portfolio(new_portfolio_object):
    ''' Resets the portfolio as described in RF14, for Swap
        just for swap. It should sell the current values in
        the portfolio and reset the portfolio with the values
        in the new_portfolio_object.

        Args:
            new_portfolio_object: a hash map, indicating the
            composition of the new portfolio, whose ID should
            already exists in Swap.

            It's structure should be as in:

                {
                    'user_login' : value,
                    'risk' : value,
                    'pk_id' : value,
                    'values' : 
                        [
                            value1,
                            value2,
                            ...,
                            valuen
                        ]
                }

            The values 'user_login', 'risk', 'pk_id', should exists in
            the respective tables. And the value of values['pk_val'] 
            should exists in the values table.

        Returns:
            (bool, string) : a bool flag for the success of the process
                             a string message showing the associated
                             message and containing the confirmation
                             number. The structure of the message is:

                             <MESSAGE>:<NUMBER>:<STATE> 
    '''

    from django.db import connection

    portfolio_user = new_portfolio_object['user_login']
    portfolio_risk = new_portfolio_object['risk']
    portfolio_id = new_portfolio_object['pk_id']

    ans = [False, None]


    cursor = connection.cursor()
    query = '''SELECT * FROM PORTFOLIOS WHERE user_login = %s AND risk = %s AND pk_id = %s'''
    params = [portfolio_user, portfolio_risk, portfolio_id]
    cursor.execute(query, params)
    result_set = [_ for _ in cursor.fetchall()]
    if len(result_set) == 0:
        # Wrong parameters
        ans[1] = 'The given parameters are invalid for the transaction::imposible'
    else:
        # Parameters in table

        flag = True
        wrong_values = []

        # Sell
        sold = sell_values(portfolio_id)

        if not sold:
            ans[1] = 'Impossible to sell the values::imposible'

        else:
            # Buy: add to my portfolio
            for itm in new_portfolio_object['values']:

                bought = buy_value(pk_val, portfolio_id)

                if not bought:
                    wrong_values.append(pk_val)

                flag = flag and bought

            if not flag:
                ans[1] = 'The following values were not in the portfolio ' + str(portfolio_id) '. '

                for value in wrong_values:
                    ans[1] += str(value) + ', '

                ans[1] += '::pendiente por confirmar'

            else:
                ans[0] = flag
                ans[1] = 'Succesful transaction, the confirmation number is: '
                ans[1] += random_generator(10, ':0123456789')
                ans[1] += ':registrada'

    return tuple(ans)

def random_generator(size, seed):
    import random
    return ''.join(random.choice(seed) for _ in range(size))

def sell_value(portfolio_id):
    ''' Deletes all the values associated with the
        portfolio_id in the table PORTFOLIOS_VALS

        Args:
            portfolio_id: the id of the portfolio associated with
            the transaction

        Returns:
            (bool): a flag for show the failure of success of the
            transaction

    '''

    from django.db import connection

    ans = True

    cursor = connection.cursor()
    query = '''DELETE FORM PORTFOLIOS_VALS WHERE pk_portfolio = %s'''
    params = [portfolio_id]
    try:
        cursor.execute(query, params)
        ans = True
    except:
        ans = False    

    return ans

def buy_value(value_id, portfolio_id):
    ''' Adds the given value to the given portfolio
        with the association value as the given parameters

        Args:
            value_id: the id of the value, that should exists
            in the database

            portfolio_id: the id of the portfolio, should be in
            in the database

            association_id: the id of the association

        Returns:
            (bool): a flag for the success of the transaction

    '''

    from django.db import connection

    ans = True

    cursor = connection.cursor()
    query = '''INSERT INTO PORTFOLIOS_VALS VALUES(%s, %s, %s)'''
    params = [random_generator(20, '0123456789'), portfolio_id, value_id]

    try:
        cursor.execute(query, params)
        ans = True
    except:
        ans = False    

    return ans

def drop_intermediate(user_id):
    pass

def dynamic_values(date1, date2):
    ''' Get the more dynamic values in Swap in a given
        range of dates, that is the more frequent values
        in solicitudes in a given date.

        Args:
            date1: (string) a string representing the lower bound
            of the date. its format should 'yyyy-mm-dd'

            dates: (string) a string representing the upper bound
            of the date. The format is the same as above

        Returns:
            (list of Vals): list of value object representing each single
            element in the list, each item in the list is a dictionary
    '''

    from django.db import connection

    ans = []

    cursor = connection.cursor()
    query = ''' SELECT VALS.*
                FROM
                    VALS
                INNER JOIN
                    (SELECT rela.val, freq, solicitude 
                    FROM   
                        (
                            SELECT VAL, COUNT(VAL) AS FREQ 
                            FROM 
                                (
                                        SOLICITUDES_VAL 
                                    INNER JOIN 
                                        SOLICITUDES 
                                    ON SOLICITUDES.PK_ID = SOLICITUDES_VAL.SOLICITUDE
                                ) 
                            GROUP BY VAL
                            ORDER BY COUNT(VAL) DESC
                        ) rela
                    INNER JOIN
                        (
                            SELECT SOLICITUDE, VAL
                            FROM 
                                (
                                        SOLICITUDES_VAL 
                                    INNER JOIN 
                                        SOLICITUDES 
                                    ON SOLICITUDES.PK_ID = SOLICITUDES_VAL.SOLICITUDE
                                )
                            WHERE 
                                (
                                    CREATED_AT >= TO_TIMESTAMP(%s,'yyyy-mm-dd') 
                                    AND 
                                    CREATED_AT < TO_TIMESTAMP(%s,'yyyy-mm-dd')
                                )
                        ) relb
                    ON rela.val = relb.val
                    WHERE FREQ IN 
                        (
                            SELECT MAX(freq)
                            FROM
                            (
                                SELECT VAL, COUNT(VAL) AS FREQ 
                                FROM 
                                        (
                                                SOLICITUDES_VAL 
                                            INNER JOIN 
                                                SOLICITUDES 
                                            ON SOLICITUDES.PK_ID = SOLICITUDES_VAL.SOLICITUDE
                                        ) 
                                GROUP BY VAL
                                ORDER BY COUNT(VAL) DESC
                            )
                        )
                    ORDER BY freq DESC) infreq
                ON infreq.val = VALS.PK_ID
            '''

    params = [date1, date2]
    cursor.execute(query, params)

    result_set = [_ for _ in cursor.fetchall()]

    for itm in result_set:
        pk = itm[0]
        value_object = ValDao().find_by_id(pk)
        if value_object:
            ans.append(value_object)

    return ans

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

