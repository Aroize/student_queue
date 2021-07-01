import sys
sys.path.insert(0, "../api")

import os
import unittest
import security


if __name__ == '__main__':
    suits = [unittest.TestLoader().loadTestsFromModule(security), ]

    print(suits)

    for suite in suits:
        unittest.TextTestRunner(verbosity=2).run(suite)
