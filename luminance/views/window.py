import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import Gio
from gi.repository import GLib
from gi.repository import Gtk

from .. import get_resource_path
from .bridge import Bridge
from .groups import Groups
from .lights import Lights


class Window(Gtk.ApplicationWindow):
    def __init__(self, bridge, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bridge = bridge

        GLib.set_application_name('Luminance')
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_name('luminance')

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/main.ui'))
        builder.connect_signals(self)

        self.header_bar = builder.get_object('headerbar')
        self.status_bar = builder.get_object('status-bar')

        self.main_content = builder.get_object('main-content')
        self.main_stack = builder.get_object('main-stack')

        self.lights_page = builder.get_object('lights-page')
        self.lights_page.add(Lights(self.bridge))

        self.groups_page = builder.get_object('groups-page')
        self.groups_page.add(Groups(self.bridge))

        self.bridge_page = builder.get_object('bridge-page')
        self.bridge_page.add(Bridge(self.bridge))

        self._on_connection_change()

        geometry = Gdk.Geometry()
        geometry.min_height = 450
        geometry.min_width = 575
        self.set_geometry_hints(None, geometry, Gdk.WindowHints.MIN_SIZE)
        self.set_titlebar(self.header_bar)

        self.add(self.main_content)

    def _on_connection_change(self):
        self.status_bar.push(
            self.status_bar.get_context_id('host-status'),
            'Connected: {host}'.format(host=self.bridge.ip)
        )

    def reload(self, bridge):
        print('reload triggered')
