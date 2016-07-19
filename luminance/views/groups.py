import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gdk
from gi.repository import Gtk

from .. import get_resource_path
from .entity import Entity

class Groups(Gtk.Box):
    def __init__(self, bridge, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.new_group_dialog = None

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/groups.ui'))
        builder.connect_signals(self)

        self.content = builder.get_object('groups-page-content')
        self.groups_list_wrapper = builder.get_object('groups-page-frame-listbox')
        self.groups_list = builder.get_object('groups-list')

        self.groups_list_wrapper.add(self.groups_list)

        for group in bridge.groups:
            self.groups_list.add(Entity(group))

        self.add(self.content)

    def _on_new_group_clicked(self, *args):
        if not self.new_group_dialog:
            self.new_group_dialog = NewGroup(
                modal=True,
                transient_for=self.get_toplevel(),
                type_hint=Gdk.WindowTypeHint.DIALOG,
                window_position=Gtk.WindowPosition.CENTER_ON_PARENT
            )

        self.new_group_dialog.show_all()
        self.new_group_dialog.present()

    def _on_row_activated(self, listbox, row):
        print('not implemented')

class NewGroup(Gtk.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/new-group.ui'))
        builder.connect_signals(self)

        headerbar = builder.get_object('headerbar')
        name_grid = builder.get_object('name-grid')

        geometry = Gdk.Geometry()
        geometry.min_height = 350
        geometry.min_width = 430

        self.set_titlebar(headerbar)
        self.set_geometry_hints(None, geometry, Gdk.WindowHints.MIN_SIZE)

        content_area = self.get_content_area()
        content_area.set_border_width(6)
        content_area.add(name_grid)

    def _on_cancel_clicked(self, *args):
        self.hide()
