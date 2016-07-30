import colorsys

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from .entity import DetailWindow
from .util import hsv_to_gdk_rgb
from .. import get_resource_path


class NewGroup(Gtk.Dialog):
    def __init__(self, bridge, *args, **kwargs):
        super().__init__(
            *args,
            modal=True,
            use_header_bar=1,
            title='New Group',
            **kwargs
        )

        self._name = None
        self._lights = []
        self.add_button('Cancel', Gtk.ResponseType.CANCEL)
        self.add_button('Save', Gtk.ResponseType.APPLY)
        self.set_response_sensitive(Gtk.ResponseType.APPLY, bool(self.name))
        self.connect('response', self._on_response)

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/new-group.ui'))
        builder.connect_signals(self)

        content_wrapper = builder.get_object('content-wrapper')
        content = builder.get_object('content')

        self.lights_list = SelectableLightList(
            bridge.lights_by_id.values(),
            set()
        )

        content.add(self.lights_list)

        content_area = self.get_content_area()
        content_area.add(content_wrapper)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def lights(self):
        return self._lights

    @lights.setter
    def lights(self, value):
        self._lights = value

    def _on_name_changed(self, name_buffer, *args):
        self.name = name_buffer.get_text()
        self.set_response_sensitive(Gtk.ResponseType.APPLY, bool(self.name))

    def _on_response(self, *args):
        self.lights = list(self.lights_list.selected_lights)


class GroupDetail(DetailWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headerbar.set_subtitle('Group {id}'.format(id=self.model.group_id))

        delete_button = Gtk.Button(label='Delete', visible=True)
        delete_button.connect('clicked', self._on_delete_click)

        self.headerbar.pack_end(delete_button)

        self.lights_list = SelectableLightList(
            self.model.bridge.lights_by_id.values(),
            set(light.light_id for light in self.model.lights)
        )

        self.content.pack_start(self.lights_list, True, True, 6)
        self.content.reorder_child(self.lights_list, 2)

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

    def _on_save_click(self, *args):
        self.model.lights = list(self.lights_list.selected_lights)

        super()._on_save_click(self, *args)


class AllGroupDetail(DetailWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headerbar.set_title('All Lights')

        # Remove ui elements that indicate modifiability
        # This is definitely on the hacky side, but it'll do for now
        self.headerbar.remove(self.headerbar.get_children()[1])
        self.content.remove(self.name_entry_container)


class SelectableLightList(Gtk.Frame):
    def __init__(self, lights, initial_selection, *args, **kwargs):
        super().__init__(
            *args,
            can_focus=False,
            shadow_type=Gtk.ShadowType.NONE,
            visible=True,
            **kwargs
        )

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/group-detail.ui'))
        builder.connect_signals(self)

        content = builder.get_object('content-wrapper')
        lights_list = builder.get_object('light-list')

        self.lights = lights
        self._selected_lights = initial_selection

        for light in self.lights:
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
                border_width=6,
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

        self.add(content)

    @property
    def selected_lights(self):
        return self._selected_lights

    def _on_light_toggle(self, check_button, light):
        if check_button.get_active():
            self.selected_lights.add(light.light_id)
        else:
            self.selected_lights.remove(light.light_id)
