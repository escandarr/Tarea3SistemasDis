-- Cargar datos filtrados
filtrados = LOAD 'eventos_filtrados/part-m-00000' 
             USING PigStorage(',') 
             AS (uuid:chararray, type:chararray, city:chararray, street:chararray, date:chararray, severity:int);

-- Extraer fecha solamente (yyyy-MM-dd)
solo_fecha = FOREACH filtrados GENERATE SUBSTRING(date, 0, 10) AS fecha;

-- Agrupar por fecha
grouped_by_date = GROUP solo_fecha BY fecha;

-- Contar incidentes por día
count_by_date = FOREACH grouped_by_date GENERATE group AS fecha, COUNT(solo_fecha) AS total;

-- Guardar salida
STORE count_by_date INTO 'salida_pig/fecha' USING PigStorage(',');
