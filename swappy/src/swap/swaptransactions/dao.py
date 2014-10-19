from django.db import connection
from models import SwapTransactionDump
from resultset.resultSet import ResultSet 

class SwapTransactionDao(object):

    def __init__(self):
        self.table_name = 'swap_transactions'
        self.schema = ('pk_id', 'created_at', 'solicitude_1_pk', 'solicitude_2_pk')
        self.cursor = connection.cursor()
        self.rs = ResultSet()

    def find_all(self, test = False):
        ans = []
        if not test:
            try:            
                query = "SELECT * FROM swap_transactions ORDER BY pk_id"
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
        pk_id = int(pk_id)
        ans = []
        if not test:
            try:
                query = "SELECT * FROM swap_transactions WHERE pk_id = %s"
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
    
    def insert(self, pk_id, solicitude_1_pk, solicitude_2_pk, test = False):
        params = [pk_id, solicitude_1_pk, solicitude_2_pk]
        params = map(int, params)
        if not test:
            try:
                query = "INSERT INTO swap_transactions VALUES(%s, Current_Timestamp, %s, %s)"
                self.cursor.execute(query, params)                
                return True
            except Exception as e:
            	print e                
                return False

    def update(self, dump_object, test = False):
        pk_id = dump_object.pk_id
        solicitude_1_pk = dump_object.solicitude_1_pk
        solicitude_2_pk = dump_object.solicitude_2_pk
        objects = self.find_by_id(pk_id)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("UPDATE swap_transactions "
                             "SET solicitude_1_pk = %s, solicitude_2_pk = %s "
                             "WHERE pk_id = %s")
                    params = [solicitude_1_pk, solicitude_2_pk, pk_id]
                    self.cursor.execute(query, params)                    
                    return True
                except Exception as e:
                	print e
                	return False
        else:
            return False

    def remove(self, pk_id, test = False):
        pk_id = int(pk_id)
        objects = self.find_by_id(pk_id)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("DELETE FROM swap_transactions WHERE pk_id = %s")
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
        created_at = rs[1]
        solicitude_1_pk = rs[2]
        solicitude_2_pk = rs[3]
        dump = SwapTransactionDump(pk_id, created_at, solicitude_1_pk, solicitude_2_pk)
        return dump