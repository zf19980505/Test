import pymysql


class Mysql:
    def __init__(self, project):
        self.conn = pymysql.connect(host='47.110.11.166', user="root", password="123456", database=project, port=3306,
                                    charset='utf8mb4')

    def mysql_delete(self, sql):
        sql_result = self.conn.cursor().execute(sql)
        self.conn.commit()
        return sql_result

    def close_mysql(self):
        self.conn.cursor().close()
        self.conn.close()
