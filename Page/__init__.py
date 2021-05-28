from ddt import ddt, file_data
import unittest


@ddt
class Test_one(unittest.TestCase):
    # 传入yaml文件里的数据，通过循环然后把value值转成tuple
    def str_by_tuple(self, data):
        self.lis_key = []
        self.lis_value = []
        for data_key, data_value in dict.items(data):
            self.lis_key.append(data_key)
            str_data = data_value[1: -1]
            str_data_one, str_data_two = str_data.split(',')
            self.tuple_data = (str_data_one, str_data_two)
            self.lis_value.append(self.tuple_data)
        self.zip_obj = zip(self.lis_key, self.lis_value)
        self.dict_data = dict(self.zip_obj)
        return self.dict_data

    @file_data('../Data/activity.yaml')
    def test_one(self, **kwargs):
        # 活动管理
        activitys = kwargs['activitys']
        # 拼团活动
        grouds = activitys['grouds']
        # 新建拼团活动
        grouds_goods = grouds['grouds_goods']
        test_groud = self.str_by_tuple(grouds_goods)


if __name__ == '__main__':
    unittest.main()
