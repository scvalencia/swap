from django.db import connection
from models import GenericUser
from models import GenericUserDump
from models import Legal
from models import LegalDump

class GenericUserDao(object):

    def __init__(self):
        self.cursor = connection.cursor()

    def find_all(self, test = False):
    	ans = []
    	if not test:			
    		query = "SELECT * FROM users ORDER BY login"
    		self.cursor.execute(query)
    		result_set = [item for item in self.cursor.fetchall()]
    		for itm in result_set:
    			ans.append(self.process_row(itm))
    	else:
    		objects = list(GenericUser.objects.all())
    		result_set = [item for item in objects]
    		for itm in result_set:
    			ans.append(self.process_generic_user_object(itm))
    	return ans

    def find_by_login(self, arg_login, test = False):
        login = str(arg_login)
        ans = []
        if not test:
            query = "SELECT * FROM users WHERE login = %s"
            params = [login]
            self.cursor.execute(query, params)
            result_set = [item for item in self.cursor.fetchall()]
            for itm in result_set:
                ans.append(self.process_row(itm))
        else:
            objects = list(GenericUser.objects.filter(login = login))
            result_set = [item for item in objects]
            for itm in result_set:
                ans.append(self.process_generic_user_object(itm))
        return ans

    def find_by_id(self, id, test = False):
        pass

    def find_by_first_name(self, first_name, test = False):
        pass

    def find_by_last_name(self, last_name, test = False):
        pass

    def find_by_email(self, email, test = False):
        pass

    def find_by_phone(self, phone, test = False):
        pass
    
    def insert(self, arg_user_login, arg_available_money, test = False):
        user_login = str(arg_user_login)
        available_money = str(arg_available_money)
        if not test:
            active_object = ActiveDump(user_login, available_money)
            query = "INSERT INTO actives VALUES(%s, %s)"
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

    def remove(self, active_object, test = False):
        pass

    def process_generic_user_object(self, generic_user_object):
        login = generic_user_object.login
        user_id = generic_user_object.user_id
        user_pass = generic_user_object.user_pass
        first_name = generic_user_object.first_name
        last_name = generic_user_object.last_name
        email = generic_user_object.email
        phone = generic_user_object.phone
        generic_user_dump = GenericUserDump(login, user_id, user_pass, 
            first_name, last_name, email, phone)
        return generic_user_dump

    def process_row(self, result_set):
        login = result_set[0]
        user_id = result_set[1]
        first_name = result_set[2]
        last_name = result_set[3]
        email = result_set[4]
        phone = result_set[5]
        user_pass = result_set[6]
        generic_user_object = GenericUserDump(login, user_id, user_pass, 
            first_name, last_name, email, phone)
        return generic_user_object

class LegalDao(object):

    def __init__(self):
        aself.cursor = connection.cursor()