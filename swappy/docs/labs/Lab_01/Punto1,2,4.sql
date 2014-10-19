/**############################# PUNTO 1 #################################**/
SELECT query_1.NombreTabla AS NombreTabla,
NVL(query_2.NumColumnas, 0) AS NumColumnas,
NVL(query_3.NumColsPK, 0) AS NumColsPK,
NVL(query_4.NumColsNotNull, 0) AS NumColsNotNull,
NVL(query_5.NumColsFKs, 0) AS NumColsFKs
FROM (
    /** Returns all table names**/
    SELECT a_t.TABLE_NAME AS NombreTabla
    FROM ALL_TABLES a_t
    WHERE a_t.OWNER = 'PARRANDEROS'
    GROUP BY a_t.TABLE_NAME
) query_1
LEFT OUTER JOIN (
    /** Returns table names with their column numbers **/
    SELECT a_t_c.TABLE_NAME AS NombreTabla,
    COUNT(a_t_c.COLUMN_NAME) AS NumColumnas
    FROM ALL_TAB_COLUMNS a_t_c
    WHERE a_t_c.OWNER = 'PARRANDEROS'
    GROUP BY a_t_c.TABLE_NAME
) query_2
ON query_1.NombreTabla=query_2.NombreTabla
LEFT OUTER JOIN (
    /** Returns table names with their PK column numbers **/
    SELECT a_c.TABLE_NAME AS NombreTabla,
    COUNT(a_c.CONSTRAINT_NAME) AS NumColsPK
    FROM ALL_CONSTRAINTS a_c
    WHERE a_c.OWNER = 'PARRANDEROS'
    AND a_c.CONSTRAINT_NAME LIKE 'PK%'
    GROUP BY a_c.TABLE_NAME
) query_3
ON query_2.NombreTabla=query_3.NombreTabla
LEFT OUTER JOIN (
    /** Returns table names with not null requirement **/
    SELECT a_t_c.TABLE_NAME AS NombreTabla,
    COUNT(a_t_c.COLUMN_NAME) AS NumColsNotNull
    FROM ALL_TAB_COLUMNS a_t_c
    WHERE a_t_c.OWNER = 'PARRANDEROS'
    AND a_t_c.NULLABLE = 'N'
    GROUP BY a_t_c.TABLE_NAME
) query_4
ON query_3.NombreTabla=query_4.NombreTabla
LEFT OUTER JOIN (
    /** Returns table names with their FK column numbers **/
    SELECT a_c.TABLE_NAME AS NombreTabla,
    COUNT(a_c.CONSTRAINT_NAME) AS NumColsFKs
    FROM ALL_CONSTRAINTS a_c
    WHERE a_c.OWNER = 'PARRANDEROS'
    AND a_c.CONSTRAINT_NAME LIKE 'FK%'
    GROUP BY a_c.TABLE_NAME
) query_5
ON query_4.NombreTabla=query_5.NombreTabla
ORDER BY NombreTabla DESC;
/**######################### FIN PUNTO 1 #################################**/


/**############################# PUNTO 2 #################################**/
SELECT query_1.NombreTabla AS NombreTabla,
query_2.TipoDataCol AS TipoDatoCol,
NVL(query_3.NumRestriccionesColsTipoDato, 0) AS NumRestriccionesColsTipoDato,
NVL(query_4.NumColsConEseTipoDeDato, 0) AS NumColsConEseTipoDeDato
FROM (
    /** Returns all table names**/
    SELECT a_t.TABLE_NAME AS NombreTabla
    FROM ALL_TABLES a_t
    WHERE a_t.OWNER = 'PARRANDEROS'
    GROUP BY a_t.TABLE_NAME
) query_1
LEFT OUTER JOIN (
    /** Returns all table names with their data types **/
    SELECT DISTINCT a_t_c.TABLE_NAME AS NombreTabla,
    a_t_c.DATA_TYPE AS TipoDataCol
    FROM ALL_TAB_COLUMNS a_t_c
    WHERE a_t_c.OWNER = 'PARRANDEROS'
) query_2
ON query_1.NombreTabla = query_2.NombreTabla
LEFT OUTER JOIN (
    /** Returns all table names with their data types and their restriction **/
    SELECT a_c_c.TABLE_NAME AS NombreTabla,
    a_t_c.DATA_TYPE AS TipoDataCol,
    COUNT(a_c_c.CONSTRAINT_NAME) AS NumRestriccionesColsTipoDato
    FROM ALL_CONS_COLUMNS a_c_c,
    ALL_TAB_COLUMNS a_t_c
    WHERE a_c_c.OWNER = 'PARRANDEROS'
    AND a_c_c.OWNER = a_t_c.OWNER
    AND a_c_c.TABLE_NAME = a_t_c.TABLE_NAME
    AND a_c_c.COLUMN_NAME = a_t_c.COLUMN_NAME
    GROUP BY a_c_c.TABLE_NAME, a_t_c.DATA_TYPE
) query_3
ON query_2.NombreTabla = query_3.NombreTabla
AND query_2.TipoDataCol = query_3.TipoDataCol
LEFT OUTER JOIN (
    /** Returns all table names with their data types and their column nums **/
    SELECT a_t_c.TABLE_NAME AS NombreTabla,
    a_t_c.DATA_TYPE AS TipoDataCol,
    COUNT(a_t_c.DATA_TYPE) AS NumColsConEseTipoDeDato
    FROM ALL_TAB_COLUMNS a_t_c
    WHERE a_t_c.OWNER = 'PARRANDEROS'
    GROUP BY a_t_c.TABLE_NAME, a_t_c.DATA_TYPE
) query_4
ON query_3.NombreTabla = query_4.NombreTabla
AND query_3.TipoDataCol = query_4.TipoDataCol
ORDER BY NombreTabla ASC, TipoDatoCol ASC;
/**######################### FIN PUNTO 2 #################################**/


/**############################# PUNTO 3 #################################**/

/**######################### FIN PUNTO 3 #################################**/


/**############################# PUNTO 4 #################################**/
SELECT query_1.NombreTabla AS NombreTabla,
query_2.NombreCol AS NombreCol,
query_3.NombreConstraintColumna AS NombreConstraintColumna
/**query_4.NombreTablaRefFK AS NombreTablaRefFK**/
FROM (
    /** Returns all table names**/
    SELECT a_t.TABLE_NAME AS NombreTabla
    FROM ALL_TABLES a_t
    WHERE a_t.OWNER = 'PARRANDEROS'
    GROUP BY a_t.TABLE_NAME
) query_1
LEFT OUTER JOIN (
    /** Returns all table names with their columns **/
    SELECT a_t_c.TABLE_NAME AS NombreTabla,
    a_t_c.COLUMN_NAME AS NombreCol
    FROM ALL_TAB_COLUMNS a_t_c
    WHERE a_t_c.OWNER = 'PARRANDEROS'
) query_2
ON query_1.NombreTabla = query_2.NombreTabla;
    
/**######################### FIN PUNTO 4 #################################**/