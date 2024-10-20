-- Script to list all bands with Glam rock as their main style, ranked by longevity

SELECT band_name, 
       IFNULL(
           -- If the band has split, calculate lifespan until the split year
           (split - formed), 
           -- If the band is still active, calculate lifespan until 2022
           (2022 - formed)
       ) AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
