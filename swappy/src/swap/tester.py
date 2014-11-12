import timeTracker, pygal
from django.db import connection
from tabulate import tabulate
from termcolor import colored
import plotly.plotly as py
from plotly.graph_objs import *

def R1(value, val_type, rent_type, active_login, passive_login, date1, date2):
	query = ''' SELECT SOLICITUDE, VAL, VAL_TYPE, CREATED_AT, ACTIVE_LOGIN, PASSIVE_REGISTER, USER_LOGIN, RENT_TYPE 
				FROM
					(
						SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVE_LOGIN, PASSIVES.PASSIVE_REGISTER, USER_LOGIN 
						FROM  
							(
								SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVESPASSIVES.ACTIVE_LOGIN, PASSIVE_REGISTER
								FROM
									(
										SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVE_LOGIN  
										FROM
											(
												SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVE_LOGIN 
												FROM 
													(
														SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID
														FROM
														(
															SOLICITUDES_VAL INNER JOIN VALS 
															ON VALS.PK_ID = SOLICITUDES_VAL.VAL
														)
													) 
												SOLICITUDES_INFO INNER JOIN SOLICITUDES 
												ON SOLICITUDES_INFO.SOLICITUDE = SOLICITUDES.PK_ID
											) 
										INFO1 INNER JOIN ACTIVES 
										ON INFO1.ACTIVE_LOGIN = ACTIVES.USER_LOGIN
									) 
								INFO2 INNER JOIN ACTIVESPASSIVES 
								ON ACTIVESPASSIVES.ACTIVE_LOGIN = INFO2.ACTIVE_LOGIN
							) 
						INFO3 INNER JOIN PASSIVES 
						ON PASSIVES.PASSIVE_REGISTER = INFO3.PASSIVE_REGISTER
					) 
				INFO4 INNER JOIN RENTS 
				ON INFO4.RENT_ID = RENTS.PK_ID
				WHERE	
					val = %s AND 
					VAL_TYPE = %s AND 
					RENT_TYPE = %s AND
				  	ACTIVE_LOGIN = %s AND
				  	USER_LOGIN = %s AND 
				  	CREATED_AT >= TO_TIMESTAMP(%s,'yyyy-mm-dd') AND 
				  	CREATED_AT < TO_TIMESTAMP(%s,'yyyy-mm-dd')
		'''
	params = [value, val_type, rent_type, active_login, passive_login, date1, date2]
	cursor = connection.cursor()
	cursor.execute(query, params)

def R2(value, val_type, rent_type, active_login, passive_login, date1, date2):
	query = ''' SELECT SOLICITUDE, VAL, VAL_TYPE, CREATED_AT, ACTIVE_LOGIN, PASSIVE_REGISTER, USER_LOGIN, RENT_TYPE 
				FROM
					(
						SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVE_LOGIN, PASSIVES.PASSIVE_REGISTER, USER_LOGIN 
						FROM  
							(
								SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVESPASSIVES.ACTIVE_LOGIN, PASSIVE_REGISTER
								FROM
									(
										SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVE_LOGIN  
										FROM
											(
												SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID, CREATED_AT, ACTIVE_LOGIN 
												FROM 
													(
														SELECT SOLICITUDE, VAL, VAL_TYPE, RENT_ID
														FROM
														(
															SOLICITUDES_VAL INNER JOIN VALS 
															ON VALS.PK_ID = SOLICITUDES_VAL.VAL
														)
													) 
												SOLICITUDES_INFO INNER JOIN SOLICITUDES 
												ON SOLICITUDES_INFO.SOLICITUDE = SOLICITUDES.PK_ID
											) 
										INFO1 INNER JOIN ACTIVES 
										ON INFO1.ACTIVE_LOGIN = ACTIVES.USER_LOGIN
									) 
								INFO2 INNER JOIN ACTIVESPASSIVES 
								ON ACTIVESPASSIVES.ACTIVE_LOGIN = INFO2.ACTIVE_LOGIN
							) 
						INFO3 INNER JOIN PASSIVES 
						ON PASSIVES.PASSIVE_REGISTER = INFO3.PASSIVE_REGISTER
					) 
				INFO4 INNER JOIN RENTS 
				ON INFO4.RENT_ID = RENTS.PK_ID
				WHERE	
					val = %s AND 
					VAL_TYPE = %s AND 
					RENT_TYPE = %s AND
  					ACTIVE_LOGIN = %s AND
  					USER_LOGIN = %s AND 
				  	CREATED_AT >= TO_TIMESTAMP(%s,'yyyy-mm-dd') AND 
				  	CREATED_AT < TO_TIMESTAMP(%s,'yyyy-mm-dd')
		'''
	params = [value, val_type, rent_type, active_login, passive_login, date1, date2]
	cursor = connection.cursor()
	cursor.execute(query, params)

