from django.db import connection
from models import ValDump
from models import RentDump
from resultset.resultSet import ResultSet 

class RentDao(object):

    def __init__(self):
        self.table_name = 'rents'
        self.schema = ('pk_id', 'rent_name', 'description', 'rent_function', 
            'rent_length', 'rent_type', 'offerant_login')
        self.cursor = connection.cursor()
        self.rs = ResultSet()

    def find_all(self, test = False):
        ans = []
        if not test:
            try:            
                query = "SELECT * FROM rents ORDER BY pk_id"
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

    def find_by_id(self, pk_id, test = False):
        pk_id = str(pk_id)
        ans = []
        if not test:
            try:
                query = "SELECT * FROM rents WHERE pk_id = %s"
                params = [pk_id]
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
    
    def insert(self, pk_id, rent_name, desc, rent_function, 
        rent_len, rent_tp, login, test = False):
        params = [pk_id, rent_name, desc, rent_function, rent_len, rent_tp, login]
        params = map(str, params)
        if not test:
            try:
                query = "INSERT INTO rents VALUES(%s, %s, %s, %s, %s, %s, %s)"
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

    def update(self, arg_object, test = False):
        pk_id = arg_object.pk_id
        rent_name = arg_object.rent_name
        desc = arg_object.description
        rent_function = arg_object.rent_function
        rent_len = arg_object.rent_length
        rent_tp = arg_object.rent_type
        login = arg_object.offerant_login
        objects = self.find_by_id(pk_id)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("UPDATE rents "
                             "SET rent_name = %s, description = %s, "
                             "rent_function = %s, rent_length = %s, rent_type = %s, "
                             "offerant_login = %s WHERE pk_id = %s")
                    params = [rent_name, desc, rent_function, rent_len, rent_tp, login, pk_id]
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

    def remove(self, pk_id, test = False):
        pk_id = str(pk_id)
        objects = self.find_by_id(pk_id)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("DELETE FROM rents WHERE pk_id = %s")
                    params = [pk_id]
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

    def process_row(self, result_set):
        pk_id = result_set[0]
        rent_name = result_set[1] 
        desc = result_set[2] 
        rent_function = result_set[3] 
        rent_len = result_set[4] 
        rent_tp = result_set[5] 
        login = result_set[6]
        dump = RentDump(pk_id, rent_name, desc, rent_function, rent_len, rent_tp, login)
        return dump

class ValDao(object):

    def __init__(self):
        self.table_name = 'vals'
        self.schema = ('pk_id', 'val_name', 'description', 'val_type', 
            'amount', 'price', 'rent_id')
        self.cursor = connection.cursor()
        self.rs = ResultSet()

    def find_all(self, test = False):
        ans = []
        if not test:
            try:            
                query = "SELECT * FROM vals ORDER BY pk_id"
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

    def find_by_id(self, pk_id, test = False):
        pk_id = str(pk_id)
        ans = []
        if not test:
            try:
                query = "SELECT * FROM vals WHERE pk_id = %s"
                params = [pk_id]
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
    
    def insert(self, pk, name, desc, val_type, amount, price, rent_id, test = False):
        params = [int(pk), str(name), str(desc), str(val_type), int(amount), 
        str(price), str(rent_id)]
        if not test:
            try:
                query = "INSERT INTO vals VALUES(%s, %s, %s, %s, %s, %s, %s)"
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

    def update(self, arg_object, test = False):
        pk_id = int(arg_object.pk_id)
        val_name = arg_object.val_name
        description = arg_object.description
        val_type = arg_object.val_type
        amount = int(arg_object.amount)
        price = arg_object.price
        rent_id = arg_object.rent_id
        objects = self.find_by_id(pk_id)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("UPDATE vals "
                             "SET val_name = %s, description = %s, val_type = %s, amount = %s, "
                             "price = %s, rent_id = %s WHERE pk_id = %s")
                    params = [val_name, description, val_type, amount, price, rent_id, pk_id]
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

    def remove(self, pk_id, test = False):
        pk_id = str(pk_id)
        objects = self.find_by_id(pk_id)
        available_for_update = (len(objects) == 1)
        if(available_for_update):
            if not test:
                try:
                    query = ("DELETE FROM vals WHERE pk_id = %s")
                    params = [pk_id]
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

    def process_row(self, rs):
        pk_id = rs[0]
        val_name = rs[1]
        description = rs[2]
        val_type = rs[3]
        amount = rs[4]
        price = rs[5]
        rent_id = rs[6]
        dump = ValDump(pk_id, val_name, description, val_type, amount, price, rent_id)
        return dump