# ![icon](https://raw.githubusercontent.com/craigcabrey/luminance/master/data/icons/hicolor/48x48/apps/luminance.png) Luminance

Luminance is a Philips Hue client for Linux written in Python and GTK+.

![Screenshot of UI](https://raw.githubusercontent.com/craigcabrey/luminance/master/screenshot.png)

## Features

*Note*: The application is not release quality at this time. You will encounter
build issues, bugs, and incomplete or non-working features. That said, please
feel free to create an issue with your problem and I will do my best to triage
it.

* Individually control lights (brightness, color, on/off, effects)
* Manage and control individual groups (brightness, color, on/off, effects)
* Create new and modify existing groups (stored on the bridge, not on your computer)
* Bridge information and management (rescan for lights, check for updates)

## Getting Started

### Requirements

* autoconf 2.69 or later
* Python 3.5 or later (earlier versions may work, but they haven't been tested)
* GTK+ 3.18 or later (earlier versions may work, but they haven't been tested)
* [phue](https://github.com/studioimaginaire/phue) 0.8 or later
* [netdisco](https://github.com/home-assistant/netdisco) 0.7 or later
* [requests](https://github.com/kennethreitz/requests) 2.10 or later
* Hue bridge (tested with the first generation only)

### Installing

1. Clone this repository.
1. In the cloned repository, run `./autogen.sh`.
1. If everything works, run `./configure --prefix=/usr && make && sudo make install`.

## License

Copyright (C) 2016 Craig Cabrey

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