def R3(val_type, bound):
	query = str(''' SELECT * 
					FROM 
					(
						SELECT * 
						FROM
							(
								SELECT * 
								FROM
						    		(
						    			(
						    				SELECT val, COUNT(val) AS Frequency 
						    			 	FROM SOLICITUDES_VAL 
						    				GROUP BY val 
						    				ORDER BY COUNT(val) DESC
						    			) 
						    			FREQ INNER JOIN VALS 
						    			ON FREQ.val = VALS.PK_ID
						    		)   
								WHERE VAL_TYPE = %s AND FREQUENCY > %s
							) 
							VALORES INNER JOIN PORTFOLIOS_VALS
				    		ON VALORES.VAL = PORTFOLIOS_VALS.PK_VAL
				    ) 
				    PORTFOLIO_INFO INNER JOIN PORTFOLIOS
					ON PK_PORTFOLIO = PK_ID 
			''')
	params = [val_type, bound]
	cursor = connection.cursor()
	cursor.execute(query, params)

def R4(val_id):
	query = ''' SELECT * 
				FROM
					(
						SELECT PK_PORTFOLIO 
						FROM 
						PORTFOLIOS_VALS INNER JOIN VALS 
						ON PORTFOLIOS_VALS.PK_VAL = VALS.PK_ID 
						WHERE PK_VAL = %s
					) 
				INFO INNER JOIN PORTFOLIOS 
				ON INFO.PK_PORTFOLIO = PORTFOLIOS.PK_ID
			'''
	params = [val_id]
	cursor = connection.cursor()
	cursor.execute(query, params)

def time():
	t = timeTracker.TimeController(R1, 7617612432630759234, '0', '1', 'cloWoo', 'hanosi', '2014-11-05', '2014-12-07')
	R1(7617612432630759234, '0', '1', 'cloWoo', 'hanosi', '2014-11-05', '2014-12-07')
	print t
	t = timeTracker.TimeController(R1, 7617612432630759234, '0', '0', 'cloWoo', 'hanosi', '2014-10-05', '2014-12-07')
	R1(7617612432630759234, '0', '1', 'cloWoo', 'hanosi', '2014-11-05', '2014-12-07')
	print t
	t = timeTracker.TimeController(R2, 7617612432630759234, '0', '1', 'cloWoo', 'hanosi', '2014-11-05', '2014-12-07')
	R2(7617612432630759234, '0', '1', 'cloWoo', 'hanosi', '2014-11-05', '2014-12-07')
	print t
	t = timeTracker.TimeController(R2, 7617612432630759234, '0', '0', 'cloWoo', 'hanosi', '2014-10-05', '2014-12-07')
	R2(7617612432630759234, '0', '1', 'cloWoo', 'hanosi', '2014-11-05', '2014-12-07')
	print t

	t = timeTracker.TimeController(R3, '0', '4')
	R3('0', 4)
	print t
	t = timeTracker.TimeController(R3, '0', '1')
	R3('0', 4)
	print t
	t = timeTracker.TimeController(R3, '1', '4')
	R3('0', 4)
	print t
	t = timeTracker.TimeController(R3, '1', '4')
	R3('0', 4)
	print t
	t = timeTracker.TimeController(R3, '0', '889')
	R3('0', 4)
	print t

	t = timeTracker.TimeController(R4, '9810102381089460792')
	R3('0', 4)
	print t

