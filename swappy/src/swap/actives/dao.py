from django.db import connection
from models import ActiveDump
from models import Active


class ActiveDao(object):
    
    def __init__(self):
        self.cursor = connection.cursor()

<<<<<<< HEAD
	def process_active_object(self, active_object):
		user_login = active_object.user_login
		available_money = active_object.available_money
		active_dump = ActiveDump(user_login, available_money)
		return active_dump

	def process_row(self, result_set):
		user_login = result_set[0]
		available_money = result_set[1]
		active_object = ActiveDump(user_login, available_money)
		return active_object

	def find_all(self, test = False):
		ans = []
		if not test:			
			query = "SELECT * FROM actives ORDER BY user_login"
			self.cursor.execute(query)
			result_set = [item for item in self.cursor.fetchall()]
			for itm in result_set:
				ans.append(self.process_row(itm))			
		else:
			objects = list(Active.objects.all())
			result_set = [item for item in self.cursor.fetchall()]
			for itm in result_set:
				ans.append(itm)
		return ans

	def find_by_login(self, login, test = False):
		ans = []
		if not test:
			query = "SELECT * FROM actives WHERE user_login = %s"
			params = [login]
			self.cursor.execute(query, login)
			result_set = [item for item in self.cursor.fetchall()]
			for itm in result_set:
				ans.append(process_row(itm))
		else:
			objects = list(Active.objects.filter(user_login = login))
			result_set = [item for item in self.cursor.fetchall()]
			for itm in result_set:
				ans.append(itm)
		return ans

	def find_by_money(self, money, test = False):
		ans = []
		if not test:
			query = "SELECT * FROM actives WHERE available_money = %s"
			params = [money]
			self.cursor.execute(query, params)
			result_set = [item for item in self.cursor.fetchall()]
			for itm in result_set:
				ans.append(process_row(itm))
		else:
			objects = list(Active.objects.filter(available_money = money))
			result_set = [item for item in self.cursor.fetchall()]
			for itm in result_set:
				ans.append(itm)
		return ans

	def insert(self, arg_user_login, arg_available_money, test = False):
		user_login = str(user_login)
		available_money = float(available_money)
		if not test:
			active_object = ActiveDump(user_login, available_money)
			query = "INSERT INTO actives VALUES(%s, %f)"
			params = [user_login, available_money]
			self.cursor.execute(query, params)
		else:
			active_object = Active(user_login = arg_user_login, 
				available_money = arg_available_money)
			active_object.save()

	def create(self, active_object, test = False):
		user_login = active_object.user_login
		available_money = active_object.available_money
		self.insert(user_login, available_money, test)

	def update(self, active_object, test = False):
		pass

	def save(self, active_object, test = False):
		pass

	def remove(self, login, test = False):
		pass

