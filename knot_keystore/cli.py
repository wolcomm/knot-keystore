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

import libknot.control


def main():
    """Execute knot-keystore cli utility."""
    knot_sock = "/run/knot/knot.sock"
    knot = libknot.control.KnotCtl()
    try:
        knot.connect(knot_sock)
    except Exception as e:
        raise e
