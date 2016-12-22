#############################################################################
#    Copyright 2016 Eric Debeau <eric.debeau@gmail.com>
#
#    Optimize geojson file keeping only ways with at least minimal length
#    - parameters argv[1] : name of limit file (polygon geojson)
#    - parameter: argv[2]: bbox separated by |
#    - parameter: argv[3]: levels separtated by |
#
#    This script is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    This script is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this script.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
import json
import sys

COLOR_DRAW = "black"
COLOR_CUT = "red"
COLOR = "@@@"
END_LEVEL_FILE = "m.geojson"

#compute size with bbox
f = open (sys.argv[2], 'r')
bbox = f.read()

levels_string = sys.argv[3]

left, bottom, right, top = bbox.split('|')
levels = levels_string.split('|')
for level in levels:
   level = int(level)

x = float(left)
y = float(top)
res = 1000 / (float(right)-float(left))

SVG_START = '<svg width="1000" height="1000" xmlns="http://www.w3.org/2000/svg"  encoding="UTF-8"
 version="1.1">'
SVG_END = '</svg>'

NB_DECIMALS = 2
float_format = "{0:."+str(NB_DECIMALS)+"f}"

# Read file with limit (polygon file)
with open(sys.argv[1]) as json_data:
    data = json.load(json_data)

# Check polygon : nb >4 and first= last and type=polygon

limit = '<path d="M'
polygon_coords = data["features"][0]["geometry"]["coordinates"][0]
point = polygon_coords[0]

limit+= str(float(float_format.format((point[0]-x)*res))) + ' ' + str(float(float_format.format((
y-point[1])*res)))
for point in polygon_coords:
    limit += "," + str(float(float_format.format((point[0]-x)*res))) + " " + str(float(float_form
at.format((y-point[1])*res)))
limit_cut = limit + '" stroke="' + COLOR_CUT + '" fill="transparent"  stroke-linecap="round"/>'
limit_draw = limit + '" stroke="' + COLOR_DRAW + '" fill="transparent" stroke-linecap="round"/>'

svg_levels = {}

# loop for levels
for level in levels:
        level_file = level + END_LEVEL_FILE
        with open(level_file) as json_data:
                data = json.load(json_data)

        svg_string = ""
        for lines in data["features"]:
                svg_string += '<path d="M'
                point = lines["geometry"]["coordinates"][0]
                svg_string+= str(float(float_format.format((point[0]-x)*res)))+' '+str(float(float_format.format((y-point[1])*res)))
                for point in lines["geometry"]["coordinates"]:
                        svg_string += "," + str(float(float_format.format((point[0]-x)*res))) + " " +str(float(float_format.format((y-point[1])*res)))
                svg_string += '" stroke="' + COLOR + '" fill="transparent" stroke-linecap="round"/>'
        svg_levels[level] = svg_string

# Create svg files with 3 layers.

# Fisrt SVG: draw limit
svg = SVG_START + limit_draw
svg += svg_levels[levels[0]].replace(COLOR, COLOR_DRAW)
svg += SVG_END
out = open ("0m.svg","w")
out.write (svg)
out.close()

for i in range(0,len(levels)):
        svg_file = levels[i] + "m.svg"
        out = open (svg_file, "w")
        svg = SVG_START + limit_cut
        svg += svg_levels[levels[i]].replace(COLOR, COLOR_CUT)
        if (i!=(len(levels)-1)):
             svg += svg_levels[levels[i+1]].replace(COLOR, COLOR_DRAW)
        svg += SVG_END
        out.write (svg)
        out.close()

# Create a SVG file with all levels
svg_file = "all.svg"
out = open (svg_file, "w")
svg = SVG_START + limit_cut
for i in range(0,len(levels)):
    svg += svg_levels[levels[i]].replace(COLOR, COLOR_CUT)
svg += SVG_END
out.write (svg)
out.close()
