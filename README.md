# DEM2SVG
Conversion from Digital Elevation Model to SVG files representing altitude levels

Get a Digital Elevation Model
- SRTM (precision model: 90m)
- EU DEM: http://www.eea.europa.eu/data-and-maps/data/eu-dem (precision model: 30m)
- Bretagne: geobretagne (precision model: 5m, date: 2012)
- LTA (precision model: 2m, date: 2011)

Get a geojson polygon file for the zone
- overpass request to get xml file and convert to geojson with JOSM. 
- Note that overpass request only provides a list of ways not always clockwise when requesting a boundary limit

Projection conversion to EPSG:4326 if necessary (required to be compatible with the geojson polygon to delimit the zone)
```
gdalwarp -overwrite -s_srs EPSG:2154 -t_srs EPSG:4326 -of GTiff lambert.tif wgs84.tif
```

Zone cut
```
gdalwarp -q -cutline zone.geojson -crop_to_cutline -of GTiff wgs84.tif zone.tif
```

Execute extraction (contour creation, file optimization and svg file creation)
```
./extract_levels.sh zone.geojson zone.tif 500
```

LTA model:
- data are provided with xyz files using CC48 projection sorted by longitude coordinates
- sort data using unix command: 
```
sort --field-separator=',' -k2,2 -k1,1 1208000_7296000.xyz > sort.xyz
```
- transform xyz files to tif: 
```
gdal_translate -of GTiff .xyz .tif
```
- merge tif files: 
```
gdalwarp *.tif lta.tif
```
