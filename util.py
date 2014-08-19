import simplekml

__author__ = 'peter'


def parse_arguments(args):
    if not args.outfile.endswith('.kml'):
        args.outfile += '.kml'

    if not args.name:
        args.name = args.outfile

    kml = simplekml.Kml(name=args.name)
    return args, kml


def parse_latlon(c):
    try:
        lat, lon = c.split(',')
    except ValueError:
        print u'Could not split {0}, invalid coordinates!'
        raise

    if 'n' in lat.lower() or 's' in lat.lower():
        deg, min, sec = lat[:-1].split()
        if 's' in lat.lower():
            lat = -(float(deg) + (float(min) / 60) + (float(sec) / 3600))
        else:
            lat = float(deg) + (float(min) / 60) + (float(sec) / 3600)
    if 'e' in lon.lower() or 'w' in lon.lower():
        deg, min, sec = lon[:-1].split()
        if 'w' in lon.lower():
            lon = -(float(deg) + (float(min) / 60) + (float(sec) / 3600))
        else:
            lon = float(deg) + (float(min) / 60) + (float(sec) / 3600)
    try:
        lat, lon = float(lat), float(lon)
    except ValueError:
        print u'Could not convert {0} to floats!'.format((lat, lon))
        raise
