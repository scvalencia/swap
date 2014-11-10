SELECT SOLICITUDE, VAL, VAL_TYPE, CREATED_AT, ACTIVE_LOGIN, PASSIVE_REGISTER, USER_LOGIN, RENT_TYPE 
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
	NOT(
	val = 7617612432630759234 AND 
	VAL_TYPE = '0' AND 
	RENT_TYPE = '1' AND
  	ACTIVE_LOGIN = 'cloWoo' AND
  	(PASSIVE_REGISTER = 19193 OR USER_LOGIN = 'hanosi'));