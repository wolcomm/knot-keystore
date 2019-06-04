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

import knot_keystore.cli  # noqa


class TestCli(object):
    """Test class."""

    def test_cli(self):
        """Dummy test."""
        retval = knot_keystore.cli.main()
        assert retval == 0
