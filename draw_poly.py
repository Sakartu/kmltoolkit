#!/usr/bin/env python
"""
Usage:
draw_poly.py [-c COLOUR] [-n NAME] [-c DESCRIPTION] <outfile> <coords>...

-c COLOUR --colour COLOUR                   Specify the colour in a KML valid way (for instance, 3fff0000 for slightly transparant blue, or a name such as "red"). [default: blue]
-n NAME --name NAME                         Specify the name for the KML node and the name of the polygon. By default this is the same as the name of the outfile.
-d DESCRIPTION --description DESCRIPTION    Specify the description of the polygon
<outfile>                   Specifies the filename of the kml file to generate
<coords>                                    Specifies a list of comma separated coordinates (lat,long) for the polygon. This can be either decimal degrees or deg/min/sec, separated by space, appended with {N,S,W,E}

Example: draw_poly.py out.kml "48 51 29.1348N,2 17 40.8984E" "48 51 30.1348N,2 17 41.8984E" "48 51 31.1348N,2 17 41.8984E"
"""

import docopt
import util


__author__ = 'peter'


args = docopt.docopt(__doc__)

args, kml = util.parse_arguments(args)

p = kml.newpolygon(name=args['--name'])

coords = []

# Check if last coordinate is also first coordinate, to make the polygon closing
if not args['<coords>'][0] == args['<coords>'][-1]:
    args['<coords>'].append(args['<coords>'][0])
print u'Drawing polygon for coordinates {0}...'.format(args['<coords>'])
for c in args['<coords>']:
    lat, lon = util.parse_latlon(c)
    coords.append((lon, lat))

p.outerboundaryis = coords
print u'Setting colour...'
p.style.polystyle.color = util.parse_color(args['--colour'])
print u'Setting description...'
p.description = args['--description']
print u'Saving to {0}...'.format(args['<outfile>'])
kml.save(args['<outfile>'])
print u'Done!'
