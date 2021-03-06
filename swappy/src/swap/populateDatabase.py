from genericusers.dao import GenericUserDao
from genericusers.dao import LegalDao
from genericusers.models import GenericUser
from genericusers.models import Legal

from actives.dao import ActiveDao
from actives.models import Active

from passives.dao import PassiveDao
from passives.dao import ActivePassiveDao
from passives.models import ActivePassive
from passives.models import Passive
from passives.models import ActivePassive

from investors.dao import InvestorDao
from investors.models import Investor

from portfolios.dao import PortfolioDao
from portfolios.models import Portfolio
from portfolios.models import PortfolioVal

from offerants.dao import OfferantDao
from offerants.models import Offerant

from vals.dao import RentDao
from vals.dao import ValDao
from vals.models import Rent
from vals.models import Val

from solicitudes.dao import SolicitudeDao
from solicitudes.models import Solicitude

from swaptransactions.dao import SwapTransactionDao
from swaptransactions.models import SwapTransaction

from termcolor import colored
from tabulate import tabulate
import string
import random

class UsersPopulator(object):

	FIRST_NAMES = 'first.txt'
	LAST_NAMES = 'last.txt'
	APELLIDOS = 'apellidos.txt'

	def __init__(self, debugging, bound, printer):
		self.last_names_index = {}
		self.first_names_index = {}
		self.numbers = '1234567890'
		self.insertor = GenericUserDao()
		self.built_names_index()
		self.debugging = debugging
		self.printer = printer
		self.bound = bound
		self.passed = 0
		self.failed = 0

	def built_names_index(self):

		file_object_names = open(self.FIRST_NAMES)
		file_object_surnames = open(self.LAST_NAMES)

		for line in file_object_names:
			line = line.strip()
			if line[0] not in self.first_names_index:
				self.first_names_index[line[0]] = [line.encode('utf-8')]
			else:
				self.first_names_index[line[0]].append(line.encode('utf-8'))

		for line in file_object_surnames:
			line = line.strip()
			if line[0] not in self.last_names_index:
				self.last_names_index[line[0]] = [line.encode('utf-8')]
			else:
				self.last_names_index[line[0]].append(line.encode('utf-8'))

	def generator(self, seed, size):
		return ''.join(random.choice(seed) for _ in range(size))

	def generate_login(self, name, last_name):
		ans = ''
		ans += name[0] + name[1]
		ans += self.generator(last_name, 4)
		return ans

	def generate_email(self, login):
		return login + '@swap.in'

	def generate_pass(self):
		seed = string.ascii_uppercase + string.digits
		return self.generator(seed, 6)

	def populate(self):
		first_names_vals = self.first_names_index.values()
		last_names_vals = self.last_names_index.values()
		first_names = []
		last_names = []
		for itm in first_names_vals:
			for i in itm:
				first_names.append(i)

		for itm in last_names_vals:
			for i in itm:
				last_names.append(i)

		i = 0
		while i < self.bound:
			first = random.choice(first_names).encode('utf-8')
			last = random.choice(last_names).encode('utf-8')
			login = self.generate_login(first, last).encode('utf-8')
			first = first.capitalize()
			first_name = ''.join(first.split())
			user_id = self.generator('1234567890', 10)
			email = self.generate_email(login).encode('utf-8')
			phone = self.generator('1234567890', 7)
			password = self.generate_pass()
			addion_tuple = first, last, login, user_id, email, phone, password
			self.insertor = GenericUserDao()
			response = self.insertor.insert(login, user_id, password, first, last, email, phone)
			if self.debugging:
				if response:
					if self.printer:
						print addion_tuple, colored(response, 'green')
					self.passed += 1
				else:
					if self.printer:
						print addion_tuple, colored(response, 'red')
					self.failed += 1
				i += 1


	def __str__(self):
		ans = ''		
		ans += colored('Passed: ' + str(self.passed), 'green')
		ans += ' '
		ans += colored('Failed: ' + str(self.failed), 'red')
		return ans

