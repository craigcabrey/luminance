import os
import sys

from gi.repository import Gio

here = os.path.abspath(os.path.dirname(__file__))

RESOURCE_PREFIX = '/com/craigcabrey/luminance'
__version__ = '0.1.0'

if os.path.exists(os.path.join(here, '../data')):
    DATA_DIR = os.path.abspath(os.path.join(here, '../data'))
else:
    DATA_DIR = os.path.join(sys.prefix, 'share/luminance')

Gio.Resource._register(
    Gio.Resource.load(
        os.path.abspath(
            os.path.join(
                DATA_DIR,
                'resources.gresource'
            )
        )
    )
)

def get_resource_path(resource):
    return '{prefix}/{resource}'.format(
        prefix=RESOURCE_PREFIX, resource=resource
    )

del here
del os
del sys
