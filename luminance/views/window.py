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
        self.set_default_icon_list([
            GdkPixbuf.Pixbuf.new_from_resource(
                get_resource_path('icons/16x16.png')
            ),
            GdkPixbuf.Pixbuf.new_from_resource(
                get_resource_path('icons/32x32.png')
            ),
            GdkPixbuf.Pixbuf.new_from_resource(
                get_resource_path('icons/48x48.png')
            ),
            GdkPixbuf.Pixbuf.new_from_resource(
                get_resource_path('icons/64x64.png')
            ),
            GdkPixbuf.Pixbuf.new_from_resource(
                get_resource_path('icons/128x128.png')
            ),
            GdkPixbuf.Pixbuf.new_from_resource(
                get_resource_path('icons/256x256.png')
            ),
            GdkPixbuf.Pixbuf.new_from_resource(
                get_resource_path('icons/512x512.png')
            )
        ])

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

        self.set_titlebar(self.header_bar)
        self.add(self.main_content)

    def _on_connection_change(self):
        self.status_bar.push(
            self.status_bar.get_context_id('host-status'),
            'Connected: {host}'.format(host=self.bridge.ip)
        )

    def reload(self, bridge):
        print('reload triggered')
