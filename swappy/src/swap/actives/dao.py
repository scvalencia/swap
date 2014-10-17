from django.db import connection
from models import Active

class ActiveDao(object):
	
	def __init__(self):
		self.cursor = connection.cursor()

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
    	pass

    def add_actives(self, argument_tuples):
    	for (login, passive, arg_money) in argument_tuples:
    		self.add_actives(login, passive, arg_money)


	def __str__(self):
		pass 