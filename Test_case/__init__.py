import unittest
from ddt import ddt, file_data


@ddt
class Test(unittest.TestCase):
    @file_data('../Data/xcx_group.yaml')
    def test_0(self, **kwargs):
        xcx_el_data = kwargs['xcx_el_data']
        test_Lis = list(xcx_el_data['xcx_keyboard'].split(','))


if __name__ == '__main__':
    unittest.main()
