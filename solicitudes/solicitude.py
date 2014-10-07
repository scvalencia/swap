class Solicitude(object):
    def __init__(self, pk_id, operation_type, val, 
                quantity, quantity_type, time_created, 
                active_login, solved, is_active):
        self.pk_id = pk_id
        self.operation_type = 'Comprar' if operation_type == 1 else 'Vender' # 1-> COMPRAR, 2 -> VENDER
        self.val = val # clase valor
        self.quantity = quantity
        self.quantity_type = 'Pesos' if quantity_type == 1 else 'Unidades' # Peso/unidades
        self.time_created = time_created # fecha de creacion
        self.active_login = active_login # Quien creo solicitud
        self.solved = solved # Estado Boolean
        self.is_active = is_active # Boolean