import timeTracker
from django.db import connection
# '2014-12-07'
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

def main():
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


main()