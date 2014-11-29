from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import transaction, connection
from django.views.generic import View

from genericusers.dao import GenericUserDao
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
import json
import random

import timeTracker

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

        MQ:
            email_activo1
            email_passive1
            email_activo2
            email_activo2
            nombre_valor
            nit_valor
            riesgo
            cantidad
            precio 
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
        sold = sell_value(portfolio_id)

        if not sold:
            ans[1] = 'Impossible to sell the values::imposible'

        else:
            # Buy: add to my portfolio
            for pk_val in new_portfolio_object['values']:

                bought = buy_value(pk_val, portfolio_id)

                if not bought:
                    wrong_values.append(pk_val)

                flag = flag and bought

            if not flag:
                ans[1] = 'The following values were not in the portfolio ' + str(portfolio_id) + '. '

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
    query = '''DELETE FROM PORTFOLIOS_VALS WHERE pk_portfolio = %s'''
    params = [portfolio_id]
    try:
        cursor.execute(query, params)
        ans = True
    except Exception, err:
        print traceback.format_exc()
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
    ''' Removes a passive user from the Swap,
        the remotion proceeds as follows:

            1.  Find for a lazy passive, that is
                a passive that has minimum work at present
            2.  Assigns to all the actives under the passive
                whose user id is user_id the found lazy passive
            3.  Remove the passive from the system

        Args:
            user_id: the id of the passive to be removed

        Returns:
            (bool, string): the email of the replacement

    '''
    # Seleccionar pasivo menos solicitado
    # Asignar a todos los activos de este pasivo (el dado)
    # el nuevo hallado. Borrar dado de pasiives, users

    from django.db import connection
    import random

    cursor = connection.cursor()

    query = ''' SELECT USER_LOGIN, A.PASSIVE_REGISTER
                FROM 
                    PASSIVES INNER JOIN
                                (
                                    SELECT PASSIVE_REGISTER, COUNT(PASSIVE_REGISTER) AS FREQ
                                    FROM ACTIVESPASSIVES
                                    GROUP BY PASSIVE_REGISTER
                                ) 
                    A
                    ON A.PASSIVE_REGISTER = PASSIVES.PASSIVE_REGISTER
                WHERE FREQ IN 
                    (
                        SELECT MIN(FREQ) 
                        FROM 
                            (
                                SELECT PASSIVE_REGISTER, COUNT(PASSIVE_REGISTER) AS FREQ
                                FROM ACTIVESPASSIVES
                                GROUP BY PASSIVE_REGISTER
                            )
                    )
                AND A.PASSIVE_REGISTER <> %s
            '''

    params = [user_id]
    cursor.execute(query, params)
    result_set = [_ for _ in cursor.fetchall()]

    new_passive = random.choice(result_set)

    new_passive_login = new_passive[0]
    new_passive_register = new_passive[1]

    query = ''' UPDATE ACTIVESPASSIVES
                SET PASSIVE_REGISTER = %s
                WHERE PASSIVE_REGISTER = %s
            '''

    params = [new_passive_register, user_id]

    cursor = connection.cursor()

    cursor.execute(query, params)

    query = '''DELETE FROM PASSIVES WHERE PASSIVE_REGISTER = %s'''
    params = [user_id]

    cursor = connection.cursor()

    cursor.execute(query, params)

    return (True, new_passive_login + '@swap.in')

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

    return [itm.__dict__ for itm in ans]