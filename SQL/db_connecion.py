# http://iambusychangingtheworld.blogspot.com/2014/07/install-cxoracle-513-in-ubuntu-1404.html
# http://kevindalias.com/2014/03/26/how-to-set-up-cx_oracle-for-python-on-mac-os-x-10-89/

import cx_Oracle
import getpass
import sys
import os

server = 'prod.oracle.virtual.uniandes.edu.co'
port = '1531'
SID = 'prod'
allowed_users = ('ISIS2304361420', 'ISIS2304031420') # Me: 361420, JC: 031420
names = {'ISIS2304361420' : 'Sebastian', 'ISIS2304031420' : 'Juan Camilo'}
passwords = {'ISIS2304361420' : 'entrambac1ddf', 'ISIS2304031420' : 'ciertib4789'}
valid_connection = False
production = False # To activate commit

class User(object):
	def __init__(self, username, password, port, sid):
		self.username = username
		self.password = password
		self.port = port
		self.sid = sid

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

def execute_file(cursor, filename):
	if not os.path.isfile(filename):
		print 'Not an SQL file'
		return 
	if filename[-3:].lower() == 'sql' and cursor:
		sql_file = open(filename, 'r')
		full_sql = sql_file.read()
		sql_commands = full_sql.split(';')
		for command in sql_commands:
			print
			print '\033[93m' + command + '\033[0m'
			print '\033[93m' + ('*' * 34) + '\033[0m'
			try:
				cursor.execute(command)
				rows = cursor.fetchall()
				if len(rows) > 0:
					for row in rows:
						print
						print row
						print
			except Exception, e:
				continue
	else:
		print 'Not an SQL file'

def main():
	global production
	if(len(sys.argv) == 3):
		code = sys.argv[1]
		production_flag = sys.argv[2]
		if production_flag.lower() == 't': # Commit?
			production = True 	
		main_user = set_user(code)
		if main_user:
			dsn_tns = cx_Oracle.makedsn(server, port, SID)
			connection = None
			try:
				connection = cx_Oracle.connect(main_user.username, main_user.password, dsn_tns)
				try:
					cursor = connection.cursor()
					filename = raw_input("Filename, (including sql extension): ")
					execute_file(cursor, filename)					
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

# TODO: DB Migration
# TODO: DB Backup