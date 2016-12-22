#!/bin/sh
##########################################################################
#
# Extract levels from DEM file to generate svg and geosjon files
#
# Author: Eric Debeau
#
# $1: MNT file
# $2: Polygon file for the zone to be extracted
# $3: Length of ways to be removed
# Provide a list of SVG files per level with 2 levels per file
#
#########################################################################
echo "Parameters"
echo "  -MNT file" "$1"
echo "  -Zone:   " "$2"
echo "  -Length: " "$3"

for i in "10" "20" "30" "40" "50" "60" "70" "80" "90" "100" "110"
do
   gdal_contour -fl $i -f geojson "$1" "$i"m.geojson
done
echo "Conversion to geojson done"

python bbox.py "$2" > bbox.txt

for i in "10" "20" "30" "40" "50" "60" "70" "80" "90" "100" "110"
do
   python optimize.py "$i"m.geojson "$3" "$4"
done
echo "Optimization done"

python geojson2svg.py "$2" bbox.txt "10|20|30|40|50|60|70|80|90|100"
echo "SVG files created"