class ActivesPopulator(object):

	def __init__(self, debugging, bound, printer):
		self.logins = [itm.login for itm in GenericUser.objects.all()]
		self.numbers = '1234567890'
		self.insertor = ActiveDao()
		self.debugging = debugging
		self.printer = printer
		self.bound = bound
		self.passed = 0
		self.failed = 0

	def generator(self, seed, size):
		return ''.join(random.choice(seed) for _ in range(size))

	def populate(self):
		i = 0
		while i < self.bound:
			login = random.choice(self.logins).encode('utf-8')
			money = random.uniform(1000.0, 24000.0)
			addion_tuple = login, money
			self.insertor = ActiveDao()
			response = self.insertor.insert(login, money)
			if self.debugging:
				if response:
					if self.printer:
						print addion_tuple, colored(response, 'green')
					self.passed += 1
				else:
					if self.printer:
						print addion_tuple, colored(response, 'red')
					self.failed += 1
				i += 1
			

	def __str__(self):
		ans = ''
		ans += colored('Passed: ' + str(self.passed), 'green')
		ans += ' '
		ans += colored('Failed: ' + str(self.failed), 'red')
		return ans

class PassivesPopulator(object):

	def __init__(self, debugging, bound, printer):
		self.logins = [itm.login for itm in GenericUser.objects.all()]
		self.numbers = '1234567890'
		self.insertor = PassiveDao()
		self.debugging = debugging
		self.printer = printer
		self.bound = bound
		self.passed = 0
		self.failed = 0

	def generator(self, seed, size):
		return ''.join(random.choice(seed) for _ in range(size))

	def populate(self):
		i = 0
		while i < self.bound:
			login = random.choice(self.logins).encode('utf-8')
			register = self.generator(self.numbers, 5)
			addion_tuple = login, register
			self.insertor = PassiveDao()
			response = self.insertor.insert(register, login)
			if self.debugging:
				if response:
					if self.printer:
						print addion_tuple, colored(response, 'green')
					self.passed += 1
				else:
					if self.printer:
						print addion_tuple, colored(response, 'red')
					self.failed += 1
				i += 1

			

	def __str__(self):
		ans = ''
		ans += colored('Passed: ' + str(self.passed), 'green')
		ans += ' '
		ans += colored('Failed: ' + str(self.failed), 'red')
		return ans

class InvestorPopulator(object):

	def __init__(self, debugging, bound, printer):
		self.logins = [itm.user_login.login for itm in Active.objects.all()]
		self.is_enterprise = ['0', '1']
		self.insertor = InvestorDao()
		self.debugging = debugging
		self.printer = printer
		self.bound = bound
		self.passed = 0
		self.failed = 0

	def populate(self):
		i = 0
		while i < self.bound:
			login = random.choice(self.logins).encode('utf-8')
			is_enterprise = random.choice(self.is_enterprise)
			addion_tuple = login, is_enterprise
			self.insertor = InvestorDao()
			response = self.insertor.insert(login, is_enterprise)
			if self.debugging:
				if response:
					if self.printer:
						print addion_tuple, colored(response, 'green')
					self.passed += 1
				else:
					if self.printer:
						print addion_tuple, colored(response, 'red')
					self.failed += 1
				i += 1

			

	def __str__(self):
		ans = ''
		ans += colored('Passed: ' + str(self.passed), 'green')
		ans += ' '
		ans += colored('Failed: ' + str(self.failed), 'red')
		return ans

