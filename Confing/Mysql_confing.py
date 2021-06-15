import pymysql


class Mysql:
    def __init__(self, project):
        self.conn = pymysql.connect(host='47.111.190.18', user="root", password="123456", database=project, port=3306,
                                    charset='utf8mb4')

    def mysql_select(self, sql):
        sql_result = self.conn.cursor().execute(sql)
        return sql_result

    def mysql_commit(self, sql):
        try:
            sql_result = self.conn.cursor().execute(sql)
            self.conn.commit()
            return sql_result
        except Exception as e:
            print(e)
            # 数据回滚
            self.conn.rollback()

    def close_mysql(self):
        self.conn.cursor().close()
        self.conn.close()
