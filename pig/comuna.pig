-- Cargar los datos filtrados por Apache Pig
filtrados = LOAD 'eventos_filtrados/part-m-00000' 
             USING PigStorage(',') 
             AS (uuid:chararray, type:chararray, city:chararray, street:chararray, date:chararray, severity:int);

-- Agrupar por comuna (city)
grouped_by_city = GROUP filtrados BY city;

-- Contar incidentes por comuna
count_by_city = FOREACH grouped_by_city GENERATE group AS comuna, COUNT(filtrados) AS total;

-- Guardar salida
STORE count_by_city INTO 'salida_pig/comuna' USING PigStorage(',');
