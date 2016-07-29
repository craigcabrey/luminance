import threading
import time

import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GLib
from gi.repository import Gtk

import requests

from .. import get_resource_path


class Setup(Gtk.Assistant):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._bridge = None
        self.available_bridges = {}
        self.selected_bridge = None

        self.connect('prepare', self._on_prepare)
        self.set_position(Gtk.WindowPosition.CENTER)

        geometry = Gdk.Geometry()
        geometry.min_height = 450
        geometry.min_width = 500

        self.set_geometry_hints(None, geometry, Gdk.WindowHints.MIN_SIZE)

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/setup.ui'))
        builder.connect_signals(self)

        self.search_page = builder.get_object('search-page')
        self.append_page(self.search_page)
        self.set_page_title(self.search_page, 'Discover Bridge(s)')
        self.set_page_type(self.search_page, Gtk.AssistantPageType.INTRO)

        self.results_list = builder.get_object('results-list')
        self.results_page = builder.get_object('results-page')
        self.append_page(self.results_page)
        self.set_page_title(self.results_page, 'Select Bridge')
        self.set_page_type(self.results_page, Gtk.AssistantPageType.CONTENT)

        self.link_button_page = builder.get_object('link-button-page')
        self.append_page(self.link_button_page)
        self.set_page_title(self.link_button_page, 'Establish Connection')
        self.set_page_type(self.link_button_page, Gtk.AssistantPageType.CUSTOM)

    @property
    def bridge(self):
        return self._bridge

    @bridge.setter
    def bridge(self, value):
        self._bridge = value

    def _on_prepare(self, assistant, page):
        if page == self.search_page:
            threading.Thread(
                args=(self._on_search_complete,),
                daemon=True,
                target=self.search
            ).start()
        elif page == self.link_button_page:
            self.link_button_page.set_visible_child_name('press-link-button')
            threading.Thread(
                args=(self._on_connection_established,),
                daemon=True,
                target=self.try_bridge_connection
            ).start()

    def _on_bridge_selected(self, list_box, row):
        self.selected_bridge = self.available_bridges[row]['address']

    def _on_manual_clicked(self, *args):
        self.results_page.set_visible_child_name('manual')

    def _on_manual_address_changed(self, entry_buffer, *args):
        self.selected_bridge = entry_buffer.get_text()

        if self.selected_bridge:
            self.set_page_complete(self.results_page, True)
        else:
            self.set_page_complete(self.results_page, False)

    def _on_search_complete(self, results):
        if results:
            for row in self.available_bridges.keys():
                self.results_list.remove(row)

            self.available_bridges = {}

            def make_bridge_row(bridge):
                row = Gtk.ListBoxRow(
                    can_focus=False,
                    visible=True
                )

                box = Gtk.Box(
                    can_focus=False,
                    margin_start=12,
                    margin_end=12,
                    margin_top=8,
                    margin_bottom=8,
                    valign=Gtk.Align.CENTER,
                    visible=True
                )

                label = Gtk.Label(
                    can_focus=False,
                    label=bridge['display'],
                    visible=True,
                    xalign=0
                )

                box.add(label)
                row.add(box)

                return row

            row = make_bridge_row(results[0])
            self.results_list.add(row)
            self.available_bridges[row] = results[0]
            self.selected_bridge = results[0]['address']

            for result in results[1:]:
                row = make_bridge_row(result)
                self.results_list.add(row)
                self.available_bridges[row] = result

            self.set_page_complete(self.search_page, True)
            self.results_page.set_visible_child_name('results')
            self.set_page_complete(self.results_page, True)
        else:
            self.results_page.set_visible_child_name('no-bridges-found')

        self.next_page()

        return False

    def search(self, cb):
        try:
            res = requests.get('https://www.meethue.com/api/nupnp')
        except Exception:
            import urllib.parse

            import netdisco.discovery

            network_discovery = netdisco.discovery.NetworkDiscovery(
                limit_discovery=['philips_hue']
            )
            network_discovery.scan()
            data = [
                {
                    'display': result[0],
                    'address': urllib.parse.urlparse(result[1]).hostname
                } for result in network_discovery.get_info('philips_hue')
            ]
        else:
            data = []

            for result in res.json():
                ip = result['internalipaddress']
                res = requests.get('http://{0}/description.xml'.format(ip))

                name = [_ for _ in filter(
                    lambda line: 'friendlyName' in line,
                    res.text.splitlines()
                )]

                assert(len(name) == 1)

                # Yea, this is easier than actually trying to parse the xml...
                name = name[0] \
                    .replace('<friendlyName>', '') \
                    .replace('</friendlyName>', '')

                data.append({'display': name, 'address': ip})
        finally:
            GLib.idle_add(cb, data)

    def _on_connection_established(self):
        if self.bridge:
            self.emit('apply')
        else:
            self.link_button_page.set_visible_child_name('unknown-error')

        return False

    def try_bridge_connection(self, cb):
        import phue

        while True:
            try:
                bridge = phue.Bridge(ip=self.selected_bridge)
            except phue.PhueRegistrationException:
                time.sleep(1)
            except Exception:
                import traceback
                traceback.print_exc()
                break
            else:
                self.bridge = bridge
                break

        GLib.idle_add(cb)
