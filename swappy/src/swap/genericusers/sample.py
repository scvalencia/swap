'''
    {'offerants' :
        [
            {
                'user-login' : '', 
                'offerant_type' : '', 
                'portfolio' : 
                    {
                        'id' : '',
                        'risk' : '',
                        'vals' :
                            [
                                {
                                    'id' : '',
                                    'name' : '',
                                    'description' : '',
                                    'type' : '',
                                    'amount' : '',
                                    'price' : '',
                                    'rent' :
                                        {
                                            'id' : '',
                                            'name' : '',
                                            'description' : '',
                                            'function' : '',
                                            'length' : '',
                                            'type' : '',
                                            'offerant_login' : ''
                                        }
                                }
                            ]
                    }
             }
         ]
    } 
'''

# Si es passive, incluir inversionistas, portafolios
# valores en negociacion, solicitudes y transacciones
# y portafolio.

'''
    {'passives':
        [  
            {
                'passive_register':
                'user_login':
                'investors':
                    {
                        ...
                    }
                'solicitudes':
                    [

                    ],
                'transactions':
                    [

                    ],
            },
        ]
    }
'''