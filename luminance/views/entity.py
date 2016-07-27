import colorsys

import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gdk
from gi.repository import Gtk

from .util import hsv_to_gdk_rgb
from .. import get_resource_path


class FramedEntityList(Gtk.Box):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/entity-list.ui'))
        builder.connect_signals(self)

        self.content = builder.get_object('content-wrapper')
        self.list = builder.get_object('list')

        for entity in model:
            self.list.add(ListBoxRow(entity))

        self.add(self.content)

    def _on_row_activated(self, listbox, row):
        DetailWindow(
            row.model,
            modal=True,
            transient_for=self.get_toplevel(),
            type_hint=Gdk.WindowTypeHint.DIALOG
        ).present()


class ListBoxRow(Gtk.ListBoxRow):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._model = model

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/entity-row.ui'))
        builder.connect_signals(self)

        entity_name_label = builder.get_object('entity-name-label')

        if hasattr(self.model, 'group_id') and self.model.group_id == 0:
            entity_name_label.set_text('All Lights')
        else:
            entity_name_label.set_text(self.model.name)

        self.color_chooser = builder.get_object('color-chooser')
        self.color_chooser.set_rgba(
            hsv_to_gdk_rgb(
                self.model.hue,
                self.model.saturation,
                self.model.brightness
            )
        )

        self.brightness_scale = builder.get_object('brightness-scale')
        self.brightness_scale.set_value(self.model.brightness)

        self.color_chooser_popover_button = builder.get_object('color-chooser-popover-button')

        entity_switch = builder.get_object('entity-switch')
        entity_switch.set_state(self.model.on)
        entity_switch.emit('state-set', self.model.on)

        content = builder.get_object('content-wrapper')

        self.add(content)

    @property
    def model(self):
        return self._model

    def _on_color_activate(self, *args):
        if self.model.on and self.color_chooser.get_visible():
            rgba = self.color_chooser.get_rgba()
            hsv = colorsys.rgb_to_hsv(rgba.red, rgba.green, rgba.blue)

            self.model.hue = int(hsv[0] * 65535)
            self.model.saturation = int(hsv[1] * 255)

    def _on_brightness_scale_change(self, scale, delta, value):
        value = max(min(int(value), 255), 1)

        if value != self.model.brightness:
            self.model.brightness = value

    def _on_entity_switch_state_set(self, switch, value):
        self.model.on = value
        self.brightness_scale.set_sensitive(value)
        self.color_chooser_popover_button.set_sensitive(value)


class DetailWindow(Gtk.Window):
    def __init__(self, model, *args, id=None, **kwargs):
        super().__init__(*args, **kwargs)

        self._model = model

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/entity-detail.ui'))
        builder.connect_signals(self)

        self.headerbar = builder.get_object('headerbar')
        self.headerbar.set_title(model.name)

        self.name_entry_container = builder.get_object('name-entry-container')
        self.name_entry = builder.get_object('name-entry')
        self.name_entry.set_text(self.model.name)

        self.brightness_scale = builder.get_object('brightness-scale')
        self.brightness_scale.set_value(self.model.brightness)

        self.color_chooser = builder.get_object('color-chooser')
        self.color_chooser.set_rgba(
            hsv_to_gdk_rgb(
                self.model.hue,
                self.model.saturation,
                self.model.brightness
            )
        )

        self.alert_long_button = builder.get_object('alert-long-button')
        self.alert_short_button = builder.get_object('alert-short-button')

        self.colorloop_switch = builder.get_object('colorloop-switch')
        self.colorloop_switch.set_state(self.model.effect == 'colorloop')

        self.entity_switch = builder.get_object('entity-switch')
        self.entity_switch.set_state(self.model.on)
        self.entity_switch.emit('state-set', self.model.on)

        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.set_titlebar(self.headerbar)

        self.content = builder.get_object('content')

        wrapper = builder.get_object('content-wrapper')

        self.add(wrapper)

    @property
    def model(self):
        return self._model

    def _on_alert_long_click(self, *args):
        self.model.alert = 'none'
        self.model.alert = 'lselect'

    def _on_alert_short_click(self, *args):
        self.model.alert = 'none'
        self.model.alert = 'select'

    def _on_brightness_scale_change(self, scale, delta, value):
        value = max(min(int(value), 255), 1)

        if value != self.model.brightness:
            self.model.brightness = value

    def _on_close_click(self, *args):
        self.destroy()

    def _on_color_activate(self, *args):
        if self.model.on and self.color_chooser.get_visible():
            rgba = self.color_chooser.get_rgba()
            hsv = colorsys.rgb_to_hsv(rgba.red, rgba.green, rgba.blue)

            self.model.hue = int(hsv[0] * 65535)
            self.model.saturation = int(hsv[1] * 255)

    def _on_save_click(self, *args):
        new_name = self.name_entry.get_text()

        if new_name != self.model.name:
            self.model.name = new_name

        self.destroy()

    def _on_colorloop_switch_change(self, switch, value):
        if value:
            self.model.effect = 'colorloop'
            self.color_chooser.set_sensitive(False)
        else:
            self.model.effect = 'none'
            self.color_chooser.set_sensitive(True)

    def _on_entity_switch_change(self, switch, value):
        self.model.on = value

        self.alert_long_button.set_sensitive(value)
        self.alert_short_button.set_sensitive(value)
        self.brightness_scale.set_sensitive(value)
        self.colorloop_switch.set_sensitive(value)

        if value:
            self.color_chooser.set_sensitive(not self.colorloop_switch.get_state())
        else:
            self.colorloop_switch.set_state(False)
            self.color_chooser.set_sensitive(False)
