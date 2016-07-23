import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gdk
from gi.repository import Gtk

from .. import get_resource_path
from .entity import Entity
from .light import Light

class Lights(Gtk.Box):
    def __init__(self, bridge, *args, **kwargs):
        super().__init__(*args, **kwargs)

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/lights.ui'))
        builder.connect_signals(self)

        self.content = builder.get_object('lights-page-content')
        self.lights_list_wrapper = builder.get_object('lights-page-frame-listbox')
        self.lights_list = builder.get_object('lights-list')

        self.lights_list_wrapper.add(self.lights_list)

        for light in bridge.get_light_objects(mode='id').values():
            self.lights_list.add(Entity(light))

        self.add(self.content)

    def _on_row_activated(self, listbox, row):
        Light(
            row.model,
            modal=True,
            transient_for=self.get_toplevel(),
            type_hint=Gdk.WindowTypeHint.DIALOG
        ).present()
