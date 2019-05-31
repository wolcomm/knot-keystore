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
"""knot_keystore cli module."""

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging

from knot_keystore.archive import get_plugins

log = logging.getLogger(__name__)


def parse_args():
    """Parse command line args."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--socket", "-s",
                        default="/run/knot/knot.sock",
                        help="path to knotc control socket")
    parser.add_argument("--plugin", "-p",
                        choices=get_plugins(),
                        default="local",
                        help="select archival plugin")
    parser.add_argument("-v", dest="verbosity",
                        default=0,
                        action="count",
                        help="increase output verbosity")
    args = parser.parse_args()
    return args


def set_loglevel(verbosity=0):
    """Set logging level."""
    level = 40 - (verbosity * 10)
    logging.basicConfig(level=level)
    return


def main():
    """Execute knot-keystore cli utility."""
    try:
        args = parse_args()
        set_loglevel(verbosity=args.verbosity)
        archive_plugin = get_plugins(name=args.plugin)
        archive = archive_plugin(knotc_socket=args.socket)
        archive.exec()
    except KeyboardInterrupt:
        log.error("Caught keyboard interrupt: aborting")
        return 130
    except Exception as e:
        log.error(f"An error occurred during execution: {e}")
        return 1
    return 0
