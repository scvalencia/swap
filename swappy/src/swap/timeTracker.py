from termcolor import colored
import time

class TimeController(object):

	def __init__(self, fnc, *args):
		self.start_time = time.time()
		self.executor = fnc
		self.arguments = args

	def get_elased_time(self):
		elapsed_time = time.time() - self.start_time
		return elapsed_time

	def prettifier(self, args):
		ans = ''
		if len(args) == 1:
			ans = '(' + str(args[0]) + ')'
		else:
			ans = str(args)

		return ans

	def header(self):
		ans = '\n'
		line = '*' * 100
		for i in range(4):
			ans += colored(line + '\n', 'green')
		return ans

	def __str__(self):
		title = '=' * 100
		function_name = self.executor.__name__
		args = self.prettifier(self.arguments)
		timer = str(self.get_elased_time())
		ans = colored(title, 'green') + self.header()
		ans += colored('ELAPSED TIME OF ' + function_name, 'green')
		ans += colored(args + ' IS ' + timer, 'green')
		ans += colored(' SECONDS', 'green')
		#ans = colored(title + '\n' + ans, 'green')
		#ans += colored('\n' + title, 'green')

		ans += self.header()
		ans += colored(title, 'green')
		
		return ans

def main():

	def tester(bound):
		ans = 0
		for i in range(bound):
			ans += i
		return ans

	t = TimeController(tester, 10)
	tester(10)
	print t

if __name__ == '__main__':
	main()
