import os
import unittest
import security


if __name__ == '__main__':
    suits = [unittest.TestLoader().loadTestsFromModule(security), ]

    for suite in suits:
        unittest.TextTestRunner(verbosity=2).run(suite)
