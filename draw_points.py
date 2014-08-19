#!/usr/bin/env python
import argparse
import simplekml
import util

__author__ = 'peter'

parser = argparse.ArgumentParser(epilog='Example usage: {0} "47 59 00N,38 45 00E" "47 59 59N,38 45 00E" "47 59 59N, 38 45 59E" "47 59 00N, 38 45 59E" out.kml'.format(__file__))
parser.add_argument('--name', '-n', help='The name for the kml file and the point(s), default is the same name as the outfile.')
parser.add_argument('--colour', '-c', help='The colour of the points, given as a KML valid colour (for instance, 3fff0000 for blue)', default='3fff0000')
parser.add_argument('coords', nargs='+', help='Point coordinates, separated by a comma for lat/long, separated by a space for next point. Can be given as degrees/minutes/seconds by using "48 51 29.1348N,2 17 40.8984E"')
parser.add_argument('outfile', help='The name of the output (kml) file')
args = parser.parse_args()

args, kml = util.parse_arguments(args)

p = kml.newoint(name=args.name)

for index, c in enumerate(args.coords):
    print u'Drawing point for coordinates {0}...'.format(args.coords)
    lat, lon = util.parse_latlon(c)
    p = kml.newpoint(name=args.name, coords=[(lon, lat)])
    print u'Setting colour...'
    p.style.polystyle.color = args.colour

print u'Saving to {0}...'.format(args.outfile)
kml.save(args.outfile)
print u'Done!'
