# Copyright (c) 2019 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the MIT License
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""knot_keystore archive module."""

from __future__ import print_function
from __future__ import unicode_literals

import logging
import shutil

from knot_keystore.knot import Knot

log = logging.getLogger(__name__)


def get_plugins(name=None):
    """Find archive plugins."""
    log.debug("Trying to find available plugins")
    builtin = {"local": ArchiveLocal}
    plugins = builtin
    log.debug(f"Available plugins: {plugins}")
    if name is not None:
        log.debug(f"Trying to find class for {name} plugin")
        try:
            plugin = plugins[name]
            log.debug(f"Found class for {name} plugin: {plugin.__name__}")
            return plugin
        except KeyError as e:
            raise e
    return plugins.keys()


class ArchiveBase(object):
    """Base class for archive plugins."""

    def __init__(self, knotc_socket=None):
        """Initialise a new instance."""
        log.debug(f"Initialising archive plugin instance {self}")
        self._knotc_socket = knotc_socket
        self._archive_path = None

    @property
    def knotc_socket(self):
        """Get knotc_socket property."""
        return self._knotc_socket

    @property
    def archive_path(self):
        """Get archive_path property."""
        return self._archive_path

    def create_archive(self):
        """Create an archive of the knot kasp-db."""
        log.debug("Preparing to create temporary kasp-db archive")
        with Knot(socket=self._knotc_socket) as knot:
            storage_path, kaspdb_dir = knot.kaspdb_path
            with knot.freeze():
                log.debug("Trying to create temporary kasp-db archive")
                self._archive_path = shutil.make_archive(base_name="kasp-db",
                                                         format="gztar",
                                                         root_dir=storage_path,
                                                         base_dir=kaspdb_dir)
                log.debug(f"Created temporary archive: {self.archive_path}")
        return


class ArchiveLocal(ArchiveBase):
    """Archive knot kasp-db to local filesystem."""

    pass
