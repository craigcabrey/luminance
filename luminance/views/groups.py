import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gdk
from gi.repository import Gtk

import phue

from .. import get_resource_path
from .entity import ListBoxRow
from .group import AllGroupDetail
from .group import GroupDetail

class Groups(Gtk.Box):
    def __init__(self, bridge, *args, **kwargs):
        super().__init__(*args, **kwargs)

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/groups.ui'))
        builder.connect_signals(self)

        self.content = builder.get_object('content-wrapper')
        self.groups_list = builder.get_object('list')

        self.groups_list.add(ListBoxRow(phue.AllLights(bridge)))
        for group in bridge.groups:
            self.groups_list.add(ListBoxRow(group))

        self.add(self.content)

    def _on_row_activated(self, listbox, row):
        if row.model.group_id == 0:
            AllGroupDetail(
                row.model,
                modal=True,
                transient_for=self.get_toplevel(),
                type_hint=Gdk.WindowTypeHint.DIALOG
            ).present()
        else:
            GroupDetail(
                row.model,
                modal=True,
                transient_for=self.get_toplevel(),
                type_hint=Gdk.WindowTypeHint.DIALOG
            ).present()
