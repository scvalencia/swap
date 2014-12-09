#!/usr/bin/env python
import pika
import random
import tasks.logic
import getpass
from portfolios.dao import PortfolioDao
from passives.dao import PassiveDao

u, p = 'scvalencia', 'admin'

PORT = 5672

local = True
queue_name = 'CF' if not local else 'SC'
connection = None

if not local:

	username = 'valencia'
	password = 'admin123'
	foreign_ip = '157.253.169.223' 

	credentials = pika.PlainCredentials(username, password)
	parameters = pika.ConnectionParameters(foreign_ip, PORT, '/', credentials)
	connection = pika.BlockingConnection(parameters)

else:

	print queue_name
	connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()
channel.queue_declare(queue=queue_name)

def send_message(body):
	channel.basic_publish(exchange='', routing_key=queue_name, body=body)

def send_R1(email, id_portfolio, values):

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
		message = 'Q1;' + email + ':' + str(id_portfolio) + ':'
		for value in values:
			message += random.choice(['0', '1', '2', '3'])
			message += str(value)
		send_message(message)
		return 'Sended'		

def send_R2(login):

	passive_object = PassiveDao().find_by_login(login)

	if len(passive_object) != 0:

		passive_object = PassiveDao().find_by_login(login)[0]
		register = passive_object.passive_register	
		return 'El nemail del reemplazo es: ' + tasks.logic.drop_intermediate(register)[-1]

	else:
		message = 'Q2;' + login
		send_message(message)
		return 'Sended'

def send_R3(name, rent, email, date1, date2):

	ans = tasks.logic.get_movement(name, rent, email, date1, date2)

	if ans == []:
		message = 'Q3;'
		message += name + ':' + rent + ':' + email + ':' + date1 + ':' + date2
		send_message(message)

	else:
		print ans

def send_R4(d1, d2):
	ans = tasks.logic.dynamic_values(d1, d2)
	message = 'Q4;' + d1 + ':' + d2
	send_message(message)


print 'Bienvenido al terminal de administracion de Swap, porfavor introduzca sus datos.'
user = raw_input('username: ')
password = getpass.getpass('Password: ')
if u == user and p == password:
	print 'Bienvenido Sebastian Valencia, que accion desea realizar?'

	while True:
		print '=' * 100
		message = '1. Recomponer portafolio.\n2. Retirar intermediario.\n3. Consultar movimiento.\n4. Consultar valores mas dinamicos.'
		print message
		value = raw_input(">> ")
		if value == '1':
			email = raw_input('Introduzca el email: ')
			id_portfolio = raw_input('Introduzca el ID: ')
			print 'Introduzca los valores.'
			values = []
			val = ''
			while val != '0':
				val = raw_input('ID valor: ')
				values.append(val)
			print send_R1(email, id_portfolio, values)

		if value == '2':
			email = raw_input('Introduzca el email: ')
			print send_R2(email)

		if value == '3':
			name = raw_input('Introduzca el nombre del valor: ')
			rent = raw_input('Introduzca la rentabilidad del valor: ')
			email = raw_input('Introduzca el email: ')
			fecha1 = raw_input('Introduzca la fecha 1 (yyyy-mm-dd): ')
			fecha2 = raw_input('Introduzca la fecha 2 (yyyy-mm-dd): ')
			print send_R3(name, rent, email, fecha1, fecha2)


		if value == '4':
			fecha1 = raw_input('Introduzca la fecha 1 (yyyy-mm-dd): ')
			fecha2 = raw_input('Introduzca la fecha 2 (yyyy-mm-dd): ')
			print send_R4(fecha1, fecha2)

		if value == '0':
			break

else:
	print 'Datos incorrectos'
	
connection.close()
