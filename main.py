# -*- coding: utf-8 -*-

import json, time, datetime
#from datetime import date, time, timedelta
from datetime import date, timedelta
from pytz import timezone

import mysql.connector
#from mysql.connector import connection
from mysql.connector import errorcode

from site_sync import SiteSync
from alrimtalk import AlrimTalk

print('** 스케쥴러 시작 **')

# 현장정보 동기화 시간 설정
schedule_site = {
    "hour": 2,
    "minute": 30,
    "old_hour": 60,
    "old_minute": 60,
    "enabled": True
}

# 정기권 알림톡 발송 시간 설정
schedule_alrimtalk = {
    "hour": 2,
    "minute": 30,
    "old_hour": 60,
    "old_minute": 60,
    "enabled": False
}

interval = 1
time.sleep(interval)

old_hour = 60
old_min = 60

test_mode = False

# 테스트 모드이면 스케쥴 시간을 현재 시간 + 1분으로 설정한다.
if test_mode:
    now = datetime.datetime.now()
    schedule_site['hour'] = now.hour
    schedule_site['minute'] = now.minute + 1
    schedule_alrimtalk['hour'] = now.hour
    schedule_alrimtalk['minute'] = now.minute + 1

print("현장정보 동기화 시간 : {:02d}:{:02d}".format(schedule_site['hour'], schedule_site['minute']))
print("정기권 알림톡 발송 시간 : {:02d}:{:02d}".format(schedule_alrimtalk['hour'], schedule_alrimtalk['minute']))

while True:
    time.sleep(interval)
    now = datetime.datetime.now()
    print(now)

    # 매시 정각 체크
    if now.minute == 0:
        if now.hour != old_hour:
            old_hour = now.hour
            time_index = now.hour % 12
            print('시간 변경됨....')

            if time_index == 0:
                print("12시....")

    # 매분 정각 체크
    if now.second == 0:
        if now.minute != old_min:
            old_min = now.minute
            print('분 변경됨....')

    # 매일 새벽 2시에 정기권 만기자 알림톡 발송
    if now.minute == 0:
        if now.hour != schedule_alrimtalk['old_hour']:
            schedule_alrimtalk['old_hour'] = now.hour

            if now.hour == schedule_alrimtalk['hour']:
                print('정기권 만기자 알림톡 발송....')

    # 현장정보 동기화 스케쥴 처리
    if now.second == 0:
        if now.minute != schedule_site['old_minute']:
            schedule_site['old_minute'] = now.minute
            print("현장정보 동기화 시간 : {}:{}".format(schedule_site['hour'], schedule_site['minute']))
            print("현재 시간 : {}:{}".format(now.hour, now.minute))
            if now.hour == schedule_site['hour'] and now.minute == schedule_site['minute']:
                print('현장정보 동기화....')
                if schedule_site['enabled']:
                    siteSync = SiteSync()
                    siteSync.run()

                # 테스트 모드이면 현장정보 동기화 시간을 현재 시간 + 1분으로 설정한다.
                if test_mode:
                    now = datetime.datetime.now()
                    schedule_site['hour'] = now.hour
                    schedule_site['minute'] = now.minute + 1
                    print("현장정보 동기화 시간 : {:02d}:{:02d}".format(schedule_site['hour'], schedule_site['minute']))

    # 정기권 알림톡 발송 스케쥴 처리
    if now.second == 0:
        if now.minute != schedule_alrimtalk['old_minute']:
            schedule_alrimtalk['old_minute'] = now.minute
            print("정기권 알림톡 발송 시간 : {}:{}".format(schedule_alrimtalk['hour'], schedule_alrimtalk['minute']))
            print("현재 시간 : {}:{}".format(now.hour, now.minute))
            if now.hour == schedule_alrimtalk['hour'] and now.minute == schedule_alrimtalk['minute']:
                print('정기권 만기자 알림톡 발송....')
                if schedule_alrimtalk['enabled']:
                    alrimtalk = AlrimTalk()
                    alrimtalk.run()

                # 테스트 모드이면 알림톡 스케쥴 시간을 현재 시간 + 1분으로 설정한다.
                if test_mode:
                    now = datetime.datetime.now()
                    schedule_alrimtalk['hour'] = now.hour
                    schedule_alrimtalk['minute'] = now.minute + 1
                    print("정기권 알림톡 발송 시간 : {:02d}:{:02d}".format(schedule_alrimtalk['hour'], schedule_alrimtalk['minute']))

