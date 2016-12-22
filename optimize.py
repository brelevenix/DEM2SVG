#############################################################################
#    Copyright 2016 Eric Debeau <eric.debeau@gmail.com>
#
#    Optimize geojson file keeping only ways with at least minimal length
#    - parameters: file_name
#    - parameters: length_min
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
from math import radians, cos, sin, asin, sqrt


def distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    R = 6371000  # radius of the earth in m
    x = (lon2 - lon1) * cos(0.5 * (lat2 + lat1))
    y = lat2 - lat1
    d = R * sqrt(x * x + y * y)
    return (round(d))


def length_way(coords):
    length = 0.0
    for i in range(1, len(coords)):
        length += distance(coords[i-1][0], coords[i-1][1],
                           coords[i][0], coords[i][1])
    return (length)

nb_decimals = 5
float_format = "{0:."+str(nb_decimals)+"f}"

file_name = sys.argv[1]
length_min = int(sys.argv[2])

with open(file_name) as json_data:
    data = json.load(json_data)
json_data.close()

for way in data["features"]:
    coords = way["geometry"]["coordinates"]
    for point in coords:
        point[0] = float(float_format.format(point[0]))
        point[1] = float(float_format.format(point[1]))
    way["properties"]["length"] = length_way(coords)

ways = data["features"]
data["features"] = [x for x in ways if x["properties"]["length"] >= length_min]

if "crs" in data.keys():
    del (data["crs"])

f = open(file_name, "w")
f.write(json.dumps(data))
f.close()
