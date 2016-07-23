import colorsys

import gi

gi.require_version('Gdk', '3.0')

from gi.repository import Gdk


def hsv_to_gdk_rgb(hue, sat, bri):
    rgb = colorsys.hsv_to_rgb(
        hue / 65535,
        sat / 255,
        bri / 255
    )

    return Gdk.RGBA(red=rgb[0], green=rgb[1], blue=rgb[2])
