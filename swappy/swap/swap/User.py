ALLOWED_USERS = {'ISIS2304361420' : 'sc.valencia', 'ISIS2304031420' : 'jc.bages'}

class User(object):
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def __str__(self):
		ans = ''
		ans += self.username + ' : '
		name = ALLOWED_USERS[self.username]
		ans += name
		return ans