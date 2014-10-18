from django.db import connection
from models import GenericUser
from models import GenericUserDump
from models import Legal
from models import LegalDump
from resultset.resultSet import ResultSet 

class GenericUserDao(object):

    def __init__(self):
        self.table_name = 'users'
        self.schema = ('login', 'user_id', 'first_name', 'last_name', 
            'email', 'phone', 'user_pass')
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
        			ans.append(self.process_object(itm))
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
                    ans.append(self.process_object(itm))
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

    def update(self, user_object, test = False):
        login = user_object.login
        user_id = user_object.user_id
        user_pass = user_object.user_pass
        first_name = user_object.first_name
        last_name = user_object.last_name
        email = user_object.email
        phone = user_object.phone
        objects = self.find_by_login(login)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("UPDATE users "
                             "SET user_id = %s, user_pass = %s, first_name = %s, last_name = %s, "
                             "email = %s, phone = %s "
                             "WHERE login = %s")
                    params = [user_id, user_pass, first_name, last_name, email, phone, login]
                    self.cursor.execute(query, params)                    
                    return True
                except:                    
                    return False
            else:
                try:
                    one_object = GenericUser.objects.filter(login = login).update(user_id = user_id,
                        user_pass = user_pass, first_name = first_name, last_name = last_name,
                        email = email, phone = phone)                    
                    return True
                except:                    
                    return False
        else:
            return False

    def remove(self, login, test = False):
        login = str(login)
        objects = self.find_by_login(login)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("DELETE FROM users WHERE login = %s")
                    params = [login]
                    self.cursor.execute(query, params)                    
                    return True
                except:                    
                    return False
            else:
                try:
                    GenericUser.objects.filter(login = login).delete()                    
                    return True
                except:                    
                    return False
        else:            
            return False

    def process_object(self, generic_user_object):
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
        self.table_name = 'legals'
        self.schema = ('legal_id', 'legal_name', 'user_login')
        self.cursor = connection.cursor()
        self.rs = ResultSet()

    def find_all(self, test = False):
        ans = []
        if not test:
            try:            
                query = "SELECT * FROM legals ORDER BY login"
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
                    ans.append(self.process_object(itm))
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
                    ans.append(self.process_object(itm))
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

    def update(self, user_object, test = False):
        login = user_object.login
        user_id = user_object.user_id
        user_pass = user_object.user_pass
        first_name = user_object.first_name
        last_name = user_object.last_name
        email = user_object.email
        phone = user_object.phone
        objects = self.find_by_login(login)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("UPDATE users "
                             "SET user_id = %s, user_pass = %s, first_name = %s, last_name = %s, "
                             "email = %s, phone = %s "
                             "WHERE login = %s")
                    params = [user_id, user_pass, first_name, last_name, email, phone, login]
                    self.cursor.execute(query, params)                    
                    return True
                except:                    
                    return False
            else:
                try:
                    one_object = GenericUser.objects.filter(login = login).update(user_id = user_id,
                        user_pass = user_pass, first_name = first_name, last_name = last_name,
                        email = email, phone = phone)                    
                    return True
                except:                    
                    return False
        else:
            return False

    def remove(self, login, test = False):
        login = str(login)
        objects = self.find_by_login(login)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("DELETE FROM users WHERE login = %s")
                    params = [login]
                    self.cursor.execute(query, params)                    
                    return True
                except:                    
                    return False
            else:
                try:
                    GenericUser.objects.filter(login = login).delete()                    
                    return True
                except:                    
                    return False
        else:            
            return False

    def process_object(self, generic_user_object):
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