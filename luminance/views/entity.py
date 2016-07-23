import colorsys

import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gdk
from gi.repository import Gtk

from .util import hsv_to_gdk_rgb
from .. import get_resource_path


class Entity(Gtk.ListBoxRow):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._model = model

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/entity.ui'))
        builder.connect_signals(self)

        entity_name_label = builder.get_object('entity-name-label')
        entity_name_label.set_text(self.model.name)

        color_chooser = builder.get_object('color-chooser')
        color_chooser.set_rgba(
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
