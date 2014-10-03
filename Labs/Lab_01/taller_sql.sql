/**############################# PUNTO 8 #################################**/
SELECT bebedores.NOMBRE,
bar.NOMBRE,
freq.FECHA_ULTIMA_VISITA
FROM PARRANDEROS.BEBEDORES bebedores,
PARRANDEROS.BARES bar,
PARRANDEROS.FRECUENTAN freq
WHERE bebedores.ID = freq.ID_BEBEDOR
AND freq.ID_BAR = bar.ID
AND bebedores.PRESUPUESTO >= bar.PRESUPUESTO
AND bar.CANT_SEDES >= 2
ORDER BY freq.FECHA_ULTIMA_VISITA ASC, bebedores.NOMBRE;
/**######################### FIN PUNTO 8 #################################**/