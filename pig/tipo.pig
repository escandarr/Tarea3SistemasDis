-- Cargar los datos filtrados
filtrados = LOAD 'eventos_filtrados/part-m-00000' 
             USING PigStorage(',') 
             AS (uuid:chararray, type:chararray, city:chararray, street:chararray, date:chararray, severity:int);

-- Agrupar por tipo de incidente
grouped_by_type = GROUP filtrados BY type;

-- Contar incidentes por tipo
count_by_type = FOREACH grouped_by_type GENERATE group AS tipo, COUNT(filtrados) AS total;

-- Guardar salida
STORE count_by_type INTO 'salida_pig/tipo' USING PigStorage(',');
