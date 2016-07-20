import os

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gio
from gi.repository import GLib
from gi.repository import Gtk

import phue

from . import __version__
from . import get_resource_path
from . import settings
from .views.window import Window


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs): 
        super().__init__(
            *args,
            application_id='com.craigcabrey.luminance',
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs
        )

        self.add_main_option(
            'host',
            ord('h'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            'Host to use for bridge connection',
            'HOST'
        )

        self.add_main_option(
            'username',
            ord('u'),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            'Username to use for bridge connection',
            'USERNAME'
        )

        self.bridge = None
        self.host = None
        self.username = None
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        builder = Gtk.Builder()

        builder.add_from_resource(get_resource_path('ui/about.ui'))
        builder.add_from_resource(get_resource_path('ui/connect.ui'))
        builder.add_from_resource(get_resource_path('ui/menu.ui'))

        self.app_menu = builder.get_object('app-menu')
        self.about_dialog = builder.get_object('about-dialog')
        self.connect_dialog = builder.get_object('connect-dialog')
        self.hostname_entry = builder.get_object('hostname-entry')

        action = Gio.SimpleAction.new('connect', None)
        action.connect('activate', self._on_connect)
        self.add_action(action)

        action = Gio.SimpleAction.new('about', None)
        action.connect('activate', self._on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new('quit', None)
        action.connect('activate', self._on_quit)
        self.add_action(action)

        self.set_app_menu(self.app_menu)

        self.mark_busy()

    def do_activate(self):
        Gtk.Application.do_activate(self)

        self._connect(self.host, self.username)

        self.unmark_busy()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()

        if options.contains('host'):
            self.host = str(options.lookup_value('host'))

        if options.contains('username'):
            self.username = str(options.lookup_value('username'))

        self.activate()

        return 0

    def _init(self):
        if not self.window:
            self.window = Window(
                self.bridge,
                application=self
            )
        else:
            self.window.reload(self.bridge)

        self.window.show_all()
        self.window.present()

    def _connect(self, host, username):
        if host and username:
            self.bridge = phue.Bridge(
                self.host,
                username=username
            )
        elif host:
            self.bridge = phue.Bridge(
                self.host
            )
        elif username:
            self.bridge = phue.Bridge(
                username=self.username
            )
        else:
            self.bridge = phue.Bridge()

        self.bridge.connect()

        self._init()

        return True

    def _on_connect(self, action, param):
        self.connect_dialog.set_transient_for(self.window)
        response = self.connect_dialog.run()

        if Gtk.ResponseType.OK:
            hostname = self.hostname_entry.get_text()
            self._connect(hostname, None)

        self.connect_dialog.hide()

    def _on_about(self, action, param):
        self.about_dialog.set_version(__version__)
        self.about_dialog.set_transient_for(self.window)
        self.about_dialog.set_modal(True)
        self.about_dialog.present()

    def _on_quit(self, action, param):
        self.quit()
