from django.db import connection
from models import Offerant
from models import OfferantDump
from resultset.resultSet import ResultSet 

class OfferantDao(object):

    def __init__(self):
        self.table_name = 'offerants'
        self.schema = ('user_login', 'offerant_type')
        self.cursor = connection.cursor()
        self.rs = ResultSet()

    def find_all(self, test = False):
        ans = []
        if not test:
            try:            
                query = "SELECT * FROM offerants ORDER BY user_login"
                self.cursor.execute(query)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except Exception as e:
                print e
                return []
        self.rs.set(ans)
        return ans

    def find_by_login(self, arg_login, test = False):
        arg_login = str(arg_login)
        ans = []
        if not test:
            try:
                query = "SELECT * FROM offerants WHERE user_login = %s"
                params = [arg_login]
                self.cursor.execute(query, params)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except Exception as e:
                print e
                return []
        self.rs.set(ans)        
        return ans
    
    def insert(self, arg_login, arg_offerant_type, test = False):
        arg_login = str(arg_login)
        arg_offerant_type = str(arg_offerant_type)
        if not test:
            try:
                query = "INSERT INTO offerants VALUES(%s, %s)"
                params = [arg_login, arg_offerant_type]
                self.cursor.execute(query, params)                
                return True
            except Exception as e:
            	print e                
                return False

    def update(self, user_object, test = False):
        user_login = user_object.user_login
        offerant_type = user_object.offerant_type
        objects = self.find_by_login(user_login)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("UPDATE offerants "
                             "SET offerant_type = %s "
                             "WHERE user_login = %s")
                    params = [offerant_type, user_login]
                    self.cursor.execute(query, params)                    
                    return True
                except Exception as e:
                	print e
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
                    query = ("DELETE FROM offerants WHERE user_login = %s")
                    params = [user_login]
                    self.cursor.execute(query, params)                    
                    return True
                except Exception as e:
                    print e                    
                    return False
        else:            
            return False        

    def process_row(self, result_set):
        user_login = result_set[0]
        offerant_type = result_set[1]
        dump = OfferantDump(user_login, offerant_type)
        return dump