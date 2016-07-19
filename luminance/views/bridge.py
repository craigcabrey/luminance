import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from .. import get_resource_path


class Bridge(Gtk.Box):
    def __init__(self, bridge, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.api = bridge.get_api()

        builder = Gtk.Builder()
        builder.add_from_resource(get_resource_path('ui/bridge.ui'))
        builder.connect_signals(self)

        self.content = builder.get_object('bridge-page-content')

        self.bridge_name_label = builder.get_object('bridge-name')
        self.bridge_name_label.set_text(bridge.name)

        self.bridge_id_label = builder.get_object('bridge-id')
        self.bridge_id_label.set_text(self.api['config']['bridgeid'])

        self.bridge_model_label = builder.get_object('bridge-model')
        self.bridge_model_label.set_text(self.api['config']['modelid'])

        self.bridge_timezone_label = builder.get_object('bridge-timezone')
        self.bridge_timezone_label.set_text(self.api['config']['timezone'])

        self.bridge_address_label = builder.get_object('bridge-address')
        if bridge.ip == self.api['config']['ipaddress']:
            self.bridge_address_label.set_text(bridge.ip)
        else:
            self.bridge_address_label.set_text(
                '{host} ({ip})'.format(
                    host=bridge.ip,
                    ip=self.api['config']['ipaddress']
                )
            )

        self.network_connection_label = builder.get_object('connection-details')
        self.network_connection_label .set_text(
            '{gw} / {nm}'.format(
                gw=self.api['config']['gateway'],
                nm=self.api['config']['netmask']
            )
        )

        self.bridge_mac_address_label = builder.get_object('bridge-mac-address')
        self.bridge_mac_address_label.set_text(self.api['config']['mac'])

        self.bridge_dhcp_label = builder.get_object('bridge-dhcp')
        self.bridge_dhcp_label.set_text(
            'Yes' if self.api['config']['dhcp'] else 'No'
        )

        self.software_version_label = builder.get_object('software-version')
        self.software_version_label.set_text(self.api['config']['swversion'])

        self.api_version_label = builder.get_object('api-version')
        self.api_version_label.set_text(self.api['config']['apiversion'])

        self.add(self.content)

    def _on_rescan_clicked(self, *args):
        print('not implemented')

    def _on_update_clicked(self, *args):
        print('not implemented')
