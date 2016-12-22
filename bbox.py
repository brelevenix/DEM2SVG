#############################################################################
#    Copyright 2016 Eric Debeau <eric.debeau@gmail.com>
#
#    Outputs bbox coordinates from a geojson polygon file
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

file_name = sys.argv[1]
with open(file_name) as data_file:
    data = json.load(data_file)

left = 180.0
right = -180.0
top = -90.0
bottom = 90.0

for point in data["features"][0]["geometry"]["coordinates"][0]:
    lon = point[0]
    lat = point[1]
    if (lon < left):
        left = lon
    if (lon > right):
        right = lon
    if (lat < bottom):
        bottom = lat
    if (lat > top):
        top = lat

bbox_left = "%.2f" % (left-0.01)
bbox_right = "%.2f" % (right+0.01)
bbox_top = "%.2f" % (top+0.01)
bbox_bottom = "%.2f" % (bottom-0.01)
print bbox_left, '|', bbox_bottom, '|', bbox_right, '|', bbox_top
