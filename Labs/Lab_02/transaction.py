import cx_Oracle
import sys
import os

server = 'prod.oracle.virtual.uniandes.edu.co'
port = '1531'
SID = 'prod'
allowed_users = ('ISIS2304361420', 'ISIS2304031420')
passwords = {'ISIS2304361420' : 'entrambac1ddf', 'ISIS2304031420' : 'ciertib4789'}
production = False # To activate commit
valid_connection = False

class Reserva(object):
	def __init__(self, id_reserva, id_funcion, id_cliente, fecha, estado):
		self.id_reserva = id_reserva  
		self.id_funcion = id_funcion
		self.id_cliente = id_cliente
		self.fecha = fecha
		self.estado = estado

class SillasReservas(object):
	def __init__(self, id_silla, id_funcion, id_reserva):
		self.id_silla = id_silla
		self.id_funcion = id_funcion 
		self.id_reserva = id_reserva

class User(object):
	def __init__(self, username, password, port, sid):
		self.username = username
		self.password = password
		self.port = port
		self.sid = sid

def make_transaction(cursor, id_reserva, id_cliente, id_funcion, id_silla1, id_silla2):
	sillas = [id_silla1, id_silla2]
	estado = 'REV'
	fecha = 'CURRENT_DATE'
	query_insertion = "INSERT INTO Reservas VALUES (%s, %s, %s, %s, %s)"
	params = [id_reserva, id_funcion, id_cliente, fecha, estado]
	cursor.execute(query_insertion, params)
	for silla in sillas:
		query_chair = "INSERT INTO SillasReserva VALUES (%s, %s, %s)"
		params[silla, id_funcion, id_reserva]
		cursor.execute(query_chair, params)

def set_user(code):
	postfix = '1420'
	global valid_connection
	main_user = None
	if code == '36':
		username = allowed_users[0]
		password = passwords[username]
		main_user = User(username, password, port, SID)
		valid_connection = True
	elif code == '03':
		username = allowed_users[1]
		password = passwords[username]
		main_user = User(username, password, port, SID)
		valid_connection = True
	return main_user

def main():
	global production
	transact = True
	if(len(sys.argv) == 2):
		code = sys.argv[1]
		production = True 	
		main_user = set_user(code)
		if main_user:
			dsn_tns = cx_Oracle.makedsn(server, port, SID)
			connection = None
			try:
				connection = cx_Oracle.connect(main_user.username, main_user.password, dsn_tns)
				try:
					cursor = connection.cursor()
					if transact:
						make_transaction(cursor, 1, 2, 3, 1, 4)
					else:
						
						query = "SELECT * FROM Reservas"
						params = []
						if params == []:
							cursor.execute(query)
						else:
							cursor.execute(query, params)
						result_set = [i for i in cursor.fetchall()]
						if result_set == []:
							print 'Empty relation'
						else:
							print 'Result'
							for i in result_set: print i					
				finally:
					cursor.close()
			finally:
				if connection is not None:
					if production:
						connection.commit()
					connection.close()		
		else:
			print 'Wrong code.'
	else:
		print 'Wrong usage.'

if __name__ == '__main__':
	main()