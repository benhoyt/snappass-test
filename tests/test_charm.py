# Copyright 2021 Ben
# See LICENSE file for licensing details.

import unittest

from ops.testing import Harness
from charm import SnappassTestCharm


class TestCharm(unittest.TestCase):
    # TODO: add actual tests
    def test_nothing(self):
        harness = Harness(SnappassTestCharm)
        self.addCleanup(harness.cleanup)
        harness.begin()
        self.assertEqual(1, 1)
