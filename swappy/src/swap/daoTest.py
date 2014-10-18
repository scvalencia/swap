from genericusers.models import GenericUser
from genericusers.models import GenericUserDump
from genericusers.dao import GenericUserDao
from django.db import connection

class GenericUserDaoTest(object):

	def __init__(self):
		self.g = GenericUserDao()
		self.rs = self.g.rs

	def test_find_all(self, test = False):
		self.g = GenericUserDao()
		rs = self.g.find_all(test)
		self.print_result_set(rs)		

	def test_find_by_login(self, login, test = False):
		self.g = GenericUserDao()
		rs = self.g.find_by_login(login, test)
		self.print_result_set(rs)

	def test_find_by_id(self, arg_id, test = False):
		self.g = GenericUserDao()
		rs = self.g.find_by_id(arg_id, test)
		self.print_result_set(rs)

	def test_find_by_fisrt_name(self, fname, test = False):
		self.g = GenericUserDao()
		rs = self.g.find_by_first_name(fname, test)
		self.print_result_set(rs)

	def test_find_by_last_name(self, lname, test = False):
		self.g = GenericUserDao()
		rs = self.g.find_by_last_name(lname, test)
		self.print_result_set(rs)

	def test_find_by_email(self, email, test = False):
		self.g = GenericUserDao()
		rs = self.g.find_by_email(email, test)
		self.print_result_set(rs)

	def test_find_by_phone(self, phone, test = False):
		self.g = GenericUserDao()
		rs = self.g.find_by_phone(phone, test)
		self.print_result_set(rs)

	def test_insert(self, arg_login, arg_user_id, arg_user_pass, arg_first_name, 
        arg_last_name, arg_email, arg_phone, test = False):
		self.g = GenericUserDao()
		self.g.insert(arg_login, arg_user_id, arg_user_pass, arg_first_name, 
			arg_last_name, arg_email, arg_phone)
		self.g = GenericUserDao()
		rs = self.g.find_all(test)
		self.print_result_set(rs)

	def test_update(self, test = False):
		user_object = GenericUserDump('mario', '23091823', 'filo', 'Mario', 
			'Hernandez', 'marito@hotmail.co', '2924483840')
		self.g = GenericUserDao()
		self.g.update(user_object, test)
		self.g = GenericUserDao()
		rs = self.g.find_all(test)
		self.print_result_set(rs)

	def test_remove(self, login, test = False):
		self.g = GenericUserDao()
		self.g.remove(login, test)
		self.g = GenericUserDao()
		rs = self.g.find_all(test)
		self.print_result_set(rs)

	def print_result_set(self, rs):
		print '=' * 100
		for itm in rs:
			print itm
		print '=' * 100

def main_slave_homebrew():
	tester = GenericUserDaoTest()
	tester.test_find_all()
	tester.test_find_by_login('nene')
	tester.test_find_by_id('2283192743')
	tester.test_find_by_fisrt_name('Guillermo')
	tester.test_find_by_last_name('Valencia')
	tester.test_find_by_email('niconico@hotmail.com')
	tester.test_find_by_phone('435345345')
	tester.test_insert('Eduardo', '3243423432', 'vafsg3gwgf', 'Eduward',
	 'Yamin', 'sdfdffs@dfsd.cm', 'sdvcvcz')
	tester.test_update()
	tester.test_remove('jcbages')

def main_slave_industrial():
	tester = GenericUserDaoTest()
	tester.test_find_all(True)
	tester.test_find_by_login('nene', True)
	tester.test_find_by_id('2283192743', True)
	tester.test_find_by_fisrt_name('Guillermo', True)
	tester.test_find_by_last_name('Valencia', True)
	tester.test_find_by_email('niconico@hotmail.com', True)
	tester.test_find_by_phone('435345345', True)
	tester.test_insert('Camila', '3243423432', 'vafsg3gwgf', 'Eduward',
	 'Yamin', 'sdfdffs@dfsd.cm', 'sdvcvcz', True)
	tester.test_update(True)
	tester.test_remove('jcbages', True)

def main(mine = False):
	if mine:
		main_slave_homebrew()
	else:
		main_slave_industrial()
	connection.close()

main()