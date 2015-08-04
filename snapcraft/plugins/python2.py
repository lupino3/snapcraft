# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2015 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import snapcraft
from snapcraft.plugins import ubuntu


class Python2Plugin(snapcraft.BasePlugin):

    def __init__(self, name, options):
        super().__init__(name, options)

        class UbuntuOptions:
            package = "python-dev"
        self.ubuntu = ubuntu.UbuntuPlugin(name, UbuntuOptions())

    # note that we don't need to set PYTHONHOME here,
    # python discovers this automatically from it installed
    # location.  And PATH is automatically set by snapcraft.

    def pull(self):
        return self.ubuntu.pull()

    def build(self):
        return self.ubuntu.build()

    def snap_files(self):
        return self.ubuntu.snap_files()
