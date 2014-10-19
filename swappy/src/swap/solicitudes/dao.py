from django.db import connection
from models import SolicitudeDump
from resultset.resultSet import ResultSet 

class SolicitudeDao(object):

    def __init__(self):
        self.table_name = 'solicitudes'
        self.schema = ('pk_id', 'request_type', 'amount', 'amount_unit', 'created_at',
            'active_login')
        self.cursor = connection.cursor()
        self.rs = ResultSet()

    def find_all(self, test = False):
        ans = []
        if not test:
            try:            
                query = "SELECT * FROM portafolios ORDER BY pk_id"
                self.cursor.execute(query)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except Exception as e:
                print e
                return []
        self.rs.set(ans)
        return ans

    def find_by_id(self, pk_id, test = False):
        pk_id = str(pk_id)
        ans = []
        if not test:
            try:
                query = "SELECT * FROM portafolios WHERE pk_id = %s"
                params = [pk_id]
                self.cursor.execute(query, params)
                result_set = [item for item in self.cursor.fetchall()]
                for itm in result_set:
                    ans.append(self.process_row(itm))
            except Exception as e:
                print e
                return []
        self.rs.set(ans)        
        return ans
    
    def insert(self, login, risk, pk_id, test = False):
        params = map(str, [login, risk, pk_id])
        if not test:
            try:
                query = "INSERT INTO portafolios VALUES(%s, %s, %s)"
                self.cursor.execute(query, params)                
                return True
            except Exception as e:
            	print e                
                return False

    def update(self, dump_object, test = False):
        pk_id = dump_object.pk_id
        user_login = dump_object.user_login
        risk = dump_object.risk
        objects = self.find_by_id(pk_id)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = "UPDATE portafolios SET user_login = %s, risk = %s WHERE pk_id = %s"
                    params = [user_login, risk, pk_id]
                    self.cursor.execute(query, params)                    
                    return True
                except Exception as e:
                	print e
                	return False
        else:
            return False

    def remove(self, pk_id, test = False):
        pk_id = str(pk_id)
        objects = self.find_by_id(pk_id)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("DELETE FROM portafolios WHERE pk_id = %s")
                    params = [pk_id]
                    self.cursor.execute(query, params)                    
                    return True
                except Exception as e:
                    print e                    
                    return False
        else:            
            return False        

    def process_row(self, result_set):
        pk_id = result_set[0]
        user_login = result_set[1]
        risk = result_set[2]
        dump = PortfolioDump(pk_id, user_login, risk)
        return dump