class LegalPopulator(object):

	def __init__(self, debugging, bound, printer):
		self.logins = [itm.user_login.login for itm in Active.objects.all()]
		self.names = [itm.first_name for itm in GenericUser.objects.all()]
		self.numbers = '0123456789'
		self.insertor = LegalDao()
		self.debugging = debugging
		self.printer = printer
		self.bound = bound
		self.passed = 0
		self.failed = 0

	def generator(self, seed, size):
		return ''.join(random.choice(seed) for _ in range(size))

	def populate(self):
		i = 0
		while i < self.bound:
			legal_id = self.generator(self.numbers, 15)
			name = random.choice(self.names).encode('utf-8')
			login = random.choice(self.logins).encode('utf-8')
			addion_tuple = legal_id, name, login
			self.insertor = LegalDao()
			response = self.insertor.insert(legal_id, name, login)
			if self.debugging:
				if response:
					if self.printer:
						print addion_tuple, colored(response, 'green')
					self.passed += 1
				else:
					if self.printer:
						print addion_tuple, colored(response, 'red')
					self.failed += 1
				i += 1

			

	def __str__(self):
		ans = ''
		ans += colored('Passed: ' + str(self.passed), 'green')
		ans += ' '
		ans += colored('Failed: ' + str(self.failed), 'red')
		return ans

class ActivesPassivesPopulator(object):

	def __init__(self, debugging, bound, printer):
		self.logins = [itm.user_login.login for itm in Active.objects.all()]
		self.registers = [itm.passive_register for itm in Passive.objects.all()]
		self.debugging = debugging
		self.printer = printer
		self.bound = bound
		self.inserter = ActivePassiveDao()
		self.passed = 0
		self.failed = 0

	def populate(self):
		i = 0
		while i < self.bound:
			login = random.choice(self.logins).encode('utf-8')
			register = random.choice(self.registers)
			addion_tuple = login, register
			self.inserter = ActivePassiveDao()			
			response = self.inserter.insert(register, login)
			if self.debugging:
				if response:
					if self.printer:
						print addion_tuple, colored(response, 'green')
					self.passed += 1
				else:
					if self.printer:
						print addion_tuple, colored(response, 'red')
					self.failed += 1
				i += 1
			

	def __str__(self):
		ans = ''
		ans += colored('Passed: ' + str(self.passed), 'green')
		ans += ' '
		ans += colored('Failed: ' + str(self.failed), 'red')
		return ans

class PortfolioPopulator(object):

	def __init__(self, debugging, bound, printer):
		self.logins = [itm.login for itm in GenericUser.objects.all()]
		self.risks = ['L', 'M', 'H']
		self.debugging = debugging
		self.printer = printer
		self.bound = bound
		self.inserter = PortfolioDao()
		self.passed = 0
		self.failed = 0

	def generator(self, seed, size):
		return ''.join(random.choice(seed) for _ in range(size))

	def populate(self):
		i = 0
		while i < self.bound:
			pk_id = random.randint(0, int(self.generator('0123456789', 20)))
			risk = random.choice(self.risks)
			login = random.choice(self.logins).encode('utf-8')
			
			addion_tuple = pk_id, risk, login
			self.inserter = PortfolioDao()			
			response = self.inserter.insert(login, risk, pk_id)
			if self.debugging:
				if response:
					if self.printer:
						print addion_tuple, colored(response, 'green')
					self.passed += 1
				else:
					if self.printer:
						print addion_tuple, colored(response, 'red')
					self.failed += 1
				i += 1
			

	def __str__(self):
		ans = ''
		ans += colored('Passed: ' + str(self.passed), 'green')
		ans += ' '
		ans += colored('Failed: ' + str(self.failed), 'red')
		return ans

class OfferantPopulator(object):

	def __init__(self, debugging, bound, printer):
		self.logins = [itm.user_login.login for itm in Active.objects.all()]
		self.types = ['1', '0']
		self.debugging = debugging
		self.printer = printer
		self.bound = bound
		self.inserter = OfferantDao()
		self.passed = 0
		self.failed = 0

	def populate(self):
		i = 0
		while i < self.bound:
			login = random.choice(self.logins).encode('utf-8')
			_type = random.choice(self.types)
			
			addion_tuple = login, _type
			self.inserter = OfferantDao()			
			response = self.inserter.insert(login, _type)
			if self.debugging:
				if response:
					if self.printer:
						print addion_tuple, colored(response, 'green')
					self.passed += 1
				else:
					if self.printer:
						print addion_tuple, colored(response, 'red')
					self.failed += 1
				i += 1
			

	def __str__(self):
		ans = ''
		ans += colored('Passed: ' + str(self.passed), 'green')
		ans += ' '
		ans += colored('Failed: ' + str(self.failed), 'red')
		return ans

