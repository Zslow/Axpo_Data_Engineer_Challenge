-- Useful Queries

SELECT
  id,
  count(1),
  date_format( '%Y-%m-%d', dt)
FROM
  iot_temperature
GROUP BY
  id, date_format( '%Y-%m-%d', dt);

SELECT
  id,
  MAX_BY("value", dt),
  date_format( '%Y-%m-%d %h:%i:%s', MAX(dt))
FROM
  iot_temperature
GROUP BY
  id limit 100;

select * from (
SELECT *,
           ROW_NUMBER() OVER (partition BY id order by dt desc) as rn
FROM iot_temperature
 ) a
where rn = 1 limit 100;

SELECT "id" , 
date_bin(CAST('1 minute' AS interval), "dt", 0) "dt_bin" , mean("value") "value" 
FROM "doc"."iot_temperature" 
GROUP BY date_bin(CAST('1 minute' AS interval), "dt", 0), "id" 
ORDER BY 2 asc ;