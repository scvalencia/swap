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
                query = "SELECT * FROM solicitudes ORDER BY pk_id"
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
                query = "SELECT * FROM solicitudes WHERE pk_id = %s"
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
    
    def insert(self, pk_id, request_type, amount, amount_unit, 
        created_at, active_login, test = False):
        params = [int(pk_id), str(request_type), str(float(amount)),
        str(amount_unit), str(active_login)]
        if not test:
            try:
                query = "INSERT INTO solicitudes VALUES(%s, %s, %s, %s, Current_Timestamp, %s)"
                self.cursor.execute(query, params)                
                return True
            except Exception as e:
            	print e                
                return False

    def update(self, dump_object, test = False):
        pk_id = dump_object.pk_id
        request_type = dump_object.request_type
        amount = dump_object.amount
        amount_unit = dump_object.amount_unit
        created_at = dump_object.created_at
        active_login = dump_object.active_login
        objects = self.find_by_id(pk_id)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("UPDATE solicitudes "
                             "SET request_type = %s, amount = %s, amount_unit = %s, active_login = %s "
                             "WHERE pk_id = %s")
                    params = [request_type, str(float(amount)), amount_unit, active_login, int(pk_id)]
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
                    query = ("DELETE FROM solicitudes WHERE pk_id = %s")
                    params = [pk_id]
                    self.cursor.execute(query, params)                    
                    return True
                except Exception as e:
                    print e                    
                    return False
        else:            
            return False        

    def process_row(self, rs):
        pk_id = rs[0]
        request_type = rs[1]
        amount = rs[2]
        amount_unit = rs[3]
        created_at = rs[4]
        active_login = rs[5]
        dump = SolicitudeDump(pk_id, request_type, amount, 
            amount_unit, created_at, active_login) 
        return dump