class RentPopulator(object):

	def __init__(self, debugging, bound, printer):
		self.function = ['1', '0']
		self.length = ['1', '0']
		self.types = ['1', '0']
		self.offerants = [itm.user_login.user_login.login for itm in Offerant.objects.all()]
		self.debugging = debugging
		self.printer = printer
		self.bound = bound
		self.inserter = RentDao()
		self.passed = 0
		self.failed = 0

	def generator(self, size, seed = string.ascii_uppercase):
		return ''.join(random.choice(seed) for _ in range(size))

	def populate(self):
		i = 0
		while i < self.bound:
			pk_id = random.randint(0, int(self.generator(20, '0123456789')))
			name = self.generator(20)
			description = self.generator(130)			
			_fun = random.choice(self.function)
			_len = random.choice(self.length)
			_type = random.choice(self.types)
			login = random.choice(self.offerants).encode('utf-8')

			
			addion_tuple = pk_id, name, description, _fun, _len, _type
			self.inserter = RentDao()			
			response = self.inserter.insert(pk_id, name, description, _fun, _len, _type, login)
			if self.debugging:
				if response:
					if self.printer:
						print addion_tuple, colored(response, 'green')
					self.passed += 1
					
				else:
					if self.printer:
						print addion_tuple, colored(response, 'red')
					self.failed += 1
				i += 1
			

	def __str__(self):
		ans = ''
		ans += colored('Passed: ' + str(self.passed), 'green')
		ans += ' '
		ans += colored('Failed: ' + str(self.failed), 'red')
		return ans

class ValPopulator(object):

	def __init__(self, debugging, bound, printer):
		self.types = ['1', '0']
		self.rents = [itm.pk_id for itm in Rent.objects.all()]
		self.debugging = debugging
		self.printer = printer
		self.bound = bound
		self.inserter = ValDao()
		self.passed = 0
		self.failed = 0

	def generator(self, size, seed):
		return ''.join(random.choice(seed) for _ in range(size))

	def populate(self):
		i = 0
		while i < self.bound:
			pk_id = random.randint(0, int(self.generator(20, '0123456789')))
			name = self.generator(10, string.ascii_lowercase)
			description = self.generator(40, string.ascii_lowercase)
			_type = random.choice(self.types)
			amount = int(self.generator(5, string.digits))
			price = random.uniform(0.0, 15.0)
			rent = random.choice(self.rents)


			addion_tuple = pk_id, name, description, _type, amount, price, rent
			self.inserter = ValDao()			
			response = self.inserter.insert(pk_id, name, description, _type, amount, price, rent)
			if self.debugging:
				if response:
					if self.printer:
						print addion_tuple, colored(response, 'green')
					self.passed += 1
					
				else:
					if self.printer:
						print addion_tuple, colored(response, 'red')
					self.failed += 1
				i += 1
			

	def __str__(self):
		ans = ''
		ans += colored('Passed: ' + str(self.passed), 'green')
		ans += ' '
		ans += colored('Failed: ' + str(self.failed), 'red')
		return ans

class PortfolioValPopulator(object):

	def __init__(self, debugging, bound, printer):
		self.portfolios = [itm.pk_id for itm in Portfolio.objects.all()]
		self.vals = [itm.pk_id for itm in Val.objects.all()]
		self.debugging = debugging
		self.printer = printer
		self.bound = bound
		self.passed = 0
		self.failed = 0

	def generator(self, size, seed):
		return ''.join(random.choice(seed) for _ in range(size))

	def populate(self):
		i = 0
		while i < self.bound:
			pk_id = random.randint(0, int(self.generator(20, '0123456789')))
			portfolio = random.choice(self.portfolios)
			value = random.choice(self.vals)

			addion_tuple = pk_id, portfolio, value			
			response = False
			try:
				from django.db import connection
				cursor = connection.cursor()
				query = "INSERT INTO portfolios_vals VALUES(%s, %s, %s)"
				params = [pk_id, portfolio, value]
				cursor.execute(query, params)
				response = True
			except Exception, e:
				response = False
			if self.debugging:
				if response:
					if self.printer:
						print addion_tuple, colored(response, 'green')
					self.passed += 1
					
				else:
					if self.printer:
						print addion_tuple, colored(response, 'red')
					self.failed += 1
				i += 1
			

	def __str__(self):
		ans = ''
		ans += colored('Passed: ' + str(self.passed), 'green')
		ans += ' '
		ans += colored('Failed: ' + str(self.failed), 'red')
		return ans

