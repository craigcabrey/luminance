import colorsys

import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gdk
from gi.repository import Gtk

from .. import get_resource_path


class Entity(Gtk.ListBoxRow):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._model = model

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/entity.ui'))
        builder.connect_signals(self)

        self.color_chooser_button = builder.get_object('color-chooser-popover-button')
        self.color_chooser = builder.get_object('color-chooser')

        self.set_visible(True)
        self.set_can_focus(True)

        self.grid = Gtk.Grid()
        self.label = Gtk.Label(label=self.model.name)
        self.switch = Gtk.Switch()

        self.grid.set_visible(True)
        self.grid.set_can_focus(False)
        self.grid.set_row_spacing(0)
        self.grid.set_column_spacing(16)
        self.grid.set_margin_start(12)
        self.grid.set_margin_end(6)
        self.grid.set_margin_top(6)
        self.grid.set_margin_bottom(6)
        self.grid.set_valign(Gtk.Align.CENTER)

        self.label.set_visible(True)
        self.label.set_can_focus(False)
        self.label.set_hexpand(True)
        self.label.set_xalign(0)
        self.label.set_use_underline(True)
        self.label.set_mnemonic_widget(self.switch)
        self.grid.attach(self.label, 0, 0, 1, 1)

        self.scale = Gtk.Scale.new_with_range(
            Gtk.Orientation.HORIZONTAL, 1, 254, 1
        )
        self.scale.set_visible(True)
        self.scale.set_can_focus(True)
        self.scale.set_draw_value(False)
        self.scale.set_value(self.model.brightness)
        self.scale.set_sensitive(self.model.on)
        self.scale.connect('change-value', self._on_scale_change)
        self.grid.attach(self.scale, 1, 0, 12, 2)

        self.color_chooser_button.set_sensitive(self.model.on)
        self.grid.attach(self.color_chooser_button, 13, 0, 1, 1)

        self.switch.set_visible(True)
        self.switch.set_can_focus(True)
        self.switch.set_halign(Gtk.Align.END)
        self.switch.set_valign(Gtk.Align.CENTER)
        self.switch.set_state(self.model.on)
        self.switch.connect('state-set', self._on_switch_change)
        self.grid.attach(self.switch, 14, 0, 1, 2)

        self.add(self.grid)

    @property
    def model(self):
        return self._model

    def _on_color_toggle(self, *args):
        if self.color_chooser_button.get_active():
            rgb = colorsys.hsv_to_rgb(
                self.model.hue / 65535,
                self.model.saturation / 255,
                self.model.brightness / 255
            )

            self.color_chooser.set_rgba(
                Gdk.RGBA(red=rgb[0], green=rgb[1], blue=rgb[2])
            )
        elif self.model.on:
            rgba = self.color_chooser.get_rgba()
            hsv = colorsys.rgb_to_hsv(rgba.red, rgba.green, rgba.blue)

            self.model._set('hue', int(hsv[0] * 65535))
            self.model._set('sat', int(hsv[1] * 255))

    def _on_scale_change(self, scale, delta, value):
        value = int(min(value, 254))

        if value != self.model.brightness:
            self.model.brightness = value

    def _on_switch_change(self, switch, value):
        self.model.on = value
        self.scale.set_sensitive(value)
        self.color_chooser_button.set_sensitive(value)
