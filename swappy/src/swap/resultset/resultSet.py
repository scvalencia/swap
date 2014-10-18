class ResultSet(object):
	def __init__(self):
		self.result_set = []

	def set(self, lst):
		self.result_set = lst

	def __str__(self):
		strings = map(str, self.result_set)
		ans = '['
		ans += ', '.join(strings)
		ans += ']'
		return ans