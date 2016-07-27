import colorsys

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from .entity import EntityDetail
from .util import hsv_to_gdk_rgb
from .. import get_resource_path


class LightDetail(EntityDetail):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
