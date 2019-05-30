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
"""knot_keystore knot module."""

from __future__ import print_function
from __future__ import unicode_literals

import contextlib
import os
import time

import libknot.control


class Knot(object):
    """A knot-dns control object."""

    def __init__(self, socket=None, storage_path="/var/lib/knot"):
        """Intitialise a new instance."""
        self.socket = socket
        self.storage_path = storage_path
        self.ctl = libknot.control.KnotCtl()

    def __enter__(self):
        """Enter connection context."""
        try:
            self.ctl.connect(self.socket)
        except Exception as e:
            raise e
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit connection context."""
        self.ctl.send(libknot.control.KnotCtlType.END)
        self.ctl.close()
        return None

    def _cmd(self, cmd=None):
        """Send a control command and return a result."""
        self.ctl.send_block(cmd)
        return self.ctl.receive_block()

    @property
    def zone_status(self):
        """Get operational zone status."""
        return self._cmd(cmd="zone-status")

    @property
    def config(self):
        """Read the running config from knot."""
        return self._cmd(cmd="conf-read")

    @property
    def kaspdb_path(self):
        """Find the path to the kasp-db directory."""
        config = self.config
        try:
            storage = config["template"]["default"]["storage"]
        except KeyError:
            storage = self.storage_path
        try:
            kasp_db = config["template"]["defaut"]["kasp-db"]
        except KeyError:
            kasp_db = "keys"
        if not kasp_db.startswith("/"):
            kasp_db = os.path.join(storage, kasp_db)
        return os.path.split(kasp_db)

    @contextlib.contextmanager
    def freeze(self):
        """Freeze zone operations."""
        self._cmd(cmd="zone-freeze")
        while True:
            time.sleep(1)
            for s in self.zone_status.values():
                if s["freeze"] != "yes":
                    continue
            break
        try:
            yield
        finally:
            self._cmd(cmd="zone-thaw")
