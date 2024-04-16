from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

from dataclasses import dataclass, field
from typing import List, Union

import time
from random import randint
import sys

# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import QSettings, QCoreApplication
# from PyQt5.QtGui import QIcon
# from PyQt5 import uic

from twilio.rest import Client
import schedule

# =============================================================================
# DATACLASS 
# =============================================================================
# Dataclass for User (input)
@dataclass
class UserData:
    username: str = None
    password: str = None
    input_dep_stn: str = '수서'
    input_arr_stn: str = '부산'
    input_date: int = None
    input_time: int = None
    input_train_num: Union[List[int]] = field(default_factory=list)
    input_seat_class: str = '일반실'
    input_seat_num: dict = None
    input_seat_select: str = '자동선택'
    want_standing_seat: bool = False
    want_queue: bool = False
    to_num: str = None

# =============================================================================
# SRT CLASS
# =============================================================================
class SRT():
    def __init__(self, user_data: UserData) -> None:
        self.__dict__.update(user_data.__dict__)

    def check_fn(self) -> None:
        # Execute Chromedriver
        chrome_options = Options() # chrome_options : close/keep the browser open
        chrome_options.add_experimental_option("detach", True) # detach : keep the browser open
        # service = Service(ChromeDriverManager().install())       
        # driver = webdriver.Chrome(service=service, chrome_options=chrome_options)
        driver = webdriver.Chrome(options=chrome_options)

        # Move to the login page
        driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')
        driver.implicitly_wait(15)
        
        # Login
        driver.find_element(By.ID, 'srchDvNm01').send_keys(username) # 회원번호
        driver.find_element(By.ID, 'hmpgPwdCphd01').send_keys(password) # 비밀번호
        driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]\
                            /div[2]/div/div[2]/input').click() # 확인버튼
        driver.implicitly_wait(5)
        
        # Move to train schedule page
        driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do')
        driver.implicitly_wait(5)
        
        # Input departure/arrival station
        dep_stn = driver.find_element(By.ID, 'dptRsStnCdNm') # 출발지
        arr_stn = driver.find_element(By.ID, 'arvRsStnCdNm') # 도착지
        dep_stn.clear() # default값 지우기
        arr_stn.clear()
        dep_stn.send_keys(input_dep_stn)
        arr_stn.send_keys(input_arr_stn)
        
        # Input departure date/time
        dep_date = driver.find_element(By.ID, 'dptDt') # 출발날짜
        dep_time = driver.find_element(By.ID, 'dptTm') # 출발시간
        # make the dropdown visible
        # driver.execute_script("arguments[0].setAttribute('style','display: True;')", dep_date)
        # driver.execute_script("arguments[0].setAttribute('style','display: True;')", dep_time)
        input_date_selected = Select(dep_date)
        input_time_selected = Select(dep_time)
        input_date_selected.select_by_value(str(input_date)) # 출발날짜 선택
        input_time_selected.select_by_visible_text(str(input_time)) # 출발시간 선택(by Visible Text) 

        # Input seat class/number
        seat_num_old = driver.find_element(By.NAME, 'psgInfoPerPrnb4') # 경로
        seat_num_normal = driver.find_element(By.NAME, 'psgInfoPerPrnb1') # 일반
        seat_num_old_selected = Select(seat_num_old)
        seat_num_normal_selected = Select(seat_num_normal)
        seat_num_old_selected.select_by_value(str(input_seat_num['경로']))
        seat_num_normal_selected.select_by_value(str(input_seat_num['일반']))

        # Click the search button
        search_btn = driver.find_element(By.XPATH, "//input[@value='조회하기']") # 조회버튼
        search_btn.click()
        driver.implicitly_wait(5)

    def reserve_fn():
        # Execute Chromedriver
        chrome_options = Options() # chrome_options : close/keep the browser open
        chrome_options.add_experimental_option("detach", True) # detach : keep the browser open
        # service = Service(ChromeDriverManager().install())       
        # driver = webdriver.Chrome(service=service, chrome_options=chrome_options)
        driver = webdriver.Chrome(options=chrome_options)

        # Move to the login page
        driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')
        driver.implicitly_wait(15)
        
        # Login
        driver.find_element(By.ID, 'srchDvNm01').send_keys(username) # 회원번호
        driver.find_element(By.ID, 'hmpgPwdCphd01').send_keys(password) # 비밀번호
        driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]\
                            /div[2]/div/div[2]/input').click() # 확인버튼
        driver.implicitly_wait(5)
        
        # Move to train schedule page
        driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do')
        driver.implicitly_wait(5)
        
        # Input departure/arrival station
        dep_stn = driver.find_element(By.ID, 'dptRsStnCdNm') # 출발지
        arr_stn = driver.find_element(By.ID, 'arvRsStnCdNm') # 도착지
        dep_stn.clear() # default값 지우기
        arr_stn.clear()
        dep_stn.send_keys(input_dep_stn)
        arr_stn.send_keys(input_arr_stn)
        
        # Input departure date/time
        dep_date = driver.find_element(By.ID, 'dptDt') # 출발날짜
        dep_time = driver.find_element(By.ID, 'dptTm') # 출발시간
        # make the dropdown visible
        # driver.execute_script("arguments[0].setAttribute('style','display: True;')", dep_date)
        # driver.execute_script("arguments[0].setAttribute('style','display: True;')", dep_time)
        input_date_selected = Select(dep_date)
        input_time_selected = Select(dep_time)
        input_date_selected.select_by_value(str(input_date)) # 출발날짜 선택
        input_time_selected.select_by_visible_text(str(input_time)) # 출발시간 선택(by Visible Text) 

        # Input seat class/number
        seat_num_old = driver.find_element(By.NAME, 'psgInfoPerPrnb4') # 경로
        seat_num_normal = driver.find_element(By.NAME, 'psgInfoPerPrnb1') # 일반
        seat_num_old_selected = Select(seat_num_old)
        seat_num_normal_selected = Select(seat_num_normal)
        seat_num_old_selected.select_by_value(str(input_seat_num['경로']))
        seat_num_normal_selected.select_by_value(str(input_seat_num['일반']))

        # Click the search button
        search_btn = driver.find_element(By.XPATH, "//input[@value='조회하기']") # 조회버튼
        search_btn.click()
        driver.implicitly_wait(5)

        # Assign int by seat class
        if input_seat_class == '특실': # td:nth-child(6)
            seat_class_num = 6
        elif input_seat_class == '일반실': # td:nth-child(7)
            seat_class_num = 7
        # else: #무관
            
        # Check the reservation status
        train_list = driver.find_elements(By.CSS_SELECTOR, '#result-form > fieldset >\
                                           div.tbl_wrap.th_thead > table > tbody > tr')
        print(train_list)
        #result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child(1)

        if isinstance(input_train_num, int):
            for i in range(1, input_train_num + 1):
                seat_class = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset >\
                                                  div.tbl_wrap.th_thead > table > tbody >\
                                                  tr:nth-child({i}) > td:nth-child(%s)" 
                                                  %seat_class_num).text
                
                
        else:
            for i in input_train_num:
                seat_class = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset >\
                                                  div.tbl_wrap.th_thead > table > tbody >\
                                                  tr:nth-child({i}) > td:nth-child(%s)" 
                                                  %seat_class_num).text
        
        print(seat_class)


                
                train_num = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset >\
                                                div.tbl_wrap.th_thead > table > tbody >\
                                                tr:nth-child(3) > td.trnNo").text
            


        # try:
        #     # Check the reservation status
        #     seat_btn = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div:nth-child(9) > input")
        #     seat_btn.click()
                        
        # except:
        #     print('예약이 불가능합니다. 다시 시도해주세요.')

        client = Client(sid, auth_token)
        message = client.messages.create(to=to_num, from_=from_num, body='SRT 예약 가능합니다.')

