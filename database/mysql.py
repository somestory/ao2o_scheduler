# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import errorcode

import logging
logger = logging.getLogger(__name__)

class Mysql:

    config = {
        'host': '127.0.0.1',
        'port': '3306',
        'user': 'user',
        'password': 'passwd',
        'database': 'database',
        'charset': 'utf8',
        'raise_on_warnings': True
    }

    conn = None
    cursor = None
    sql = ''

    # 초기화
    def __init__(self, config):
        if False:
            print("config.host = ", config['host'])
            print("config.port = ", config['port'])
            print("config.user = ", config['user'])
            print("config.password = ", config['password'])
            print("config.database = ", config['database'])

        self.config = config

    # Database 접속
    def connect(self):
        if not self.conn:
            try:
                self.conn = mysql.connector.connect(**self.config)
                self.cursor = self.conn.cursor()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
            else:
            #   self.conn.close()
                pass
            print("self.connect() self.conn = ", self.conn)

    # Database 접속 해제
    def disconnect(self):
        if self.conn:
            self.conn.close()

    # Database 접속 해제
    def close(self):
        if self.conn:
            self.conn.close()

    def query(self, query):
        logger.info('ModelBase.query: query = ', query)
        if not self.conn:
            self.connect()
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
    #   self.conn.close()
    #   for row in rows:
    #       logger.info(row)
        return rows

    def list(self):
        sql = "SELECT * FROM foo LIMIT 10"
        logger.info('sql = ', sql)
        if not self.conn:
            self.connect()
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
    #   self.conn.close()
        return row

    def select(self, query):
        if not self.conn:
            self.connect()
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
    #   self.conn.close()
        return rows

    def selectone(self, query):
        logger.info('ModelBase.selectone: query = ', query)
        if not self.conn:
            self.connect()
        self.cursor.execute(query)
        row = self.cursor.fetchone()
    #   self.conn.close()
        return row

    def execute(self, query):
        logger.info('ModelBase.selectone: execute = ', query)
        if not self.conn:
            self.connect()
        self.cursor.execute(query)
        self.conn.commit()
    #   self.conn.close()

    def insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

