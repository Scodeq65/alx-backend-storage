-- Script to rank country origins of bands by the number of fans
-- The script should not fail if the table already exists

SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
