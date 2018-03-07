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

# ao2o DB 정보 (실제 정보로 변경할 것)
config_ao2o = {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'user',
    'password': 'password',
    'database': 'ao2o',
    'raise_on_warnings': True,
}

# fc_master DB 정보 (실제 정보로 변경할 것)
config_fc_master = {
    'server': '127.0.0.1',
    'port': '1433',
    'user': 'user',
    'password': 'password',
    'database': 'fc_master',
    'charset': 'utf8',
    'as_dict': True
}

# 알림톡 발송 모듈
class AlrimTalk:
    def __init__(self):
        print('** 알림톡 발송 초기화 **')
        pass

    def run(self):
        print('** 알림톡 발송 실행 **')
        pass

        # 1. 알림톡 대상 기간 시작일과 종료일을 설정한다.
        # 2. 정기권 만기 대상이 현재 기준 10일 이내이며, 알림톡 발송이 설정되어 있는 데이터만 추출한다.
        # 3. 알림톡 발송한다.

        today = datetime.date.today()
        start_date = date.today() - datetime.timedelta(days=7)
        end_date = date.today() + datetime.timedelta(days=10)

        start_date = "{}-{}-{}".format(start_date.year, start_date.month, start_date.day)
        end_date = "{}-{}-{}".format(end_date.year, end_date.month, end_date.day)

        print("만기 기간 : {} ~ {}".format(start_date, end_date))
        areacode = ''
        self.alrim(start_date, end_date, areacode)


    #   self.mysql_test()


    def mysql_test(self):
        query = "SELECT * FROM areadef LIMIT 10"
        cnx_mysql = Mysql(config_ao2o)
        rows = cnx_mysql.query(query)
        for row in rows:
            print(row)
        cnx_mysql.disconnect()


    def alrim(self, start_date, end_date, area_code):

        user_name = ''
        car_number = ''

        print('start_date = ', start_date)
        print('end_date = ', end_date)
        print('area_code = ', area_code)
        print('car_number = ', car_number)
        print('user_name = ', user_name)


        # 검색식 생성
        query = ""
        query += "SELECT TOP 2000 "
        query += "cc.*, aa.acLotAreaName1, kk.iKakao "
        query += "FROM custdef cc "
        query += "JOIN areadef aa ON cc.iLotArea = aa.iLotArea "
        query += "LEFT OUTER JOIN kakao kk ON cc.iLotArea = kk.iLotArea AND cc.iUser = kk.iUser "
        query += "WHERE 1=1 "
        query += " AND kk.iKakao > 0 "
        if area_code == '':
            pass
        #   query += "  AND cc.iLotArea IN (51, 61) "
        else:
            query += "  AND cc.iLotArea = {} ".format(area_code)
        if car_number != '':
            query += " AND cc.acPlate1 LIKE '%{}%' ".format(car_number)
        if user_name != '':
            query += " AND cc.acUserName LIKE '%{}%' ".format(user_name)
        if (user_name != '' or car_number != '') and 0:
            query += "AND ("
            if user_name != '':
                query += " cc.acUserName LIKE '%{}%' ".format(user_name)
            if car_number != '':
                if user_name != '':
                    query += " OR "
                query += " cc.acPlate1 LIKE '%{}%' ".format(car_number)
            query += ") "
        if start_date != '':
            query += " AND cc.dtValidEndDate >= '{}' ".format(str(start_date))
        if end_date != '':
            query += " AND cc.dtValidEndDate <= '{}' ".format(str(end_date))
        query += " AND cc.dtValidEndDate IS NOT NULL "
    #   query += " AND cc.acPlate1 IS NOT NULL "
    #   query += " AND cc.acPlate1 <> '' "
        query += " OR cc.acPlate1 = '48수4022' "
        query += " ORDER BY acPlate1, dtValidEndDate "
        print('query = ' + query)

        cnx_mysql = Mysql(config_ao2o)
        cnx_mssql = Mssql(config_fc_master)

        rows = cnx_mssql.query(query)

        # 발송 날자시간 확인 (utc 시간으로 변환한다.)
        send_time = datetime.datetime.now().astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
        cnt = 0
        for row in rows:
            if row['iKakao'] == None or row['iKakao'] == 0:
                row['iKakao'] = '--'
            else:
                row['iKakao'] = '발송'
            if row['acPlate1'] == '48수4022':
                row['acTelNo2'] = '010-6212-9897'
                row['acTelNo2'] = '010-9701-3500'

            row['acTelNo2'] = '010-9701-3500'

            phone_no = format(row['acTelNo2'])
            phone_no = phone_no.replace(' ', '')
            phone_no = phone_no.replace('-', '')
            phone_no = phone_no.replace('.', '')
            phone_no = phone_no.replace('/', '')
            print("정기권 고객:", row['acUserName'], phone_no)

            # acrm000011 - 정기권 만기 안내 + 버튼
            query = ""
            query += "INSERT INTO ata_mmt_tran (date_client_req, template_code, content, recipient_num, msg_status, subject, callback, sender_key, msg_type, etc_text_1, etc_text_2, etc_text_3, attachment_type, attachment_name, attachment_url)"
            query += " VALUES ("
        #   query += "SYSDATE(),"
            query += "'{}',".format(send_time)
            query += "'acrm000011',"
            query += "'< 정기권 만기 안내 >\n\n"
            query += "안녕하세요. {}님\n\n".format(row['acUserName'])
            query += "정기권 만기 안내입니다.\n\n"
            query += "주차장 : {}\n".format(row['acLotAreaName1'])
            query += "정기권 만기일 : {}\n".format(row['dtValidEndDate'])
        #   query += "사용기간 : {} ~ {}\n\n".format(row['dtValidStartDate'], row['dtValidEndDate'])
            query += "\n* 감사합니다. *\n',"

            query += "'{}',".format(phone_no)
            query += "'1',"
            query += "'장애알림',"
            query += "'1899-7275',"
            query += "'----- alrimtalk 인증키를 적는다 -----',"
            query += "1008,"
            query += "'acrm',"
            query += "'관리자',"
            query += "'{}: {}',".format(row['acLotAreaName1'], row['acUserName'])
            query += "'button',"
            query += "'정기권 안내',"
            query += "'http://www.amanopark.co.kr/custdefpay/doViewMst'"
            query += ")"

            print("정기권 고객: query = ", query)
            cnx_mysql.execute(query)

            cnt += 1
            print(cnt, row)

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

