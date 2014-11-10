SELECT * 
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
				WHERE VAL_TYPE = '0' AND FREQUENCY > 1
			) 
			VALORES INNER JOIN PORTFOLIOS_VALS
    		ON VALORES.VAL = PORTFOLIOS_VALS.PK_VAL
    ) 
    PORTFOLIO_INFO INNER JOIN PORTFOLIOS
	ON PK_PORTFOLIO = PK_ID; 