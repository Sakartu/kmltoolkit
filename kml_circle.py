__author__ = 'peter'
#!/usr/bin/env python

# This code was originally from:
# The MIT License
#
# Copyright (c) 2007 Nick Galbreath
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# Version 3 - 24-Sept-2014 Fixed some pep8 violations and removed main method
#                          calls (by Sakartu)
#
# Version 2 - 12-Sept-2007 Simplified XML output
#                          Added commandline interface
# Version 1 - 10-Sept-2007 Initial release
#

from math import *


def to_earth(p):
    """
    Convert (x,y,z) on unit sphere
    back to (long, lat)
    :param p: is vector of three elements
    :return:
    """
    if p[0] == 0.0:
        longitude = pi / 2.0
    else:
        longitude = atan(p[1] / p[0])
    colatitude = acos(p[2])
    latitude = (pi / 2.0 - colatitude)

    # select correct branch of arctan
    if p[0] < 0.0:
        if p[1] <= 0.0:
            longitude = -(pi - longitude)
        else:
            longitude = pi + longitude

    deg = 180.0 / pi
    return [longitude * deg, latitude * deg]


def to_cart(longitude, latitude):
    """
    convert long, lat IN RADIANS to (x,y,z)
    :return: lat,lon in radians
    """
    theta = longitude
    # spherical coordinate use "co-latitude", not "lattitude"
    # lattiude = [-90, 90] with 0 at equator
    # co-latitude = [0, 180] with 0 at north pole
    phi = pi / 2.0 - latitude
    return [cos(theta) * sin(phi), sin(theta) * sin(phi), cos(phi)]


def rot_point(vec, pt, phi):
    """
    rotate point pt, around unit vector vec by phi radians
    http://blog.modp.com/2007/09/rotating-point-around-vector.html
    :param vec: vector to rotate around
    :param pt: point to rotate
    :param phi: radians to rotate
    :return:
    """
    # remap vector for sanity
    (u, v, w, x, y, z) = (vec[0], vec[1], vec[2], pt[0], pt[1], pt[2])

    a = u * x + v * y + w * z
    d = cos(phi)
    e = sin(phi)

    return [(a * u + (x - a * u) * d + (v * z - w * y) * e),
            (a * v + (y - a * v) * d + (w * x - u * z) * e),
            (a * w + (z - a * w) * d + (u * y - v * x) * e)]


def spoints(lon, lat, meters, n, offset=0):
    """
    spoints -- get raw list of points in long,lat format

    meters: radius of polygon
    n: number of sides
    offset: rotate polygon by number of degrees

    Returns a list of points comprising the object
    """
    # constant to convert to radians
    rad = pi / 180.0
    # Mean Radius of Earth, meters
    mr = 6378.1 * 1000.0
    offsetradians = offset * rad
    # compute longitude degrees (in radians) at given latitude
    r = (meters / (mr * cos(lat * rad)))

    vec = to_cart(lon * rad, lat * rad)
    pt = to_cart(lon * rad + r, lat * rad)
    pts = []

    for i in range(0, n):
        pts.append(to_earth(rot_point(vec, pt, offsetradians + (2.0 * pi / n) * i)))

    # connect to starting point exactly
    # not sure if required, but seems to help when
    # the polygon is not filled
    pts.append(pts[0])
    return pts
