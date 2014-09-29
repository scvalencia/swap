class Solicitude(object):
    def __init__(self, pk_id, operation_type, val, 
                quantity, quantity_type, time_created, 
                active_login, solved, is_active):
        self.pk_id = pk_id
        self.operation_type = operation_type
        self.val = val
        self.quantity = quantity
        self.quantity_type = quantity_type
        self.time_created = time_created
        self.active_login = active_login
        self.solved = solved
        self.is_active = is_active