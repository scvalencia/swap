/* Frequencies */
SELECT ID_BAR, COUNT(*) AS total FROM PARRANDEROS.FRECUENTAN GROUP BY ID_BAR;
/* Get minimum */
SELECT MIN(query1.total) FROM (SELECT ID_BAR, COUNT(*) AS total FROM PARRANDEROS.FRECUENTAN GROUP BY ID_BAR) query1;
/* Frequencies JOIN Bar */
SELECT * 
FROM 
  (PARRANDEROS.BARES Bares 
  INNER JOIN
  (SELECT ID_BAR, COUNT(*) AS total FROM PARRANDEROS.FRECUENTAN GROUP BY ID_BAR) inner_query
  ON Bares.ID = inner_query.ID_BAR);
/* Answer */
SELECT nameBar, cityBar, budget
FROM
  (SELECT 
          Bares.NOMBRE AS nameBar,
          Bares.CIUDAD AS cityBar,
          Bares.PRESUPUESTO AS budget,
          total
  FROM
          (PARRANDEROS.BARES Bares 
          INNER JOIN
          (SELECT ID_BAR, COUNT(*) AS total FROM PARRANDEROS.FRECUENTAN GROUP BY ID_BAR) inner_query
          ON Bares.ID = inner_query.ID_BAR) 
          ) min_query          
  WHERE min_query.total = (SELECT MIN(query1.total) FROM (SELECT ID_BAR, COUNT(*) AS total FROM PARRANDEROS.FRECUENTAN GROUP BY ID_BAR) query1) 
        AND (budget = 'Bajo' OR budget = 'Medio');
SELECT nameBar, cityBar, budget
FROM
  (SELECT 
          Bares.NOMBRE AS nameBar,
          Bares.CIUDAD AS cityBar,
          Bares.PRESUPUESTO AS budget,
          total
  FROM
          (PARRANDEROS.BARES Bares 
          INNER JOIN
          (SELECT ID_BAR, COUNT(*) AS total FROM PARRANDEROS.FRECUENTAN GROUP BY ID_BAR) inner_query
          ON Bares.ID = inner_query.ID_BAR) 
          ) min_query          
  WHERE min_query.total = (SELECT MIN(query1.total) FROM (SELECT ID_BAR, COUNT(*) AS total FROM PARRANDEROS.FRECUENTAN GROUP BY ID_BAR) query1);

