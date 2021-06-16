import xlrd


class Data_conversion:
    def __init__(self):
        self.lis_value = []
        self.lis_key = []

    # 传入yaml文件里的数据，通过循环然后把value值转成tuple
    def str_by_tuple(self, data):
        for data_key, data_value in dict.items(data):
            self.lis_key.append(data_key)
            str_data = data_value[1: -1]
            str_data_one, str_data_two = str_data.split(',')
            self.tuple_data = (str_data_one, str_data_two)
            self.lis_value.append(self.tuple_data)
        self.zip_obj = zip(self.lis_key, self.lis_value)
        self.dict_data = dict(self.zip_obj)
        return self.dict_data

    # 传入yaml文件里的数据，通过循环然后把value值转成lis
    def str_lis(self, data):
        for data_key, data_value in dict.items(data):
            self.lis_key.append(data_key)
            str_data = data_value[1: -1]
            x1, y1, x2, y2 = str_data.split(',')
            size = [x1, y1, x2, y2]
            self.lis_value.append(size)
        self.zip_obj = zip(self.lis_key, self.lis_value)
        self.dict_data = dict(self.zip_obj)
        return self.dict_data

    # 读取xls表格的内容
    def read_xls(self, xls_data):
        readbook = xlrd.open_workbook(r'' + xls_data)
        sheet = readbook.sheet_by_index(0)  # 索引的方式，从0开始
        ncol_value = sheet.col_values(0)
        return ncol_value[1:]