from resultset.resultSet import ResultSet
from django.db import connection
from models import ActiveDump
from models import Active

class ActiveDao(object):
    
    def __init__(self):
        self.table_name = 'actives'
        self.schema = ('user_login', 'available_money')
        self.cursor = connection.cursor()
        self.rs = ResultSet()

    def find_all(self, test = False):
        self.cursor = connection.cursor()
        ans = []
        if not test:
            try:
                query = "SELECT * FROM actives ORDER BY user_login"
                self.cursor.execute(query)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except Exception as e:
                print e
                return []
        else:
            try:
                objects = list(Active.objects.all())
                result_set = [item for item in objects]
                for itm in result_set:
                    ans.append(self.process_object(itm))
            except Exception as e:
                print e
                return []
        self.rs.set(ans)
        return ans

    def find_by_login(self, arg_login, test = False):
        login = str(arg_login)
        ans = []
        if not test:
            try:
                query = "SELECT * FROM actives WHERE user_login = %s"
                params = [login]
                self.cursor.execute(query, params)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except Exception as e:
                print e                
                return []
        else:
            try:
                objects = list(Active.objects.filter(user_login = login))
                result_set = [item for item in objects]
                for itm in result_set:
                    ans.append(self.process_object(itm))
            except Exception as e:
                print e                
                return []
        self.rs.set(ans)        
        return ans

    def insert(self, arg_login, arg_money, test = False):
        login = str(arg_login)
        money = str(arg_money)
        if not test:
            try:
                query = "INSERT INTO actives VALUES(%s, %s)"
                params = [login, money]
                self.cursor.execute(query, params)                
                return True
            except Exception as e:
                print e               
                return False
        else:
            try:
                generic_object = Active(login = login, user_id = user_id)
                generic_object.save()                
                return True
            except Exception as e:
                print e                
                return False

    def update(self, active_object, test = False):
        login = active_object.user_login
        money = active_object.available_money
        objects = self.find_by_login(login)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("UPDATE actives "
                             "SET available_money = %s "
                             "WHERE user_login = %s")
                    params = [money, login]
                    self.cursor.execute(query, params)                    
                    return True
                except Exception as e:
                    print e                    
                    return False
            else:
                try:
                    one_object = Active.objects.filter(user_login = login).update(available_money = money)                    
                    return True
                except Exception as e:
                    print e                    
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
                    query = ("DELETE FROM actives WHERE user_login = %s")
                    params = [login]
                    self.cursor.execute(query, params)                    
                    return True
                except Exception as e:
                    print e                    
                    return False
            else:
                try:
                    Active.objects.filter(user_login = login).delete()                    
                    return True
                except Exception as e:
                    print e                    
                    return False
        else:            
            return False

    def process_object(self, generic_object):
        login = generic_object.user_login
        money = generic_object.available_money
        dump = ActiveDump(login, money)
        return dump

    def process_row(self, result_set):
        login = result_set[0]
        money = result_set[1]
        generic_object = ActiveDump(login, money)
        return generic_object