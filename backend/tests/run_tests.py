import os
import unittest
import security_tests


if __name__ == '__main__':
    # fixes import errors when running from console or pre-push hook
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../'
    os.chdir(CURRENT_PATH)

    suites = [unittest.TestLoader().loadTestsFromModule(security_tests), ]

    failed = False
    for suite in suites:
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful():
            failed = True

    if failed:
        exit(1)
