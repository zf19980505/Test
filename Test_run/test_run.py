import unittest
import os

case_path = os.path.abspath(os.path.join(os.getcwd(), "../Test_case"))
# test_dir = '/.'
Login_discover = unittest.defaultTestLoader.discover(case_path, pattern='Login*', top_level_dir=None)
activity_discover = unittest.defaultTestLoader.discover(case_path, pattern='activity*', top_level_dir=None)
discover = [Login_discover, activity_discover]


if __name__ == '__main__':
    # unittest.main()
    Test_runner = unittest.TextTestRunner()
    for i in discover:
        Test_runner.run(i)