class SolicitudePopulator(object):

	def __init__(self, debugging, bound, printer):
		self.types = ['1', '0']
		self.units = ['1', '0']
		self.logins = [itm.user_login.login for itm in Active.objects.all()]
		self.debugging = debugging
		self.printer = printer
		self.bound = bound
		self.inserter = SolicitudeDao()
		self.passed = 0
		self.failed = 0

	def generator(self, size, seed):
		return ''.join(random.choice(seed) for _ in range(size))

	def populate(self):
		i = 0
		while i < self.bound:
			pk_id = random.randint(0, int(self.generator(20, '0123456789')))
			_type = random.choice(self.types)
			amount = random.uniform(0.0, 15.00)
			unit = random.choice(self.units)
			login = random.choice(self.logins).encode('utf-8')


			addion_tuple = pk_id, _type, amount, unit, login
			self.inserter = SolicitudeDao()			
			response = self.inserter.insert(pk_id, _type, amount, unit, login)
			if self.debugging:
				if response:
					if self.printer:
						print addion_tuple, colored(response, 'green')
					self.passed += 1
					
				else:
					if self.printer:
						print addion_tuple, colored(response, 'red')
					self.failed += 1
				i += 1
			

	def __str__(self):
		ans = ''
		ans += colored('Passed: ' + str(self.passed), 'green')
		ans += ' '
		ans += colored('Failed: ' + str(self.failed), 'red')
		return ans

class SwapTransactionsPopulator(object):

	def __init__(self, debugging, bound, printer):
		self.solicitudes = [itm.pk_id for itm in Solicitude.objects.all()]
		self.debugging = debugging
		self.printer = printer
		self.bound = bound
		self.inserter = SwapTransactionDao()
		self.passed = 0
		self.failed = 0

	def generator(self, size, seed):
		return ''.join(random.choice(seed) for _ in range(size))

	def populate(self):
		i = 0
		while i < self.bound:
			pk_id = random.randint(0, int(self.generator(20, '0123456789')))
			s1 = random.choice(self.solicitudes)
			s2 = random.choice(self.solicitudes)

			addion_tuple = pk_id, s1, s2
			self.inserter = SwapTransactionDao()			
			response = self.inserter.insert(pk_id, s1, s2)
			if self.debugging:
				if response:
					if self.printer:
						print addion_tuple, colored(response, 'green')
					self.passed += 1
					
				else:
					if self.printer:
						print addion_tuple, colored(response, 'red')
					self.failed += 1
				i += 1
			

	def __str__(self):
		ans = ''
		ans += colored('Passed: ' + str(self.passed), 'green')
		ans += ' '
		ans += colored('Failed: ' + str(self.failed), 'red')
		return ans

