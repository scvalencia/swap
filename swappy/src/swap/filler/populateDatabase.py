from genericusers.dao import GenericUserDao
import string
import random

FIRST_NAMES = 'first.txt'
LAST_NAMES = 'last.txt'
APELLIDOS = 'apellidos.txt'

last_names_index = {}
first_names_index = {}

def populate_users(bound):
	built_names_index()
	first_names_vals = first_names_index.values()
	last_names_vals = last_names_index.values()
	first_names = []
	last_names = []
	for itm in first_names_vals:
		for i in itm:
			first_names.append(i)

	for itm in last_names_vals:
		for i in itm:
			last_names.append(i)


	i = 0
	while i < bound:
		first = random.choice(first_names)
		last = random.choice(last_names)
		login = generate_login(first, last)
		user_id = generator('1234567890', 10)
		email = generate_email(login)
		phone = generator('1234567890', 7)
		password = generate_pass()
		print first, last, login, user_id, email, phone, password
		inserter = GenericUserDao()
		inserter.insert(login, user_id, password, first, last, email, phone)
		i += 1

def built_names_index():

	global first_names_index
	global last_names_index

	file_object_names = open(FIRST_NAMES)
	file_object_surnames = open(LAST_NAMES)

	for line in file_object_names:
		line = line.strip()
		if line[0] not in first_names_index:
			first_names_index[line[0]] = [line]
		else:
			first_names_index[line[0]].append(line)

	for line in file_object_surnames:
		line = line.strip()
		if line[0] not in last_names_index:
			last_names_index[line[0]] = [line]
		else:
			last_names_index[line[0]].append(line)

	file_object_surnames = open(APELLIDOS)

	for line in file_object_surnames:
		line = line.strip()
		if line[0] not in last_names_index:
			last_names_index[line[0]] = [line]
		else:
			last_names_index[line[0]].append(line)

def generator(seed, size):
	# Seed => string.ascii_uppercase + string.digits
	return ''.join(random.choice(seed) for _ in range(size))

def generate_login(name, last_name):
	ans = ''
	ans += name[0] + name[1]
	ans += generator(last_name, 4)
	return ans

def generate_email(login):
	return login + '@swap.in'

def generate_pass():
	seed = string.ascii_uppercase + string.digits
	return generator(seed, 6)

populate_users(2000)
	
