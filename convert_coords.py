#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Usage:
convert_coords.py [COORD]...

Options:
COORD       A set of lat/lon coordinates in any one of the most used formats. If left out, you will be asked for coords
"""
from __future__ import unicode_literals
import re

from docopt import docopt
from decimal import Decimal

__author__ = 'peter'

FLOATRE = r'\d+(?:[.,]\d+)?'
DMS_FORMAT = re.compile(r'''(\d+)[° ](\d+)[' ]({0})["]?([NS])[ ,](\d+)[° ](\d+)[' ]({0})["]?([EW])'''.format(FLOATRE), re.U | re.I)
DEG_FORMAT = re.compile(r'''([-]?{0})[ ,]([-]?{0})'''.format(FLOATRE), re.U | re.I)


def main():
    args = docopt(__doc__)
    if not args['COORD']:
        while True:
            i = raw_input('Coord: ')
            parse_coord(i.decode('utf8'))

    for c in args['COORD']:
        parse_coord(c)


def parse_coord(c):
    # DD MM SS format
    m = DMS_FORMAT.search(c)
    if m:
        lat = Decimal(m.group(1)) + (Decimal(m.group(2)) / 60) + Decimal(m.group(3)) / 3600
        lat = -lat if 's' in m.group(4).lower() else lat
        lon = Decimal(m.group(5)) + (Decimal(m.group(6)) / 60) + Decimal(m.group(7)) / 3600
        lon = -lon if 'w' in m.group(8) else lon
        print '{0:.6f} {1:.6f}'.format(lat, lon)

    # Deg format
    m = DEG_FORMAT.match(c)
    if m:
        lat = Decimal(m.group(1))
        lat_sign = 'N' if lat >= 0 else 'S'
        lat_deg, lat_min, lat_sec = to_deg_min_sec(abs(lat))

        lon = Decimal(m.group(2))
        lon_sign = 'E' if lon >= 0 else 'W'
        lon_deg, lon_min, lon_sec = to_deg_min_sec(abs(lon))
        print '{0}°{1}\'{2:.2f}"{3} {4}°{5}\'{6:.2f}"{7}'.format(lat_deg, lat_min, lat_sec, lat_sign, lon_deg, lon_min, lon_sec, lon_sign)

def to_deg_min_sec(c):
    deg = int(c)
    _, dec = divmod(Decimal(c), Decimal(1))
    min = dec * Decimal(60)
    dec -= min * (Decimal(1) / Decimal(60))
    sec = dec * Decimal(3600)
    return int(deg), int(min), sec






if __name__ == '__main__':
    main()