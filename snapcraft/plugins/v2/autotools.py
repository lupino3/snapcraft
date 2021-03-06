# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2020 Canonical Ltd
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

"""The autotools plugin is used for autotools based parts.

Autotools based projects are the ones that have the usual
`./configure && make && make install` instruction set.

This plugin will check for the existence of a 'configure' file, if one
cannot be found, it will run 'autoconf --install'.

This plugin uses the common plugin keywords as well as those for "sources".
For more information check the 'plugins' topic for the former and the
'sources' topic for the latter.

In addition, this plugin uses the following plugin-specific keywords:

    - configflags:
      (list of strings)
      configure flags to pass to the build such as those shown by running
      './configure --help'
"""

from typing import Any, Dict, List, Set

from snapcraft.plugins.v2 import PluginV2


class AutotoolsPlugin(PluginV2):
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        return {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "configflags": {
                    "type": "array",
                    "minitems": 1,
                    "uniqueItems": True,
                    "items": {"type": "string"},
                    "default": [],
                }
            },
        }

    def get_build_packages(self) -> Set[str]:
        return {"autoconf", "automake", "autopoint", "gcc", "libtool"}

    def get_build_environment(self) -> Dict[str, str]:
        return {"SNAPCRAFT_AUTOTOOLS_INSTALL_PREFIX": "/"}

    def get_build_commands(self) -> List[str]:
        configure_cmd = "./configure"
        if self.options.configflags:
            configflags = " ".join(self.options.configflags)
            configure_cmd = f"{configure_cmd} {configflags}"
        if not any(c.startswith("--prefix=") for c in self.options.configflags):
            configure_cmd = (
                f'{configure_cmd} --prefix="${{SNAPCRAFT_AUTOTOOLS_INSTALL_PREFIX}}"'
            )
        return [
            "[ ! -f ./configure ] && autoreconf --install",
            configure_cmd,
            'make -j"${SNAPCRAFT_PARALLEL_BUILD_COUNT}"',
            'make install DESTDIR="${SNAPCRAFT_PART_INSTALL}"',
        ]
