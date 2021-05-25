import unittest
from Test_case.Login_case import *
from Test_case.activity_case import *


class Test_Server(unittest.TestCase):
    # 实例化测试套件
    @classmethod
    def setUpClass(cls):
        print(1111111)
        cls.suite = unittest.TestSuite()

    def setUp(self):
        print(22222222222)
        self.suite.addTest(Login('test_open'))

    def tearDown(self):
        print(33333333333)
        self.suite.addTest(Login('test_over'))

    def test_groudcase(self):
        print(4444444444)
        self.suite.addTest(Activity_TestRun('test_newgroud'))


if __name__ == '__main__':
    # unittest.main()
    Test_runner = unittest.TextTestRunner()
    Test_runner.run(Test_Server())
