#!/bin/bash
##########################################################################
#
# Extract levels from DEM file to generate svg and geosjon files
#
# Author: Eric Debeau, David Blaisonneau
#
# See printhelp for parameters
# Provide a list of SVG files per level with 2 levels per file
#
#########################################################################

function printhelp () {
  echo "
usage: $0 -f <file> -i <file> -l <length> -L <list>
or     $0 -f <file> -i <file> -l <length> -a <start> -b <stop> -c <step>
  -f: MNT file
  -i: Polygon file for the zone to be extracted
  -l: Length of ways to be removed
  -L: Layers (comma separated value)
  -c: starting layer
  -b: end layer
  -c: step between layers
  -h: print this help
"
  exit
}

# Parse options
while getopts ":f:i:l:L:a:b:c:h" optname
  do
    case "$optname" in
      "f") MNT=$OPTARG;;
      "i") ZONE=$OPTARG;;
      "l") LEN=$OPTARG;;
      "L") LAYERSSTR=$OPTARG;;
      "a") LAYERSSTART=$OPTARG;;
      "b") LAYERSSTOP=$OPTARG;;
      "c") LAYERSSTEP=$OPTARG;;
      "h") printhelp;;
      "?") echo "Unknown option $OPTARG"; printhelp;;
      ":") echo "No argument value for option $OPTARG"; printhelp;;
      *)   echo "Unknown error while processing options";;
    esac
  done

# Check mandatory parameters are present
if [ -z ${MNT+x} ] || [ -z ${ZONE+x} ] || [ -z ${LEN+x} ]
then
  echo "Error: Missing option"
  printhelp
fi

echo ${LAYERSSTART+x}
echo ${LAYERSSTART}

# Parse layers options to get a LAYERS array
if [ $LAYERSSTR ]
then
  IFS=',' read -ra LAYERS <<< "$LAYERSSTR"
elif [ -v LAYERSSTART ] || [ -v LAYERSSTOP ] || [ -v LAYERSSTEP ]
then
  LAYERS=($(seq $LAYERSSTART $LAYERSSTEP $LAYERSSTOP))
else
  echo "Error: Missing layers parameters (-l or -a, -b and -c)"
  printhelp
fi

# Print parameters
echo "Parameters"
echo "  -MNT file: ${MNT}"
echo "  -Zone:     ${ZONE}"
echo "  -Length:   ${LEN}"
echo -n "  -Layers:   "; ( IFS=$','; echo "${LAYERS[*]}" ); echo

# Now the real job

for i in "${LAYERS[@]}"
do
  gdal_contour -fl $i -f geojson "$1" "$i"m.geojson
done
echo "Conversion to geojson done"

python bbox.py "$2" > bbox.txt

for i in "${LAYERS[@]}"
do
  python optimize.py "$i"m.geojson "$3" "$4"
done
echo "Optimization done"


LAYERSSTR=$( IFS=$'|'; echo "${LAYERS[*]}" )
python geojson2svg.py "$2" bbox.txt "${LAYERSSTR}"
echo "SVG files created"
