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

import functools
import logging
import os
import shutil
import stat
import tempfile

from cryptography.fernet import Fernet

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


def with_encrypted_archive(func):
    """Wrap the decorated function with archival and encryption."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        log.debug("Generating symetric encryption key")
        key = Fernet.generate_key()
        cipher = Fernet(key)
        log.debug("Creating temp directory")
        with tempfile.TemporaryDirectory() as tmp_path:
            log.debug(f"Working in {tmp_path}")
            cleartext_path = self.get_cleartext_archive(tmp_path)
            ciphertext_path = f"{cleartext_path}.enc"
            log.debug("Trying to open cleartext archive for reading")
            try:
                with open(cleartext_path, "rb") as cleartext_file:
                    cleartext = cleartext_file.read()
            except Exception as e:
                log.error(f"Failed to read cleartext archive: {e}")
                raise e
            log.debug("Trying to encrypt archive")
            try:
                ciphertext = cipher.encrypt(cleartext)
            except Exception as e:
                log.error(f"Failed to encrypt archive: {e}")
                raise e
            log.debug("Trying to open ciphertext archive for writing")
            try:
                with open(ciphertext_path, "wb") as ciphertext_file:
                    ciphertext_file.write(ciphertext)
            except Exception as e:
                log.error(f"Failed to write cyphertext archive: {e}")
                raise e
            log.debug("Trying to call wrapped method")
            try:
                return func(self, *args, **kwargs,
                            ciphertext_path=ciphertext_path,
                            key=key)
            except Exception as e:
                log.error(f"Error during call to wrapped method: {e}")
                raise e
    return wrapper


class ArchiveBase(object):
    """Base class for archive plugins."""

    def __init__(self, knotc_socket=None, config=None):
        """Initialise a new instance."""
        log.debug(f"Initialising archive plugin instance {self}")
        self._knotc_socket = knotc_socket
        if config is not None:
            for k, v in config.items():
                setattr(self, k, v)

    @property
    def knotc_socket(self):
        """Get knotc_socket property."""
        return self._knotc_socket

    def exec(self, ciphertext_path=None, key=None):  # pragma: no cover
        """Execute archival proceedure, overide in child classes."""
        raise NotImplementedError

    def get_cleartext_archive(self, tmp_path):
        """Create an archive of the knot kasp-db."""
        log.debug("Preparing to create temporary kasp-db archive")
        base_name = os.path.join(tmp_path, "kasp-db")
        with Knot(socket=self.knotc_socket) as knot:
            storage_path, kaspdb_dir = knot.kaspdb_path
            with knot.freeze():
                log.debug("Trying to create temporary kasp-db archive")
                try:
                    path = shutil.make_archive(base_name=base_name,
                                               format="gztar",
                                               root_dir=storage_path,
                                               base_dir=kaspdb_dir)
                except Exception as e:
                    log.error(f"Failed to create temp kasp-db archive: {e}")
                    raise e
                log.debug(f"Created temporary archive: {path}")
        return path


class ArchiveLocal(ArchiveBase):
    """Archive knot kasp-db to local filesystem."""

    @with_encrypted_archive
    def exec(self, ciphertext_path=None, key=None):
        """Execute archival proceedure."""
        log.debug(f"Trying to save encrypted archive to {self.path}")
        try:
            archive_path = shutil.copy(src=ciphertext_path, dst=self.path)
        except Exception as e:
            log.error(f"Failed to copy encrypted archive from \
                        {ciphertext_path}: {e}")
            raise e
        log.info(f"Encrypted archive written to {archive_path}")
        key_path = os.path.join(self.path, "kasp-db.key")
        log.debug("Trying to write encryption key to file")
        try:
            with open(key_path, "wb") as key_file:
                key_file.write(key)
            os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
        except Exception as e:
            log.error(f"Failed to write encryption key to file: {e}")
            raise e
        log.info(f"Encryption key written to {key_path}")
        return
