from django.db import connection
from models import GenericUser
from models import GenericUserDump
from models import Legal
from models import LegalDump
from resultset.resultSet import ResultSet 

class GenericUserDao(object):

    def __init__(self):
        self.cursor = connection.cursor()
        self.rs = ResultSet()

    def find_all(self, test = False):
    	ans = []
    	if not test:
            try:			
        		query = "SELECT * FROM users ORDER BY login"
        		self.cursor.execute(query)
        		result_set = [item for item in self.cursor.fetchall()]
        		for itm in result_set:
        			ans.append(self.process_row(itm))
            except:
                return []
    	else:
            try:
        		objects = list(GenericUser.objects.all())
        		result_set = [item for item in objects]
        		for itm in result_set:
        			ans.append(self.process_generic_user_object(itm))
            except:
                return []
        self.rs.set(ans)
    	return ans

    def find_by_login(self, arg_login, test = False):
        login = str(arg_login)
        ans = []
        if not test:
            try:
                query = "SELECT * FROM users WHERE login = %s"
                params = [login]
                self.cursor.execute(query, params)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except:
                return []
        else:
            try:
                objects = list(GenericUser.objects.filter(login = login))
                result_set = [item for item in objects]
                for itm in result_set:
                    ans.append(self.process_generic_user_object(itm))
            except:
                return []
        self.rs.set(ans)
        return ans

    def find_by_id(self, arg_id, test = False):
        arg_id = str(arg_id)
        ans = []
        if not test:
            try:
                query = "SELECT * FROM users WHERE user_id = %s"
                params = [arg_id]
                self.cursor.execute(query, params)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except:
                return []
        else:
            try:
                objects = list(GenericUser.objects.filter(user_id = arg_id))
                result_set = [item for item in objects]
                for itm in result_set:
                    ans.append(self.process_generic_user_object(itm))
            except:
                return []
        self.rs.set(ans)
        return ans

    def find_by_first_name(self, first_name, test = False):
        first_name = str(first_name)
        ans = []
        if not test:
            try:
                query = "SELECT * FROM users WHERE first_name = %s"
                params = [first_name]
                self.cursor.execute(query, params)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except:
                return []
        else:
            try:
                objects = list(GenericUser.objects.filter(first_name = first_name))
                result_set = [item for item in objects]
                for itm in result_set:
                    ans.append(self.process_generic_user_object(itm))
            except:
                return []
        self.rs.set(ans)
        return ans

    def find_by_last_name(self, last_name, test = False):
        last_name = str(last_name)
        ans = []
        if not test:
            try:
                query = "SELECT * FROM users WHERE last_name = %s"
                params = [last_name]
                self.cursor.execute(query, params)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except:
                return []
        else:
            try:
                objects = list(GenericUser.objects.filter(last_name = last_name))
                result_set = [item for item in objects]
                for itm in result_set:
                    ans.append(self.process_generic_user_object(itm))
            except:
                return []
        self.rs.set(ans)
        return ans

    def find_by_email(self, email, test = False):
        email = str(email)
        ans = []
        if not test:
            try:
                query = "SELECT * FROM users WHERE email = %s"
                params = [email]
                self.cursor.execute(query, params)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except:
                return []
        else:
            try:
                objects = list(GenericUser.objects.filter(email = email))
                result_set = [item for item in objects]
                for itm in result_set:
                    ans.append(self.process_generic_user_object(itm))
            except:
                return []
        self.rs.set(ans)
        return ans

    def find_by_phone(self, phone, test = False):
        phone = str(phone)
        ans = []
        if not test:
            try:
                query = "SELECT * FROM users WHERE phone = %s"
                params = [phone]
                self.cursor.execute(query, params)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except:
                return []
        else:
            try:
                objects = list(GenericUser.objects.filter(phone = phone))
                result_set = [item for item in objects]
                for itm in result_set:
                    ans.append(self.process_generic_user_object(itm))
            except:
                return []
        self.rs.set(ans)
        return ans
    
    def insert(self, arg_login, arg_user_id, arg_user_pass, arg_first_name, 
        arg_last_name, arg_email, arg_phone, test = False):
        login = str(arg_login)
        user_id = str(arg_user_id)
        user_pass = str(arg_user_pass)
        first_name = str(arg_first_name)
        last_name = str(arg_last_name)
        email = str(arg_email)
        phone = str(arg_phone)
        if not test:
            try:
                query = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s)"
                params = [login, user_id, user_pass, first_name, last_name, email, phone]
                self.cursor.execute(query, params)
                return True
            except:
                return False
        else:
            try:
                generic_user_object = GenericUser(login = login, user_id = user_id, user_pass = user_pass,
                    first_name = first_name, last_name = last_name, email = email, phone = phone)
                generic_user_object.save()
                return True
            except:
                return False

    def create(self, active_object, test = False):
        ans = self.insert(active_object.login, active_object.user_id, 
            active_object.user_pass, active_object.first_name, active_object.last_name,
            active_object.email, active_object.phone, test)
        return ans

    def update(self, active_object, test = False):
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