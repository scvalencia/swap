class Passive(object):
    def __init__(self, login, register):
        self.login = login
        self.register = register

    def __hash__(self):
    	return self.login