# test in here!
def main() -> None:
    user = UserData(username, password, input_dep_stn, input_arr_stn, input_date
                    , input_time, input_train_num, input_seat_class, input_seat_num
                    , input_seat_select, want_standing_seat, want_queue, to_num)
    srt = SRT(user)
    srt.check_fn()
    srt.reserve_fn()

# =============================================================================
# USER INPUT
# =============================================================================
username = 'XXX'
password =  'XXX'

input_dep_stn = '수서'
input_arr_stn = '부산'

input_date = 20240503 # 1개월 이내(YYYYMMDD)
input_time = 14 # ex) 00, 02, 14, 16...

# input_train_num = 2 # 
input_train_num = [343, 345] # 예약할 기차 번호
# list(기차 번호) or int(검색 결과 상단에서부터 예약 가능 여부 확인할 기차 수)

input_seat_class = '특실' # 특실, 일반실, 무관(입석 포함)
input_seat_num = {'경로':0, '일반':1} # 일반, 경로
input_seat_select = '자동선택' # 수동선택, 자동선택
want_standing_seat = False # 입석도 괜찮나요? True, False
want_queue = False # 예약 대기 원하나요? True, False

# Twilio Information
sid = 'XXX'
auth_token = 'XXX'
from_num = 'XXX'
to_num = 'XXX'

# =============================================================================
# EXECUTION
# =============================================================================
user = UserData(username, password, input_dep_stn, input_arr_stn, input_date
                , input_time, input_train_num, input_seat_class, input_seat_num
                , input_seat_select, want_standing_seat, want_queue, to_num)

if __name__ == '__main__':
    main()

# # Run 'reserve_fn' every hour
# schedule.every(1).hours.do(reserve_fn)
# schedule.every(40).seconds.do(reserve_fn)
# while True:
#     marker = True
#     schedule.run_pending()
#     time.sleep(1)
#     if marker == True:
#         schedule.cancel_job(reserve_fn)
#         break