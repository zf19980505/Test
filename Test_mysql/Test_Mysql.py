import pymysql


class Test_sql:
    def test_01(self):
        # a = ['hyg_db1', 'hyg_db2', 'hyg_db3', 'hyg_db4']
        a = ['yjr_db1']
        for aaaa in a:
            conn = pymysql.connect(host='47.110.11.166', user="root", password="123456", database=aaaa, port=3306,
                                   charset='utf8mb4')
            cursor = conn.cursor()
            # todo 不是购物车
            order_sql = 'SELECT oi.order_sn,oi.size FROM `t_refund` re INNER JOIN tb_order_info oi on re.order_sn = oi.order_sn where oi.attr01_value != "购物车"'
            cursor.execute(order_sql)
            yijiaren_results = cursor.fetchall()
            for i in yijiaren_results:
                refund_updates = f"UPDATE t_refund SET goods_size = '{i[1]}' WHERE order_sn = '{i[0]}'"
                cursor.execute(refund_updates)
                conn.commit()

            # todo 购物车
            goods_order_sql = 'SELECT re.id, re.order_sn, re.goodsNumber FROM `t_refund` re INNER JOIN tb_order_info oi on re.order_sn = oi.order_sn where oi.attr01_value = "购物车"'
            orde_goods = 'SELECT og.order_sn,og.size, og.skuId from tb_order_goods og'
            cursor.execute(orde_goods)
            yijiaren_results = cursor.fetchall()
            # print(yijiaren_results)
            # self.lis_key = []
            # self.lis_val = []
            goods_size = {}  # key: order_sn  value: {'skuId': [size, ]}
            use_order_sn = {}  # key: order_sn  value: index

            for refunds in yijiaren_results:
                if goods_size.get(refunds[0]):
                    if goods_size[refunds[0]].get(refunds[2]):
                        goods_size[refunds[0]][refunds[2]].append(refunds[1])
                    else:
                        goods_size[refunds[0]][refunds[2]] = [refunds[1]]
                else:
                    goods_size[refunds[0]] = {}
                    goods_size[refunds[0]][refunds[2]] = [refunds[1]]

            # print(goods_size)
            cursor.execute(goods_order_sql)
            yijiaren_results = cursor.fetchall()
            # print(yijiaren_results)
            for i in yijiaren_results:
                if use_order_sn.get(i[1]):
                    size_index = use_order_sn[i[1]]
                    size = goods_size[i[1]][i[2]][size_index]
                    refund_updates = f"UPDATE t_refund SET goods_size = '{ size }' WHERE id = '{i[0]}'"
                    if (use_order_sn[i[1]]+1) != len(goods_size[i[1]]):  # 判断size长度如果等于index, 下标就不+=1
                        use_order_sn[i[1]] += 1
                    cursor.execute(refund_updates)
                    conn.commit()
                else:
                    use_order_sn[i[1]] = 0
                    size = goods_size[i[1]][i[2]][0]
                    refund_updates = f"UPDATE t_refund SET goods_size = '{size}' WHERE id = '{i[0]}'"
                    cursor.execute(refund_updates)
                    conn.commit()
            cursor.close()
            conn.close()


if __name__ == '__main__':
    Test_sql().test_01()
    # a = {}
    # a['1'] = {}
    # a['1']['2'] = 1
    # print(a)