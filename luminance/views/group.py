import colorsys

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from .entity import DetailWindow
from .util import hsv_to_gdk_rgb
from .. import get_resource_path


class GroupDetail(DetailWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/group-detail.ui'))
        builder.connect_signals(self)

        self.headerbar.set_subtitle('Group {id}'.format(id=self.model.group_id))

        delete_button = Gtk.Button(label='Delete', visible=True)
        delete_button.connect('clicked', self._on_delete_click)

        self.headerbar.pack_end(delete_button)

        content = builder.get_object('content-wrapper')
        lights_list = builder.get_object('light-listbox')

        self.selected_lights = set(light.light_id for light in self.model.lights)

        for light in self.model.bridge.lights_by_id.values():
            row = Gtk.ListBoxRow(
                activatable=False,
                can_focus=False,
                visible=True
            )

            box = Gtk.Box(
                can_focus=False,
                visible=True,
                margin_start=12,
                margin_end=6,
                margin_top=8,
                margin_bottom=8
            )

            check_box = Gtk.CheckButton(
                active=light.light_id in self.selected_lights,
                can_focus=True,
                draw_indicator=True,
                label=light.name,
                receives_default=False,
                visible=True
            )

            check_box.connect('toggled', self._on_light_toggle, light)

            box.add(check_box)
            row.add(box)
            lights_list.add(row)

        self.content.pack_start(content, True, True, 6)
        self.content.reorder_child(content, 2)

    def _on_delete_click(self, *args):
        dialog = Gtk.MessageDialog(
            buttons=Gtk.ButtonsType.YES_NO,
            secondary_text='Are you sure you wish to delete this group?',
            text='Confirm Deletion',
            transient_for=self
        )

        if dialog.run():
            self.model.bridge.delete_group(self.model.group_id)
            self.destroy()

        dialog.destroy()

    def _on_light_toggle(self, check_button, light):
        if check_button.get_active():
            self.selected_lights.add(light.light_id)
        else:
            self.selected_lights.remove(light.light_id)

    def _on_save_click(self, *args):
        self.model.lights = list(self.selected_lights)

        super()._on_save_click(self, *args)


class AllGroupDetail(DetailWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headerbar.set_title('All Lights')

        # Remove ui elements that indicate modifiability
        # This is definitely on the hacky side, but it'll do for now
        self.headerbar.remove(self.headerbar.get_children()[1])
        self.content.remove(self.name_entry_container)
