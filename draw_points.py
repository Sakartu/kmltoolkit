#!/usr/bin/env python
"""
Usage:
draw_points.py [-n NAME] <outfile> <coords>...


-n NAME --name NAME         Specify the name for the KML node and the name of the point(s). By default this is the same as the name of the outfile.
<outfile>                   Specifies the filename of the kml file to generate
<coords>                    Specifies a list of comma separated coordinates (lat,long) for the point(s). This can be either decimal degrees or deg/min/sec, separated by space, appended with {N,S,W,E}

Example: draw_poly.py out.kml "48 51 29.1348N,2 17 40.8984E" "48 51 30.1348N,2 17 41.8984E" "48 51 31.1348N,2 17 41.8984E"
"""
from docopt import docopt
import util

__author__ = 'peter'

args = docopt(__doc__)
args, kml = util.parse_arguments(args)

for index, c in enumerate(args['<coords>']):
    print u'Drawing point for coordinates {0}...'.format(c)
    lat, lon = util.parse_latlon(c)
    p = kml.newpoint(name='{0}-{1}'.format(args['--name'], index), coords=[(lon, lat)])

print u'Saving to {0}...'.format(args['<outfile>'])
kml.save(args['<outfile>'])
print u'Done!'
