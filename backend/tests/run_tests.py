import sys
sys.path.insert(0, "../api")
sys.path.insert(0, "backend/api")

import os
import unittest
import security_tests


if __name__ == '__main__':
    suites = [unittest.TestLoader().loadTestsFromModule(security_tests), ]

    failed = False
    for suite in suites:
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful():
            failed = True

    if failed:
        exit(1)
