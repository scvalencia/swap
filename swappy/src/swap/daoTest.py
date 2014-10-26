from genericusers.models import GenericUserDump
from genericusers.dao import GenericUserDao
from genericusers.models import GenericUser
from django.db import connection
from termcolor import colored

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class GenericUserDaoTest(object):

	def __init__(self):
		self.g = GenericUserDao()
		self.rs = self.g.rs
		self.separator = 'yellow'
		self.passed = 0
		self.failed = 0

	def test_schema(self, fail = False):
		real_schema = None
		if not fail:
			real_schema = ('login', 'user_id', 'first_name', 
				'last_name', 'email', 'phone', 'user_pass')
		else:
			real_schema = ('uno')
		oracle = self.g.schema
		message = ''
		print colored("1. TEST SCHEMA", self.separator)
		print colored("=" * 100, self.separator)
		try:
			assert(real_schema == oracle)
			message = 'El esquema de la base de datos corresponde con el de Oracle'
			print "Real data: ", real_schema
			print "Desired data: ", oracle 
			print colored(message, 'green')
			self.passed += 1
		except Exception as e:
			message = "Los esquemas no coinciden"
			print "Real data: ", real_schema
			print "Desired data: ", oracle  
			print colored(message, 'red')
			self.failed += 1
		print colored("=" * 100, self.separator)

	def test_name(self, fail = False):
		real_name = None
		if not fail:
			real_name = 'users'
		else:
			real_name = 'uno'
		oracle = self.g.table_name
		message = ''
		print colored("2. TEST NAME", self.separator)
		print colored("=" * 100, self.separator)
		try:
			assert(real_name == oracle)
			message = 'El nombre de la base de datos corresponde con el de Oracle'
			print "Real data: ", real_name
			print "Desired data: ", oracle 
			print colored(message, 'green')
			self.passed += 1
		except Exception as e:
			message = "Los nombres no coinciden"
			print "Real data: ", real_name
			print "Desired data: ", oracle  
			print colored(message, 'red')
			self.failed += 1
		print colored("=" * 100, self.separator)

	def test_cursor(self, fail = False):
		real_cursor = None
		if not fail:
			real_cursor = '1' is not None
		else:
			real_cursor = '1' is None
		oracle = self.g.cursor is not None
		message = ''
		print colored("3. TEST CURSOR", self.separator)
		print colored("=" * 100, self.separator)
		try:
			assert((oracle is not None) == real_cursor)
			message = 'El cursor no esta vacio'
			print "Real data: ", real_cursor
			print "Desired data: ", oracle 
			print colored(message, 'green')
			self.passed += 1
		except Exception as e:
			message = "El cursor a la base de datos se encuentra vacio"
			print "Real data: ", real_cursor
			print "Desired data: ", oracle  
			print colored(message, 'red')
			self.failed += 1
		print colored("=" * 100, self.separator)

	def test_find_all(self, fail = False):
		real_collection = []
		if not fail:
			cursor = connection.cursor()
			query = "SELECT * FROM users ORDER BY login"
			cursor.execute(query)
			collection = [itm for itm in cursor.fetchall()]
			for itm in collection:
				real_collection.append(self.g.process_row(itm))
		else:
			real_collection = [i for i in range(80)]
		oracle = self.g.find_all()
		message = ''
		print colored("4. TEST FETCH ALL", self.separator)
		print colored("=" * 100, self.separator)
		
		try:
			flag = 	True
			for i in range(len(oracle)):
				if oracle[i].user_id != real_collection[i].user_id:
					flag = False
					break
			assert(flag)
			message = 'Las colecciones de objetos coinciden en contenido (no en id)'
			print "Real data: ", real_collection
			print "Desired data: ", oracle 
			print colored(message, 'green')
			self.passed += 1
		except Exception as e:
			message = "Los conjuntos de resultados no coinciden"
			print "Real data: ", real_collection
			print "Desired data: ", oracle  
			print colored(message, 'red')
			self.failed += 1
		print colored("=" * 100, self.separator)
		connection.close()

	def test_find_by_login1(self, fail = False):
		self.g = GenericUserDao()
		real_collection = []
		if not fail:
			cursor = connection.cursor()
			query = "SELECT * FROM users WHERE login = %s"
			params = ['scvalencia']
			cursor.execute(query, params)
			collection = [itm for itm in cursor.fetchall()]
			for itm in collection:
				real_collection.append(self.g.process_row(itm))
		else:
			real_collection = [i for i in range(80)]
		oracle = self.g.find_by_login('scvalencia')
		message = ''
		print colored("5. TEST FINB BY ID1", self.separator)
		print colored("=" * 100, self.separator)
		
		try:
			flag = 	len(real_collection) == len(oracle)
			for i in range(len(oracle)):
				if oracle[i].user_id != real_collection[i].user_id:
					flag = flag or False
					break
			assert(flag)
			message = 'Las colecciones de objetos coinciden (por ID)'
			print "Real data: ", real_collection
			print "Desired data: ", oracle 
			print colored(message, 'green')
			self.passed += 1
		except Exception as e:
			message = "Los conjuntos de resultados no coinciden (por ID)"
			print "Real data: ", real_collection
			print "Desired data: ", oracle  
			print colored(message, 'red')
			self.failed += 1
		print colored("=" * 100, self.separator)
		connection.close()

	def test_find_by_login2(self, fail = False):
		self.g = GenericUserDao()
		real_collection = []
		if not fail:
			cursor = connection.cursor()
			query = "SELECT * FROM users WHERE login = %s"
			params = ['scvalenci']
			cursor.execute(query, params)
			collection = [itm for itm in cursor.fetchall()]
			for itm in collection:
				real_collection.append(self.g.process_row(itm))
		else:
			real_collection = [i for i in range(80)]
		oracle = self.g.find_by_login('scvalencia')
		message = ''
		print colored("6. TEST FINB BY ID2", self.separator)
		print colored("=" * 100, self.separator)		
		try:
			flag = 	(len(real_collection) != len(oracle))
			assert(flag)
			message = 'Las colecciones de objetos no coinciden (por ID)'
			print "Real data: ", real_collection
			print "Desired data: ", oracle 
			print colored(message, 'green')
			self.passed += 1
		except Exception as e:
			message = "Los conjuntos de resultados no deben coincidir (por ID)"
			print "Real data: ", real_collection
			print "Desired data: ", oracle  
			print colored(message, 'red')
			self.failed += 1
		print colored("=" * 100, self.separator)
		connection.close()

	def test_remove(self, fail = False):
		self.g = GenericUserDao()
		real_collection = []
		print colored("6. TEST REMOVE", self.separator)
		print colored("=" * 100, self.separator)
		if not fail:
			try:
				cursor = connection.cursor()
				login = 'julieta'
				user_id = '432'
				user_pass = 'qazwsxedcrfv'
				first_name = 'Julieta'
				last_name = 'Avendanio'
				email = 'je.avendano@gm.com'
				phone = '7647'
				self.g.remove(login)
				query = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s)"
				params = [login, user_id, first_name, last_name, email, phone, user_pass]
				cursor.execute(query, params)
				query = "SELECT * FROM users WHERE login = %s"
				params = [login]
				cursor.execute(query, params)
				collection = [itm for itm in cursor.fetchall()]
				for itm in collection: real_collection.append(self.g.process_row(itm))
				assert(len(real_collection) == 1)
				self.g.remove(login)
				juliettes = self.g.find_by_login(login)
				assert(len(juliettes) == 0)
				message = 'El usuario fue creado y removido exitosamente'
				print colored(message, 'green')
				self.passed += 1

			except Exception as e:
				message = "El usuario no fue removido correctamente"  
				print colored(message, 'red')
				self.failed += 1

		print colored("=" * 100, self.separator)
		connection.close()

	def test_insert(self, fail = False):
		self.g = GenericUserDao()
		real_collection = []
		print colored("7. TEST INSERT", self.separator)
		print colored("=" * 100, self.separator)
		if not fail:
			try:
				cursor = connection.cursor()
				login = 'juliette'
				user_id = '432'
				user_pass = 'qazws'
				first_name = 'Jul'
				last_name = 'Aven'
				email = 'je.avend'
				phone = '7647'
				query = "DELETE FROM users WHERE login = %s"
				params = [login]
				cursor.execute(query, params)
				try:
					self.g = GenericUserDao()
					self.g.remove(login)
					self.g.insert(login, user_id, user_pass, first_name, 
						last_name, email, phone)
					real_collection = self.g.find_by_login(login)
				except Exception as e:
					print e
				assert(len(real_collection) == 1)
				self.g.remove(login)
				message = 'El usuario fue creado y removido exitosamente'
				print colored(message, 'green')
				self.passed += 1

			except Exception as e:
				message = "El usuario no fue insertado correctamente"  
				print colored(message, 'red')
				self.failed += 1

		print colored("=" * 100, self.separator)
		connection.close()

	def test_update(self, fail = False):
		self.g = GenericUserDao()
		real_collection = []
		print colored("8. TEST UPDATE", self.separator)
		print colored("=" * 100, self.separator)
		if not fail:
			try:
				cursor = connection.cursor()
				login = 'fabian'
				user_id = '432'
				user_pass = 'qazwsxedcrfv'
				first_name = 'Julieta'
				last_name = 'Avendanio'
				email = 'je.avendano@gm.com'
				phone = '7647'
				self.g.remove(login)
				try:
					query = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s)"
					params = [login, user_id, first_name, last_name, email, phone, user_pass]
					cursor.execute(query, params)
				except Exception as e:
					print e
				real_collection = self.g.process_object(self.g.find_by_login(login)[0])
				user_id = '433'
				user_object = GenericUserDump(login, user_id, user_pass, 
					first_name, last_name, email, phone)
				self.g.update(user_object)
				collection = self.g.process_object(self.g.find_by_login(login)[0])
				flag = real_collection.user_id != collection.user_id
				flag = flag and real_collection.login == collection.login
				assert(flag)
				self.g.remove(login)
				message = 'El usuario fue creado y actualizado exitosamente'
				print colored(message, 'green')
				self.passed += 1

			except Exception as e:
				message = "El usuario no fue actualizado correctamente"  
				print colored(message, 'red')
				self.failed += 1

		print colored("=" * 100, self.separator)
		connection.close()

def main_slave_homebrew():
	tester = GenericUserDaoTest()
	print colored("=" * 100, tester.separator)
	tester.test_schema()
	tester.test_name()
	tester.test_cursor()
	tester.test_find_all()
	tester.test_find_by_login1()
	tester.test_find_by_login2()
	tester.test_remove()
	tester.test_insert()
	tester.test_update()
	print_report(tester.passed, tester.failed)

def print_report(passed, failed):
	print colored('_' * 100, 'yellow')
	total = passed + failed
	percentage_passed = (passed * 100.0) / total
	percentage_failed = (failed * 100.0) / total
	print colored('Succesful test cases ' + str(percentage_passed) + ' %', 'green')
	print colored('Failed test cases ' + str(percentage_failed) + ' %', 'red')
	print colored('_' * 100, 'yellow')

def main():
	main_slave_homebrew()
	connection.close()
main()