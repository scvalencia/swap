from django.db import connection

from models import Passive
from models import PassiveDump
from resultset.resultSet import ResultSet 

class PassiveDao(object):

    def __init__(self):
        self.table_name = 'passives'
        self.schema = ('passive_register', 'user_login')
        self.cursor = connection.cursor()
        self.rs = ResultSet()

    def find_all(self, test = False):
        ans = []
        if not test:
            try:            
                query = "SELECT * FROM passives ORDER BY passive_register"
                self.cursor.execute(query)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except Exception as e:
                print e
                return []
        self.rs.set(ans)
        return ans

    def find_by_register(self, arg, test = False):
        arg = str(arg)
        ans = []
        if not test:
            try:
                query = "SELECT * FROM passives WHERE passive_register = %s"
                params = [arg]
                self.cursor.execute(query, params)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except Exception as e:
                print e
                return []
        self.rs.set(ans)        
        return ans
    
    def insert(self, reg, login, test = False):
        reg = str(reg)
        login = str(login)
        if not test:
            try:
                query = "INSERT INTO passives VALUES(%s, %s)"
                params = [reg, login]
                self.cursor.execute(query, params)                
                return True
            except Exception as e:
            	print e                
                return False

    def update(self, arg_object, test = False):
        reg = arg_object.passive_register
        log = arg_object.user_login
        objects = self.find_by_register(reg)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("UPDATE passives "
                             "SET user_login = %s "
                             "WHERE passive_register = %s")
                    params = [log, reg]
                    self.cursor.execute(query, params)                    
                    return True
                except Exception as e:
                	print e
                	return False
        else:
            return False

    def remove(self, reg, test = False):
        reg = str(reg)
        objects = self.find_by_register(reg)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("DELETE FROM passives WHERE passive_register = %s")
                    params = [reg]
                    self.cursor.execute(query, params)                    
                    return True
                except Exception as e:
                    print e                    
                    return False
        else:            
            return False        

    def process_row(self, result_set):
        passive_register = result_set[0]
        user_login = result_set[1]
        dump = PassiveDump(passive_register, user_login)
        return dump