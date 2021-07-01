import sys
sys.path.insert(0, "../api")

import os
import unittest
import security_tests


if __name__ == '__main__':
    suites = [unittest.TestLoader().loadTestsFromModule(security_tests), ]

    for suite in suites:
        unittest.TextTestRunner(verbosity=2).run(suite)
