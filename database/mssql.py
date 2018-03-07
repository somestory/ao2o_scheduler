# -*- coding: utf-8 -*-

import pymssql

import logging
logger = logging.getLogger(__name__)

class Mssql:

    config = {
        'server': '127.0.0.1',
        'port': '1433',
        'user': 'user',
        'password': 'passwd',
        'database': 'database',
        'charset': 'utf8',
        'as_dict': True
    }
    conn = None
    cursor = None
    sql = ''

    # 초기화
    def __init__(self, config):
    #   self.conn = pymssql.connect(server='127.0.0.1', database='database', user='user', password='passwd', charset='utf8')
    #   self.cursor = self.conn.cursor()
    #   self.connect()
        if False:
            print("config.server = ", config['server'])
            print("config.port = ", config['port'])
            print("config.user = ", config['user'])
            print("config.password = ", config['password'])
            print("config.database = ", config['database'])

        self.config = config

    # Database 접속
    def connect(self):
        if not self.conn:
            self.conn = pymssql.connect(**self.config)
            self.cursor = self.conn.cursor()

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
        sql = "SELECT TOP 10 * FROM foo"
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

