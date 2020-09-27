'''
import pymysql

def in_sql(company_name, recruit_type, professionals, job_recruitment, url_href, content):
    db = pymysql.connect(host='localhost', user='root', password='12345', port='3306')

    cursor = db.cursor()
    cursor.execute('CREATE DATABASE ncu DEFAULT CHARACTER SET utf8')
    sql = 'INSERT INTO company(company_name, recruit_type, professionals, job_recruitment, url_href, content) values(%s, %s, %s, %s, %s, %s)'
    #cursor.execute('CREATE DATABASE ncu DEFAULT CHARACTER SET utf8')
    try:
        cursor.execute(sql, (company_name, recruit_type, professionals, job_recruitment, url_href, content))
        db.commit()
    except:
        db.rollback()
    db.close()
    '''
"""
Desc: 自定义Mysql类
Date: 2019/11/08
Editor: liuxianglong
"""
import pymysql
import logging
import re
from pymysql.cursors import Cursor, DictCursor


class MysqlClient(object):
    def __init__(self, host, port, user, password, db, cursor=Cursor):
        self.host = host
        self.database = db
        self.user = user
        self.password = password
        self.port = port
        self.cursor = cursor
        self.connect = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.connect.cursor(self.cursor)   # 返回dict类型数据， 默认为Cursor是列表数据
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return True

    def test_connection(self):
        """测试mysql连接，如果异常，重新连接"""
        try:
            self.connect.ping()
        except:
            self.connect = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
            self.cursor = self.connect.cursor(self.cursor)

    def execute_cmd(self, command):
        """执行指令"""
        try:
            self.test_connection()
            self.cursor.execute(command)
            self.connect.commit()
            self.logger.debug('执行指令成功: %s' % command)
            return self.cursor
        except pymysql.err.ProgrammingError:
            self.logger.error('mysql命令语法错误, 指令: %s' % command, exc_info=True)
            return None
        except pymysql.err.IntegrityError:
            self.logger.error('重复值插入, 指令: %s' % command, exc_info=True)
            return None
        except pymysql.err.InternalError:
            self.logger.error('插入的值类型与mysql列类型不一致')
            return None

    def close(self):
        self.cursor.close()
        self.connect.close()

    def table_exists(self, table_name):
        """检查数据库下面是否存在数据表"""
        sql = "show tables;"
        self.cursor.execute(sql)
        tables = [self.cursor.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return True
        else:
            return False


#if __name__  == '__main__':
def in_sql(company_name, recruit_type, professionals, job_recruitment, url_href, content):
    sql = MysqlClient('localhost', 3306, 'root', '12345', 'ncu')

    #for i in range(1, len(name)):
        #name = "star war %d" % i
    cmd = 'insert into company values("%s", "%s", "%s", "%s", "%s", "%s")' % (company_name, recruit_type, professionals, job_recruitment, url_href, content)
        #cmd = 'insert into movie values("%s", "124", "55", "5s", "7s")' % str(i)
    sql.execute_cmd(cmd)

    # cmd = 'select * from movie'
    # result = sql.execute_cmd(cmd)
    # for item in result.fetchall():
