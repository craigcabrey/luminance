import colorsys

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from .util import hsv_to_gdk_rgb
from .. import get_resource_path


class Light(Gtk.Window):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._model = model

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/light.ui'))
        builder.connect_signals(self)

        headerbar = builder.get_object('headerbar')
        headerbar.set_title(model.name)
        headerbar.set_subtitle('Light {id}'.format(id=model.light_id))

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

        self.light_switch = builder.get_object('light-switch')
        self.light_switch.set_state(self.model.on)

        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.set_titlebar(headerbar)

        content = builder.get_object('content-wrapper')

        self.add(content)

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
        value = int(min(value, 254))

        if value != self.model.brightness:
            self.model.brightness = value

    def _on_close_click(self, *args):
        self.close()

    def _on_color_activate(self, *args):
        rgba = self.color_chooser.get_rgba()
        hsv = colorsys.rgb_to_hsv(rgba.red, rgba.green, rgba.blue)

        self.model.hue = int(hsv[0] * 65535)
        self.model.saturation = int(hsv[1] * 255)

    def _on_save_click(self, *args):
        new_name = self.name_entry.get_text()

        if new_name != self.model.name:
            self.model.name = new_name

        self.close()

    def _on_colorloop_switch_change(self, switch, value):
        if value:
            self.model.effect = 'colorloop'
            self.color_chooser.set_sensitive(False)
        else:
            self.model.effect = 'none'
            self.color_chooser.set_sensitive(True)

    def _on_light_switch_change(self, switch, value):
        self.model.on = value

        self.alert_long_button.set_sensitive(value)
        self.alert_short_button.set_sensitive(value)
        self.brightness_scale.set_sensitive(value)
        self.colorloop_switch.set_sensitive(value)

        if value:
            self.color_chooser.set_sensitive(not self.colorloop_switch.get_state())
        else:
            self.color_chooser.set_sensitive(False)
