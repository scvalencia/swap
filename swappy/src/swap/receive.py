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

local = True
foreign_ip = '157.253.169.223'

def callback(ch, method, properties, body):

	print body

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

			process_query(kind, number, args)

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

			print 'scfgdfgf'

			if '@' in args:

				arroba = args.index('@')
				login = args[:arroba]
				return process_Q2(login)

			else:

				return process_Q2(args)


		elif number == 3:
			
			parse = [_ for _ in args.split(':')]
			return process_Q3(parse[0], parse[1], parse[2], parse[3], parse[4])
		elif number == 4:
			parse = [_ for _ in args.split(':')]
			return process_Q4(parse[0], parse[1])

	elif kind == ANSWER:

		if number == 1:

			args = [_ for _ in args.split(',')]
			flag = args[0]
			register = args[1]
			print 'Respuesta: ' + flag
			print 'No Registro: ' + register 

		elif number == 2:

			print 'Correo nuevo intermediario: ' + args

		elif number == 3:

			values = [_ for _ in args.split('|')]
			for itm in values:
				parse = itm.split(',')
				print 'Id_valor: ' + parse[1]

		elif number == 4:

			values = [_ for _ in args.split('|')]
			for itm in values:
				parse = itm.split(',')
				print 'Id_valor: ' + parse[1]

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

		message = tasks.logic.reset_portfolio(ans)

		flag = message[0]
		message = message[1]

		if flag:

			PORT = 5672

			queue_name = 'CF' if not local else 'SC'
			connection = None

			if not local:

				username = 'valencia'
				password = 'admin123'
				 

				credentials = pika.PlainCredentials(username, password)
				parameters = pika.ConnectionParameters(foreign_ip, PORT, '/', credentials)
				connection = pika.BlockingConnection(parameters)

			else:

				connection = pika.BlockingConnection(pika.ConnectionParameters(
			        host='localhost'))

			channel = connection.channel()
			channel.queue_declare(queue=queue_name)

			def send_message(body):
				channel.basic_publish(exchange='', routing_key=queue_name, body=body)


			meg = 'R1;' + str(flag) + ',' + str(random.randint(0, 2342524))
			print meg
			send_message(meg)

			connection.close()


		else:
			return 'Error'


	else:
		return 'The given portfolio is not on Swap'

def process_Q2(login):
	print 'dsfgf'

	passive_object = PassiveDao().find_by_login(login)

	if len(passive_object) != 0:

		passive_object = PassiveDao().find_by_login(login)[0]
		register = passive_object.passive_register

		message = tasks.logic.drop_intermediate(register)

		flag = message[0]
		message = message[1]

		if flag:
			
			PORT = 5672

			queue_name = 'CF' if not local else 'SC'
			connection = None

			if not local:

				username = 'valencia'
				password = 'admin123' 

				credentials = pika.PlainCredentials(username, password)
				parameters = pika.ConnectionParameters(foreign_ip, PORT, '/', credentials)
				connection = pika.BlockingConnection(parameters)

			else:

				connection = pika.BlockingConnection(pika.ConnectionParameters(
			        host='localhost'))

			channel = connection.channel()
			channel.queue_declare(queue=queue_name)

			def send_message(body):
				channel.basic_publish(exchange='', routing_key=queue_name, body=body)


			meg = 'R2;' + message
			print meg
			send_message(meg)
			print meg

			connection.close()

		else:
			return 'ERROR'


	else:
		return 'There is not a passive user with such email'

def process_Q3(val_name, rent_type, email, date1, date2):

	ans = []
	ans += tasks.logic.get_movement(val_name, rent_type, email, date1, date2)
	flag = len(ans) != 0
	if True:
		if flag:
			
			PORT = 5672

			queue_name = 'CF' if not local else 'SC'
			connection = None

			if not local:

				username = 'valencia'
				password = 'admin123' 

				credentials = pika.PlainCredentials(username, password)
				parameters = pika.ConnectionParameters(foreign_ip, PORT, '/', credentials)
				connection = pika.BlockingConnection(parameters)

			else:

				connection = pika.BlockingConnection(pika.ConnectionParameters(
			        host='localhost'))

			channel = connection.channel()
			channel.queue_declare(queue=queue_name)

			def send_message(body):
				channel.basic_publish(exchange='', routing_key=queue_name, body=body)


			meg = 'R3;'
			
			i = 0
			for itm in values:
				meg += str(itm[-1]) + ',' + str(itm[0])
				if i == (len(values) - 1):
					pass
				else:
					meg += '|'

			meg = meg[:-1]
			print meg
			send_message(meg)
			connection.close()

		else:
			
			PORT = 5672

			queue_name = 'CF' if not local else 'SC'
			connection = None

			if not local:

				username = 'valencia'
				password = 'admin123'

				credentials = pika.PlainCredentials(username, password)
				parameters = pika.ConnectionParameters(foreign_ip, PORT, '/', credentials)
				connection = pika.BlockingConnection(parameters)

			else:

				connection = pika.BlockingConnection(pika.ConnectionParameters(
			        host='localhost'))

			channel = connection.channel()
			channel.queue_declare(queue=queue_name)

			def send_message(body):
				channel.basic_publish(exchange='', routing_key=queue_name, body=body)


			meg = 'R3;'
			
			i = 0
			for itm in ans:
				meg += str(itm[-1]) + ',' + str(itm[0])
				if i == (len(values) - 1):
					pass
				else:
					meg += '|'

			meg = meg[:-1]
			send_message(meg)
			connection.close()

def process_Q4(date1, date2):
	values = tasks.logic.dynamic_values(date1, date2)
	flag = len(values) != 0
	if True:
		if flag:
			
			PORT = 5672

			queue_name = 'CF' if not local else 'SC'
			connection = None

			if not local:

				username = 'valencia'
				password = 'admin123'

				credentials = pika.PlainCredentials(username, password)
				parameters = pika.ConnectionParameters(foreign_ip, PORT, '/', credentials)
				connection = pika.BlockingConnection(parameters)

			else:

				connection = pika.BlockingConnection(pika.ConnectionParameters(
			        host='localhost'))

			channel = connection.channel()
			channel.queue_declare(queue=queue_name)

			def send_message(body):
				channel.basic_publish(exchange='', routing_key=queue_name, body=body)


			meg = 'R4;'
			
			i = 0
			for itm in values:
				meg += str(itm[-1]) + ',' + str(itm[0])
				if i == (len(values) - 1):
					pass
				else:
					meg += '|'

			meg = meg[:-1]
			print meg
			send_message(meg)
			connection.close()

		else:
			return 'ERROR'


while True:
	channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()

