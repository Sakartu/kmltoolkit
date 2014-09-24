#!/usr/bin/env python
"""
Usage:
draw_circle.py [-c COLOUR] [-n NAME] [-d DESCRIPTION] <outfile> <coords> <radius> [<sides>]

-c COLOUR --colour COLOUR                   Specify the colour in a KML valid way (for instance, 3fff0000 for slightly transparant blue, or a name such as "red"). [default: blue]
-d DESCRIPTION --description DESCRIPTION    Specify the description of the polygon
-n NAME --name NAME                         Specify the name for the KML node and the name of the polygon. By default this is the same as the name of the outfile.
<outfile>                                   Specifies the filename of the kml file to generate
<coords>                                    Specifies a set of coordinates (lat,long) for the circle. This can be either decimal degrees or deg/min/sec, separated by space, appended with {N,S,W,E}
<radius>                                    The radius of the circle, in meters
<sides>                                     The number of sides to use for the circle. [default: 20]


Example: draw_circle.py out.kml "48 51 29.1348N,2 17 40.8984E"
"""

import docopt
import kml_circle
import util


__author__ = 'peter'


args = docopt.docopt(__doc__)

args, kml = util.parse_arguments(args)

p = kml.newpolygon(name=args['--name'])

print u'Drawing circle for coordinates {0}...'.format(args['<coords>'])
lat, lon = util.parse_latlon(args['<coords>'])

coords = kml_circle.spoints(lon, lat, float(args['<radius>']), int(args['<sides>'] or 20))

p.outerboundaryis = coords
print u'Setting colour...'
p.style.polystyle.color = util.parse_color(args['--colour'])
if '--description' in args:
    print u'Setting description...'
    p.description = args['--description']
print u'Saving to {0}...'.format(args['<outfile>'])
kml.save(args['<outfile>'])
print u'Done!'
