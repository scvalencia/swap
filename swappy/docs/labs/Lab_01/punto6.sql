/* Número específico */
SELECT query_1.NombreBebida, query_1.TipoBebida
FROM(
   SELECT
     Bebidas.NOMBRE AS NombreBebida,
     TipoBebida.NOMBRE AS TipoBebida,
     Bebidas.GRADO_ALCOHOL AS GradoAlcohol
 	 FROM(
		PARRANDEROS.BEBIDAS Bebidas
		INNER JOIN
		PARRANDEROS.TIPO_BEBIDA TipoBebida
		ON
		Bebidas.TIPO = TipoBebida.ID
		)
	) query_1
WHERE query_1.GradoAlcohol = 12
ORDER BY NombreBebida, TipoBebida DESC;


/* Máximo grado de alcohol */                  
SELECT query_1.NombreBebida, query_1.TipoBebida
FROM(
   SELECT
     Bebidas.NOMBRE AS NombreBebida,
     TipoBebida.NOMBRE AS TipoBebida,
     Bebidas.GRADO_ALCOHOL AS GradoAlcohol
 	 FROM(
		PARRANDEROS.BEBIDAS Bebidas
		INNER JOIN
		PARRANDEROS.TIPO_BEBIDA TipoBebida
		ON
		Bebidas.TIPO = TipoBebida.ID
		)
	) query_1
WHERE query_1.GradoAlcohol = (SELECT MAX(PARRANDEROS.BEBIDAS.GRADO_ALCOHOL) 
						      FROM PARRANDEROS.BEBIDAS)
ORDER BY NombreBebida, TipoBebida DESC;