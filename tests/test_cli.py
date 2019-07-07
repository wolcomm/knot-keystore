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
"""knot_keystore cli module tests."""

import unittest.mock

import pytest

from knot_keystore.archive import get_plugins
from knot_keystore.cli import main


class TestCli(object):
    """CLI test class."""

    @pytest.mark.parametrize("plugin", get_plugins())
    @pytest.mark.parametrize("operation", ("archive", "retrieve"))
    def test_cli(self, plugin, operation):
        """Test CLI."""
        args = ["knot-keystore", "--plugins", plugin]
        if operation == "retrieve":
            args.append("--retrieve")
        with unittest.mock.patch("sys.argv", args):
            retval = main()
        assert retval == 0
