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




def main():
	debugging = True
	printer = False
	reporter = True
	size = 20000

	Users = UsersPopulator(debugging, size, printer)
	Users.populate()

	Actives = ActivesPopulator(debugging, size, printer) 
	Actives.populate()

	Passives = PassivesPopulator(debugging, size, printer)
	Passives.populate()

	Investors = InvestorPopulator(debugging, size, printer)
	Investors.populate()

	Legals = LegalPopulator(debugging, size, printer)
	Legals.populate()

	ActivesPassives = ActivesPassivesPopulator(debugging, size, printer)
	ActivesPassives.populate()

	if reporter:
		entities = {'Users' : Users, 'Actives' : Actives, 
		'Passives' : Passives, 'Investors' : Investors, 'Legals' : Legals}
		headers = ['Entity', 'Test']
		table = []
		for key in entities:
			dummy = [key, entities[key]]
			table.append(dummy)

		print tabulate(table, headers, tablefmt="grid")

main()
	
