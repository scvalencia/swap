from django.db import connection
from models import ActiveDump
from models import Active


class ActiveDao(object):
	
	def __init__(self):
		self.cursor = connection.cursor()

	def process_row(self, result_set):
        user_login = result_set[0]
        passive_register = result_set[1]
        available_money = result_set[2]
        active_object = ActiveDump(user_login, passive_register, available_money)
        return active_object

	def find_all(self, test = False):
		ans = []
		if not test:			
			query = "SELECT * FROM actives ORDER BY user_login"
			self.cursor.execute(query)
			result_set = [item for item in self.cursor.fetchall()]
			for itm in result_set:
				ans.append(process_row(itm))			
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
			self.cursor.execute(query)
			result_set = [item for item in self.cursor.fetchall()]
			for itm in result_set:
				ans.append(process_row(itm))
		else:
			objects = list(Active.objects.filter(user_login = login))
			result_set = [item for item in self.cursor.fetchall()]
			for itm in result_set:
				ans.append(itm)
		return ans

	def finb_by_passive(self, passive, test = False):
		ans = []
		if not test:
			query = "SELECT * FROM actives WHERE user_login = %s"
			self.cursor.execute(query)
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
		pass

	def create(self, active_object, test = False):
		pass

	def update(self, active_object, test = False):
		pass

	def save(self, active_object, test = False):
		pass

	def remove(self, login, test = False):
		pass




	def get_active_by_login(self, arg_user_login):
		only_active = None
		query = "SELECT * FROM actives WHERE user_login = %s"
		params = [arg_user_login]
		self.cursor.execute(query, params)
		result_set = [item for item in self.cursor.fetchall()]
		length = len(tuples)
		if length == 0:
			only_active = None
		else:
			actives = []
			for itm in result_set:
				user_login = itm[0]
    			passive_register = itm[1]
    			available_money = itm[2]
    			active = Active(user_login, passive_register, available_money)
    			actives.append(active)

			only_active = actives.pop()

		connection.close()
		return only_active

	def get_actives_by_passive_register(self, arg_passive_register):
		actives = []
		query = "SELECT * FROM actives WHERE passive_register = %s"
		params = [arg_passive_register]
		self.cursor.execute(query, params)
		result_set = [item for item in self.cursor.fetchall()]
		for item in result_set:
			user_login = itm[0]
    		passive_register = itm[1]
    		available_money = itm[2]
    		active = Active(user_login, passive_register, available_money)
    		actives.append(active)
    	return actives

    def get_actives_by_available_money(self, arg_available_money):
    	actives = []
		query = "SELECT * FROM actives WHERE available_money = %s"
		params = [arg_available_money]
		self.cursor.execute(query, params)
		result_set = [item for item in self.cursor.fetchall()]
		for item in result_set:
			user_login = itm[0]
    		passive_register = itm[1]
    		available_money = itm[2]
    		active = Active(user_login, passive_register, available_money)
    		actives.append(active)
    	return actives

    def add_active(self, arg_login, arg_passive, arg_money):
    	added_Actives = []

    def add_actives(self, argument_tuples):
    	for (login, passive, arg_money) in argument_tuples:
    		self.add_actives(login, passive, arg_money)


	def __str__(self):
		pass 