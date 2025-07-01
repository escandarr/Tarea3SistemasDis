-- Cargar CSV sin encabezado desde /data
raw = LOAD 'eventos_sin_filtrar.csv' 
      USING PigStorage(',') 
      AS (uuid:chararray, type:chararray, city:chararray, street:chararray, pubMillis:chararray, severity:int);

-- Filtrar entradas inválidas
valid = FILTER raw BY 
    (type IS NOT NULL AND type != '') AND 
    (city IS NOT NULL AND city != '') AND 
    (severity IS NOT NULL) AND 
    (pubMillis IS NOT NULL AND pubMillis != '');

-- Convertir pubMillis directamente a tipo DATE con el formato correcto
processed = FOREACH valid GENERATE 
    uuid, 
    LOWER(type) AS type, 
    LOWER(city) AS city, 
    LOWER(street) AS street,
    ToDate(pubMillis, 'yyyy-MM-dd HH:mm:ss') AS date,
    severity;

-- Eliminar salida previa si existe
rmf 'eventos_filtrados';

-- Guardar CSV limpio 
STORE processed INTO 'eventos_filtrados' USING PigStorage(',');
