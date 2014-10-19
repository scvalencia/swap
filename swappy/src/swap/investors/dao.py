from django.db import connection
from models import Investor
from models import InvestorDump
from resultset.resultSet import ResultSet 

class InvestorDao(object):

    def __init__(self):
        self.table_name = 'investors'
        self.schema = ('user_login', 'is_enterprise')
        self.cursor = connection.cursor()
        self.rs = ResultSet()

    def find_all(self, test = False):
        ans = []
        if not test:
            try:            
                query = "SELECT * FROM investors ORDER BY user_login"
                self.cursor.execute(query)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except:
                return []
        else:
            try:
                objects = list(Legal.objects.all())
                result_set = [item for item in objects]
                for itm in result_set:
                    ans.append(self.process_object(itm))
            except:
                return []
        self.rs.set(ans)
        return ans

    def find_by_login(self, arg_login, test = False):
        arg_login = str(arg_login)
        ans = []
        if not test:
            try:
                query = "SELECT * FROM investors WHERE user_login = %s"
                params = [arg_login]
                self.cursor.execute(query, params)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except:
                return []
        else:
            try:
                objects = list(Legal.objects.filter(legal_id = legal_id))
                result_set = [item for item in objects]
                for itm in result_set:
                    ans.append(self.process_object(itm))
            except:
                return []
        self.rs.set(ans)        
        return ans
    
    def insert(self, arg_login, arg_is_enterprise, test = False):
        arg_login = str(arg_login)
        arg_is_enterprise = str(arg_is_enterprise)
        if not test:
            try:
                query = "INSERT INTO investors VALUES(%s, %s)"
                params = [arg_login, arg_is_enterprise]
                self.cursor.execute(query, params)                
                return True
            except Exception as e:
            	print e                
                return False
        else:
            try:
                generic_user_object = Legal(legal_id = legal_id, legal_name = legal_name, 
                    user_login = user_login)
                generic_user_object.save()                
                return True
            except:                
                return False

    def update(self, user_object, test = False):
        user_login = user_object.user_login
        is_enterprise = user_object.is_enterprise
        objects = self.find_by_login(user_login)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("UPDATE investors "
                             "SET is_enterprise = %s "
                             "WHERE user_login = %s")
                    params = [is_enterprise, user_login]
                    self.cursor.execute(query, params)                    
                    return True
                except Exception as e:
                	print e
                	return False
            else:
                try:
                    one_object = Legal.objects.filter(legal_id = legal_id).update(legal_name = legal_name,
                        user_login = user_login)                    
                    return True
                except:                    
                    return False
        else:
            return False

    def remove(self, user_login, test = False):
        user_login = str(user_login)
        objects = self.find_by_login(user_login)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("DELETE FROM investors WHERE user_login = %s")
                    params = [user_login]
                    self.cursor.execute(query, params)                    
                    return True
                except:                    
                    return False
            else:
                try:
                    Legal.objects.filter(legal_id = legal_id).delete()                    
                    return True
                except:                    
                    return False
        else:            
            return False

    def process_object(self, generic_object):
        user_login = generic_object.user_login
        is_enterprise = generic_object.is_enterprise
        dump = InvestorDump(user_login, is_enterprise)
        return dump

    def process_row(self, result_set):
        user_login = result_set[0]
        is_enterprise = result_set[1]
        dump = InvestorDump(user_login, is_enterprise)
        return dump