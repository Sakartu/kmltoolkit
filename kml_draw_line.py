#!/usr/bin/env python
"""
Usage:
draw_line.py [-c COLOUR] [-n NAME] [-d DESCRIPTION] <outfile> <coords>...

-c COLOUR --colour COLOUR                   Specify the colour in a KML valid way (for instance, 3fff0000 for slightly transparant blue or a name such as "red"). [default: blue]
-n NAME --name NAME                         Specify the name for the KML node and the name of the line. By default this is the same as the name of the outfile.
<outfile>                                   Specifies the filename of the kml file to generate
                <coords>                    Specifies a list of comma separated coordinates (lat,long) for the line. This can be either decimal degrees or deg/min/sec, separated by space, appended with {N,S,W,E}
-d DESCRIPTION --description DESCRIPTION    Specify the description of the line

Example: draw_poly.py out.kml "48 51 29.1348N,2 17 40.8984E" "48 51 30.1348N,2 17 41.8984E" "48 51 31.1348N,2 17 41.8984E"
"""

import docopt
import util


__author__ = 'peter'


args = docopt.docopt(__doc__)

args, kml = util.parse_arguments(args)

p = kml.newlinestring(name=args['--name'])

coords = []

print u'Drawing line for coordinates {0}...'.format(args['<coords>'])

for c in args['<coords>']:
    lat, lon = util.parse_latlon(c)
    coords.append((lon, lat))

p.coords = coords
print u'Setting colour...'
p.style.linestyle.color = util.parse_color(args['--colour'])
print u'Setting description...'
p.description = args['--description']
print u'Saving to {0}...'.format(args['<outfile>'])
kml.save(args['<outfile>'])
print u'Done!'
