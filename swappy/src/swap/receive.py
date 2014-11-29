#!/usr/bin/env python
import pika
import random
import tasks.logic
from portfolios.dao import PortfolioDao
from passives.dao import PassiveDao

queue_name = 'SC'

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()
channel.queue_declare(queue=queue_name)

QUESTION = 1
ANSWER = 2

def callback(ch, method, properties, body):

	if len(body) > 3:

		if ';' in body:

			parse = body.split(';')
			
			head = parse[0]
			args = parse[1]

			kind, number = None, '0'

			if head[0] == 'Q':
				kind = QUESTION
				number = head[1]

			elif head[0] == 'R':
				kind = ANSWER
				number = head[1]

			print process_query(kind, number, args)

def process_query(kind, number, args):
	number = int(number)

	if kind == QUESTION:
		if number == 1:

			args = [_ for _ in args.split(':')]

			email = args[0]
			id_portfolio = args[1]
			values = args[2]

			return process_Q1(email, id_portfolio, values)

		elif number == 2:

			if '@' in args:

				arroba = args.index('@')
				login = args[:arroba]
				return process_Q2(login)

		elif number == 3:
			return 'QUESTION 3'
		elif number == 4:
			return 'QUESTION 4'

	elif kind == ANSWER:
		if number == 1:
			return 'ANSWER 1'
		elif number == 2:
			return 'ANSWER 2'
		elif number == 3:
			return 'ANSWER 3'
		elif number == 4:
			return 'ANSWER 4'

def process_Q1(email, id_portfolio, args):

	ans = {'user_login' : None, 'risk' : None, 'pk_id' : None, 'values' : []}

	portfolio_object = PortfolioDao().find_by_id(id_portfolio)

	if len(portfolio_object) != 0:

		portfolio_object = PortfolioDao().find_by_id(id_portfolio)[0]

		ans['pk_id'] = portfolio_object.pk_id
		ans['user_login'] = portfolio_object.user_login
		ans['risk'] = portfolio_object.risk

		values = [_.split(',')[1] for _ in args.split('|')]

		for value in values:
			ans['values'].append(int(value))

		return tasks.logic.reset_portfolio(ans)

	else:
		return 'The given portfolio is not on Swap'

def process_Q2(login):

	passive_object = PassiveDao().find_by_login(login)

	if len(passive_object) != 0:

		passive_object = PassiveDao().find_by_login(login)[0]
		register = passive_object.passive_register	
		return tasks.logic.drop_intermediate(register)

	else:
		return 'There is not a passive user with such email'


while True:
	channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()

