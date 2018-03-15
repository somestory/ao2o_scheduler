# ao2o_scheduler

## 개요

ao2o_scheduler는 아마노코리아 O2O 서비스에서 사용하는 프로그램으로 지정된 시간에 작업을 수행하는 스케쥴러입니다.

1. 현장 정보를 동기화하는 작업을 수행합니다.
2. 정기권 만기 안내를 카카오 알림톡으로 자동 전송하는 작업을 수행합니다.

스케쥴의 지정은 main.py 소스 안에 schedule_site 와 schedule_alrimtalk 에 값을 설정하여 지정합니다.

## 개발언어
python 3.6

## 프로그램 실행
1. 기본으로 실행할 때
  - python main.py
2. 백그라운드로 실행할 때
  - nohup python main.py > /dev/null &

