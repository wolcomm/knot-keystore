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
import shutil

from knot_keystore.knot import Knot


def parse_args():
    """Parse command line args."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--socket", "-s",
                        default="/run/knot/knot.sock",
                        help="path to knotc control socket")
    args = parser.parse_args()
    return args


def main():
    """Execute knot-keystore cli utility."""
    args = parse_args()
    with Knot(socket=args.socket) as knot:
        storage, kaspdb = knot.kaspdb_path
        with knot.freeze():
            archive = shutil.make_archive(base_name="keys", format="gztar",
                                          root_dir=storage, base_dir=kaspdb)
            print(archive)
    return