def stats(number):
	from django.db import connection
	import random

	values_distribution_query = ''' SELECT VAL, COUNT(VAL) AS FREQ 
									FROM SOLICITUDES_VAL 
									GROUP BY VAL ORDER BY COUNT(VAL) ASC
							    '''

	actives_distribution_query = ''' SELECT ACTIVE_LOGIN, COUNT(ACTIVE_LOGIN) AS FREQ 
									 FROM SOLICITUDES 
									 GROUP BY ACTIVE_LOGIN ORDER BY COUNT(ACTIVE_LOGIN) ASC
								 '''

	passives_distribution_query = ''' SELECT USER_LOGIN AS PASSIVE_LOGIN, FREQ
									  FROM
										(
											SELECT PASSIVE_REGISTER, COUNT(PASSIVE_REGISTER) AS FREQ 
											FROM ACTIVESPASSIVES 
											GROUP BY PASSIVE_REGISTER ORDER BY COUNT(PASSIVE_REGISTER) ASC
										) 
									  REGISTERS INNER JOIN PASSIVES
									  ON REGISTERS.PASSIVE_REGISTER = PASSIVES.PASSIVE_REGISTER
								  '''

	values_on_portfolio_query = ''' SELECT PK_VAL, COUNT(PK_VAL) AS FREQ 
								    FROM PORTFOLIOS_VALS 
									GROUP BY PK_VAL ORDER BY COUNT(PK_VAL) ASC
								'''

	cursor = connection.cursor()

	cursor.execute(values_distribution_query)
	values_freqs = [(_[0], _[1]) for _ in cursor.fetchall()]

	cursor.execute(actives_distribution_query)
	actives_freqs = [(_[0].encode('utf-8'), _[1]) for _ in cursor.fetchall()]

	cursor.execute(passives_distribution_query)
	passives_freqs = [(_[0].encode('utf-8'), _[1]) for _ in cursor.fetchall()]

	cursor.execute(values_on_portfolio_query)
	values_ion_portfolio = [(_[0], _[1]) for _ in cursor.fetchall()]

	def stats_R1():
		values = [random.choice(values_freqs) for _ in range(20)]
		value_types = [random.choice(['0', '1']) for _ in range(20)]
		rent_types = [random.choice(['0', '1']) for _ in range(20)]
		active_logins = [random.choice(actives_freqs) for _ in range(20)]
		passive_logins = [random.choice(passives_freqs) for _ in range(20)]
		dates = sorted([random_date() for _ in range(20)])
		dates_1 = dates[0:10]
		dates_2 = dates[10:]

		items = [[] for _ in range(20)]

		i = 0
		for counter in range(20):
			itm = values[counter]
			items[i].append(itm[0])
			items[i].append(itm[1])
			items[i].append(value_types[counter])
			items[i].append(rent_types[counter])
			itm = active_logins[counter]
			items[i].append(itm[0])
			items[i].append(itm[1])
			itm = passive_logins[counter]
			items[i].append(itm[0])
			items[i].append(itm[1])
			items[i].append(dates_1[i % 10])
			items[i].append(dates_2[i % 10])
			i += 1

		arguments = [[] for _ in range(20)]
		i = 0
		for itm in items:
			arguments[i].append(itm[0])
			arguments[i].append(itm[2])
			arguments[i].append(itm[3])
			arguments[i].append(itm[4])
			arguments[i].append(itm[6])
			arguments[i].append(itm[8])
			arguments[i].append(itm[9])
			i += 1

		arguments = map(tuple, arguments)
		max_time = (0.0, 0)
		times = []
		i = 0
		for _ in arguments:
			value = _[0]
			val_type = _[1] 
			rent_type = _[2] 
			active_login = _[3]
			passive_login = _[4]
			date1 = _[5]
			date2 = _[6]
			t = timeTracker.TimeController(R1)
			R1(value, val_type, rent_type, active_login, passive_login, date1, date2)
			time = t.get_elased_time()
			if time > max_time[0]:
				max_time = time, i
			times.append(time)
			items[i].append(time)
			i += 1

		headers = ["id_value", "freq", "value_type", "rent_type", "active_login", 
				   "freq", "passive_login", "freq", "date1", "date2", "time"]

		table = [[] for _ in range(20)]

		i = 0
		min_time = min(times)
		index = times.index(min_time)
		for itm in items:
			if i == max_time[1]:
				table[i].append(colored(itm[0], 'green'))
				table[i].append(colored(itm[1], 'green'))
				table[i].append(colored(itm[2], 'green'))
				table[i].append(colored(itm[3], 'green'))
				table[i].append(colored(itm[4], 'green'))
				table[i].append(colored(itm[5], 'green'))
				table[i].append(colored(itm[6], 'green'))
				table[i].append(colored(itm[7], 'green'))
				table[i].append(colored(itm[8], 'green'))
				table[i].append(colored(itm[9], 'green'))
				#table[i].append(colored(itm[10], 'green'))
				table[i].append(itm[10])
				#table[i].append(colored(itm[11], 'green'))
			elif i == index:
				table[i].append(colored(itm[0], 'red'))
				table[i].append(colored(itm[1], 'red'))
				table[i].append(colored(itm[2], 'red'))
				table[i].append(colored(itm[3], 'red'))
				table[i].append(colored(itm[4], 'red'))
				table[i].append(colored(itm[5], 'red'))
				table[i].append(colored(itm[6], 'red'))
				table[i].append(colored(itm[7], 'red'))
				table[i].append(colored(itm[8], 'red'))
				table[i].append(colored(itm[9], 'red'))
				#table[i].append(colored(itm[10], 'green'))
				table[i].append(itm[10])
			else:
				table[i] = map(str, itm)
			i += 1


		print tabulate(table, headers, tablefmt="grid")

	def stats_R2():
		values = [random.choice(values_freqs) for _ in range(20)]
		value_types = [random.choice(['0', '1']) for _ in range(20)]
		rent_types = [random.choice(['0', '1']) for _ in range(20)]
		active_logins = [random.choice(actives_freqs) for _ in range(20)]
		passive_logins = [random.choice(passives_freqs) for _ in range(20)]
		dates = sorted([random_date() for _ in range(20)])
		dates_1 = dates[0:10]
		dates_2 = dates[10:]

		items = [[] for _ in range(20)]

		i = 0
		for counter in range(20):
			itm = values[counter]
			items[i].append(itm[0])
			items[i].append(itm[1])
			items[i].append(value_types[counter])
			items[i].append(rent_types[counter])
			itm = active_logins[counter]
			items[i].append(itm[0])
			items[i].append(itm[1])
			itm = passive_logins[counter]
			items[i].append(itm[0])
			items[i].append(itm[1])
			items[i].append(dates_1[i % 10])
			items[i].append(dates_2[i % 10])
			i += 1

		arguments = [[] for _ in range(20)]
		i = 0
		for itm in items:
			arguments[i].append(itm[0])
			arguments[i].append(itm[2])
			arguments[i].append(itm[3])
			arguments[i].append(itm[4])
			arguments[i].append(itm[6])
			arguments[i].append(itm[8])
			arguments[i].append(itm[9])
			i += 1

		arguments = map(tuple, arguments)
		max_time = (0.0, 0)
		times = []
		i = 0
		for _ in arguments:
			value = _[0]
			val_type = _[1] 
			rent_type = _[2] 
			active_login = _[3]
			passive_login = _[4]
			date1 = _[5]
			date2 = _[6]
			t = timeTracker.TimeController(R1)
			R1(value, val_type, rent_type, active_login, passive_login, date1, date2)
			time = t.get_elased_time()
			if time > max_time[0]:
				max_time = time, i
			times.append(time)
			items[i].append(time)
			i += 1

		headers = ["id_value", "freq", "value_type", "rent_type", "active_login", 
				   "freq", "passive_login", "freq", "date1", "date2", "time"]

		table = [[] for _ in range(20)]

		i = 0
		min_time = min(times)
		index = times.index(min_time)
		for itm in items:
			if i == max_time[1]:
				table[i].append(colored(itm[0], 'green'))
				table[i].append(colored(itm[1], 'green'))
				table[i].append(colored(itm[2], 'green'))
				table[i].append(colored(itm[3], 'green'))
				table[i].append(colored(itm[4], 'green'))
				table[i].append(colored(itm[5], 'green'))
				table[i].append(colored(itm[6], 'green'))
				table[i].append(colored(itm[7], 'green'))
				table[i].append(colored(itm[8], 'green'))
				table[i].append(colored(itm[9], 'green'))
				#table[i].append(colored(itm[10], 'green'))
				table[i].append(itm[10])
				#table[i].append(colored(itm[11], 'green'))
			elif i == index:
				table[i].append(colored(itm[0], 'red'))
				table[i].append(colored(itm[1], 'red'))
				table[i].append(colored(itm[2], 'red'))
				table[i].append(colored(itm[3], 'red'))
				table[i].append(colored(itm[4], 'red'))
				table[i].append(colored(itm[5], 'red'))
				table[i].append(colored(itm[6], 'red'))
				table[i].append(colored(itm[7], 'red'))
				table[i].append(colored(itm[8], 'red'))
				table[i].append(colored(itm[9], 'red'))
				#table[i].append(colored(itm[10], 'green'))
				table[i].append(itm[10])
			else:
				table[i] = map(str, itm)
			i += 1


		print tabulate(table, headers, tablefmt="grid")

	def stats_R3():
		value_types = [random.choice(['0', '1']) for _ in range(20)]
		bounds = [random.choice(range(19)) for _ in range(20)]

		items = [[] for _ in range(20)]
		i = 0
		for counter in range(20):
			items[counter].append(value_types[i])
			items[counter].append(bounds[i])
			i += 1

		arguments = [[] for _ in range(20)]
		i = 0
		for itm in items:
			arguments[i].append(itm[0])
			arguments[i].append(itm[1])
			i += 1

		arguments = map(tuple, arguments)
		max_time = (0.0, 0)
		times = []
		i = 0
		for _ in arguments:
			val_type = _[0]
			bound = _[1]
			t = timeTracker.TimeController(R3)
			R3(val_type, bound)
			time = t.get_elased_time()
			if time > max_time[0]:
				max_time = time, i
			times.append(time)
			items[i].append(time)
			i += 1

		headers = ["value_Type", "bound", "time"]

		table = [[] for _ in range(20)]

		i = 0
		min_time = min(times)
		index = times.index(min_time)
		for itm in items:
			if i == max_time[1]:
				table[i].append(colored(itm[0], 'green'))
				table[i].append(colored(itm[1], 'green'))
				table[i].append(itm[2])
			elif i == index:
				table[i].append(colored(itm[0], 'red'))
				table[i].append(colored(itm[1], 'red'))
				table[i].append(itm[2])
			else:
				table[i] = map(str, itm)
			i += 1

		print tabulate(table, headers, tablefmt="grid")

	def stats_R4():
		values = [random.choice(values_freqs) for _ in range(20)]

		items = [[] for _ in range(20)]
		i = 0
		for counter in range(20):
			items[counter].append(values[i][0])
			items[counter].append(values[i][1])
			i += 1

		arguments = [[] for _ in range(20)]
		i = 0
		for itm in items:
			arguments[i].append(itm[0])
			i += 1

		arguments = map(tuple, arguments)
		max_time = (0.0, 0)
		times = []
		i = 0
		for _ in arguments:
			val = _[0]
			t = timeTracker.TimeController(R4)
			R4(val)
			time = t.get_elased_time()
			if time > max_time[0]:
				max_time = time, i
			times.append(time)
			items[i].append(time)
			i += 1

		headers = ["value_ID", "freq", "time"]

		table = [[] for _ in range(20)]

		i = 0
		min_time = min(times)
		index = times.index(min_time)
		for itm in items:
			if i == max_time[1]:
				table[i].append(colored(itm[0], 'green'))
				table[i].append(colored(itm[1], 'green'))
				table[i].append(itm[2])
			elif i == index:
				table[i].append(colored(itm[0], 'red'))
				table[i].append(colored(itm[1], 'red'))
				table[i].append(itm[2])
			else:
				table[i] = map(str, itm)
			i += 1

		print tabulate(table, headers, tablefmt="grid")

	def random_date():
		ans = ''
		ans += '2014-'
		ans += str(random.choice(range(11, 12)))
		ans += '-' + random.choice(['04', '05', '06', '07', '08', '09', '10', '11', '12'])
		return ans

	def printer(collection):
		for itm in collection:
			print 'sds'
			print itm
	

	def distribution_analysis(number):
		number = (number % 5)
		if number < 2:
			stats_R1()
		elif number == 2:
			stats_R2()
		elif number == 3:
			stats_R3()
		else:
			stats_R4()

	distribution_analisis(number)


stats(1)