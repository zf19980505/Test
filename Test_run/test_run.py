import unittest
import os

case_path = os.path.abspath(os.path.join(os.getcwd(), "../Test_case"))
# test_dir = '/.'
discover = unittest.defaultTestLoader.discover(case_path, pattern='*_case.py', top_level_dir=None)


if __name__ == '__main__':
    # unittest.main()
    Test_runner = unittest.TextTestRunner()
    Test_runner.run(discover)
