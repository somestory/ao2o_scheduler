# -*- coding: utf-8 -*-

import json, time, datetime
#from datetime import date, time, timedelta
from datetime import date, timedelta
import pytz

import mysql.connector
#from mysql.connector import connection
from mysql.connector import errorcode
from database.mysql import Mysql
from database.mssql import Mssql

# ao2o DB 정보
config_ao2o = {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'user',
    'password': 'pass',
    'database': 'ao2o',
    'raise_on_warnings': True,
}

# fc_master DB 정보
config_fc_master = {
    'server': '127.0.0.1',
    'port': '1433',
    'user': 'user',
    'password': 'pass',
    'database': 'fc_master',
    'charset': 'utf8',
    'as_dict': True
}

# 현장정보 동기화 모듈
class SiteSync:
    def __init__(self):
        print('** 현장정보 동기화 초기화 **')
        pass

    def run(self):
        print('** 현장정보 동기화 실행 **')
        pass

        # 1. 기존 현장을 disable 시킨다.
        # 2. 동기화 시간 설정
        # 3. fc_master.areadef 의 현장 목록을 가져 온다.
        # 4. ao2o.areadef 에 등록한다.

        cnx_mysql = Mysql(config_ao2o)
        cnx_mssql = Mssql(config_fc_master)

        # 기존 현장을 disable 시킨다.
        query = "UPDATE areadef SET enabled = 0"
        cnx_mysql.execute(query)

        # 동기화 시간 확인 (utc 시간으로 변환한다.)
        sync_utc_time = datetime.datetime.now().astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
        sync_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("sync_time = ", sync_time)

        # 검색식 생성
        query = "SELECT * FROM areadef "
        print('query = ' + query)

        rows = cnx_mssql.query(query)
        cnt = 0
        for row in rows:
            cnt += 1
            if row['acLotAreaName1'] == None:
                row['acLotAreaName1'] = ''
            if row['acLotAreaName2'] == None:
                row['acLotAreaName2'] = ''
            if row['acLotAreaInfo'] == None:
                row['acLotAreaInfo'] = ''
            if row['acCompanyPlace'] == None:
                row['acCompanyPlace'] = ''
            if row['acCompanyAddress'] == None:
                row['acCompanyAddress'] = ''
            if row['acZipCode1'] == None:
                row['acZipCode1'] = ''
            if row['acZipCode2'] == None:
                row['acZipCode2'] = ''
            if row['acTelNo'] == None:
                row['acTelNo'] = ''

            if row['acLotAreaName1'] == '' and row['acLotAreaName2'] != '':
                row['acLotAreaName1'] = row['acLotAreaName2']

        #   logger.info(row[0])
        #   print("row = ", row)

            query = "SELECT * FROM areadef WHERE id = {} AND iLotArea = {}".format(row['id'], row['iLotArea'])
            print("query = ", query)
            areas = cnx_mysql.query(query)
            if len(areas) == 0:
                print("신규 현장 정보")
                query = ""
                query += "INSERT INTO areadef ("
                query += " id"
                query += ", iLotArea"
                query += ", acLotAreaName1"
                query += ", acLotAreaName2"
                query += ", acLotAreaInfo"
                query += ", acCompanyPlace"
                query += ", acZipCode1"
                query += ", acZipCode2"
                query += ", acTelNo"
                query += ", last_sync_time"
                query += ", update_count"
                query += ", enabled"
                query += ") VALUES ("
                query += "{}".format(row['id'])
                query += ", {}".format(row['iLotArea'])
                query += ", '{}'".format(row['acLotAreaName1'])
                query += ", '{}'".format(row['acLotAreaName2'])
                query += ", '{}'".format(row['acLotAreaInfo'])
                query += ", '{}'".format(row['acCompanyPlace'])
                query += ", '{}'".format(row['acZipCode1'])
                query += ", '{}'".format(row['acZipCode2'])
                query += ", '{}'".format(row['acTelNo'])
                query += ", '{}'".format(sync_utc_time)
                query += ", {}".format(1)
                query += ", {}".format(1)
                query += ")"
            else:
                print("이미 등록된 현장 정보")
                query = ""
                query += "UPDATE areadef SET"
                query += " acLotAreaName1 = '{}'".format(row['acLotAreaName1'])
                query += ", acLotAreaName2 = '{}'".format(row['acLotAreaName2'])
                query += ", acLotAreaInfo = '{}'".format(row['acLotAreaInfo'])
                query += ", acCompanyPlace = '{}'".format(row['acCompanyPlace'])
                query += ", acZipCode1 = '{}'".format(row['acZipCode1'])
                query += ", acZipCode2 = '{}'".format(row['acZipCode2'])
                query += ", acTelNo = '{}'".format(row['acTelNo'])
                query += ", last_sync_time = '{}'".format(sync_utc_time)
                query += ", update_count = update_count + 1"
                query += ", enabled = 1"
                query += " WHERE "
                query += " id = {} AND iLotArea = {}".format(row['id'], row['iLotArea'])
            print("query[{}] = {}".format(cnt, query))
            cnx_mysql.execute(query)

        cnx_mysql.disconnect()
        cnx_mssql.disconnect()


if __name__ == "__main__":

    exit()

    try:
        cnx = mysql.connector.connect(**config_11)
        query = 'SELECT acLotAreaName1, acLotAreaInfo FROM areadef'
        cursor = cnx.cursor()
        cursor.execute(query)
        for (acLotAreaName1, acLotAreaInfo) in cursor:
            print("{} - {}".format(acLotAreaName1, acLotAreaInfo))
        cursor.close()

        for result in cnx.cmd_query_iter(query):
            if 'columns' in result:
                columns = result['columns']
                rows = cnx.get_rows()
                print("columns = {}\nrows = {}".format(columns, rows))
            else:
                print("Nothing data...");

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