class SolicitudeValPopulator(object):

	def __init__(self, debugging, bound, printer):
		self.solicitudes = [itm.pk_id for itm in Solicitude.objects.all()]
		self.vals = [itm.pk_id for itm in Val.objects.all()]
		self.debugging = debugging
		self.printer = printer
		self.bound = bound
		self.passed = 0
		self.failed = 0

	def populate(self):
		i = 0
		while i < self.bound:
			solicitude = random.choice(self.solicitudes)
			value = random.choice(self.vals)

			addion_tuple = solicitude, value			
			response = False
			try:
				from django.db import connection
				cursor = connection.cursor()
				query = "INSERT INTO solicitudes_val VALUES(%s, %s)"
				params = [solicitude, value]
				cursor.execute(query, params)
				response = True
			except Exception, e:
				response = False
			if self.debugging:
				if response:
					if self.printer:
						print addion_tuple, colored(response, 'green')
					self.passed += 1
					
				else:
					if self.printer:
						print addion_tuple, colored(response, 'red')
					self.failed += 1
				i += 1
			

	def __str__(self):
		ans = ''
		ans += colored('Passed: ' + str(self.passed), 'green')
		ans += ' '
		ans += colored('Failed: ' + str(self.failed), 'red')
		return ans

def cleaner(sure, secure):
	if sure and secure:
		from django.db import connection
		cursor = connection.cursor()
		queries = []

		query = "DELETE FROM solicitudes_val"
		queries.append(query)

		query = "DELETE FROM swap_transactions"
		queries.append(query)

		query = "DELETE FROM solicitudes"
		queries.append(query)

		query = "DELETE FROM portfolios_vals"
		queries.append(query)

		query = "DELETE FROM vals"
		queries.append(query)

		query = "DELETE FROM rents"
		queries.append(query)

		query = "DELETE FROM portfolios"
		queries.append(query)

		query = "DELETE FROM activespassives"
		queries.append(query)

		query = "DELETE FROM offerants"
		queries.append(query)

		query = "DELETE FROM legals"
		queries.append(query)

		query = "DELETE FROM investors"
		queries.append(query)

		query = "DELETE FROM passives"
		queries.append(query)

		query = "DELETE FROM actives"
		queries.append(query)

		query = "DELETE FROM users"
		queries.append(query)

		for query in queries:
			print query
			cursor.execute(query)

		connection.commit()
		connection.close()


def main():
	debugging = True
	printer = True
	reporter = True

	Users = UsersPopulator(debugging, 1, printer)
	Users.populate()

	Actives = ActivesPopulator(debugging, 1, printer) 
	Actives.populate()

	Passives = PassivesPopulator(debugging, 1, printer)
	Passives.populate()

	Investors = InvestorPopulator(debugging, 1, printer)
	Investors.populate()

	Legals = LegalPopulator(debugging, 1, printer)
	Legals.populate()

	ActivesPassives = ActivesPassivesPopulator(debugging, 1, printer)
	ActivesPassives.populate()

	Portfolios = PortfolioPopulator(debugging, 1, printer)
	Portfolios.populate()

	Offerants = OfferantPopulator(debugging, 1, printer)
	Offerants.populate()

	Rents = RentPopulator(debugging, 1, printer)
	Rents.populate()	

	Vals = ValPopulator(debugging, 1, printer)
	Vals.populate()	

	PortfolioVals = PortfolioValPopulator(debugging, 1, printer)
	PortfolioVals.populate()

	Solicitudes = SolicitudePopulator(debugging, 1, printer)
	Solicitudes.populate()

	Transactions = SwapTransactionsPopulator(debugging, 1, printer)
	Transactions.populate()

	SolicitudeVal = SolicitudeValPopulator(debugging, 1, printer)
	SolicitudeVal.populate()

	if reporter:
		entities = {'Users' : Users, 'Actives' : Actives, 
		'Passives' : Passives, 'Investors' : Investors, 'Legals' : Legals,
		'Portfolios' : Portfolios, 'Offerants' : Offerants, 'Rents' : Rents,
		'Vals' : Vals, 'PortfolioVals' : PortfolioVals, 'Solicitudes' : Solicitudes,
		'Transactions' : Transactions, 'SolicitudeVals' : SolicitudeVal}
		headers = ['Entity', 'Test']
		table = []
		for key in entities:
			dummy = [key, entities[key]]
			table.append(dummy)

		print tabulate(table, headers, tablefmt="grid")


populate = True
clean = False

if populate and not clean:
	main()
elif clean and not populate:
	cleaner(clean, not populate)