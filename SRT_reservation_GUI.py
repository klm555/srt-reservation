# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 18:22:31 2022

@author: hwlee
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

import time
from random import randint
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSettings, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5 import uic # ui 파일을 사용하기 위한 모듈

# =============================================================================
# 
# =============================================================================
# .ui 파일을 class 형태로 load
ui_class = uic.loadUiType('SRT_reservation.ui')[0]

class main_window(QMainWindow, ui_class):
    def __init__(self):
        # 부모 클래스(QMainWindow, ui_class (?))로부터 속성 및 메소드를 상속받음
        super().__init__()
        
        self.setupUi(self)
        
        # setting(값을 저장해 놓을 변수) 생성
        QCoreApplication.setOrganizationName('hwl')
        QCoreApplication.setApplicationName('SRT Automatic Reservation')
        self.setting = QSettings()
        # setting에 저장된 value를 불러와서 입력
        # .setText() : box에 text assign / .setCurrentText() : combobox에 text assign
        self.setting.beginGroup('log-on')
        self.id_input_box.setText(self.setting.value('id'))
        self.pw_input_box.setText(self.setting.value('pw'))
        self.setting.endGroup()
        
        self.setting.beginGroup('reservation')
        self.dep_input_box.setText(self.setting.value('departure'))
        self.arr_input_box.setText(self.setting.value('arrival'))
        self.date_input_box.setText(self.setting.value('date'))
        self.time_input_cbbox.setCurrentText(self.setting.value('time'))
        self.train_num_input_cbbox.setCurrentText(self.setting.value('number_of_trains'))
        self.seat_class_input_cbbox.setCurrentText(self.setting.value('seat_class'))
        self.adult_num_input_cbbox.setCurrentText(self.setting.value('number_of_adults'))
        self.senior_num_input_cbbox.setCurrentText(self.setting.value('number_of_seniors'))
        self.seat_select_cbbox.setCurrentText(self.setting.value('seat_selection'))
        self.want_standing_seat_cbbox.setCurrentText(self.setting.value('want_standing_seat'))
        self.want_queue_cbbox.setCurrentText(self.setting.value('want_queue'))
        self.setting.endGroup()
        
        # 예약, 끝내기 버튼
        self.reserve_btn.clicked.connect(self.reserve_fn) # 버튼 누르면 실행
        self.cancel_btn.clicked.connect(self.close) # 취소 누르면 꺼짐
         
        # 기타
        self.setWindowIcon(QIcon('./images/train_icon.png')) # icon 설정
        self.pw_input_box.setEchoMode(QLineEdit.Password) # pw 안보이게 설정
        
    # 실행해야할 명령 전달 when Qt receives a window close request        
    def closeEvent(self, event):
        if self.login_checkbox.isChecked():
            # setValue(key, value) : key와 value를 setting에 저장
            # .text() : 해당 box의 값 / .currentText() : 해당 combobox의 값
            self.setting.beginGroup('log-on')
            self.setting.setValue('id', self.id_input_box.text())
            self.setting.setValue('pw', self.pw_input_box.text())
            self.setting.endGroup()
        else: # setting의 모든 값을 clear
            self.setting.clear()
            
        if self.reserve_checkbox.isChecked():
            self.setting.beginGroup('reservation')
            self.setting.setValue('departure', self.dep_input_box.text())
            self.setting.setValue('arrival', self.arr_input_box.text())
            self.setting.setValue('date', self.date_input_box.text())
            self.setting.setValue('time', self.time_input_cbbox.currentText())
            self.setting.setValue('number_of_trains', self.train_num_input_cbbox.currentText())
            self.setting.setValue('seat_class', self.seat_class_input_cbbox.currentText())
            self.setting.setValue('number_of_adults', self.adult_num_input_cbbox.currentText())
            self.setting.setValue('number_of_seniors', self.senior_num_input_cbbox.currentText())
            self.setting.setValue('seat_selection', self.seat_select_cbbox.currentText())
            self.setting.setValue('want_standing_seat', self.want_standing_seat_cbbox.currentText())
            self.setting.setValue('want_queue', self.want_queue_cbbox.currentText())
            self.setting.endGroup()
        else: self.setting.clear()

# =============================================================================
# USER INPUT
# =============================================================================
# username = '2080926322' # self.id_input_box.text()
# password =  '1q2w#E$R' # self.pw_input_box.text()

# input_dep_stn = '수서' # self.dep_input_box.text()
# input_arr_stn = '부산' # self.arr_input_box.text()

# input_date = '20221221' # 1개월 이내(YYYYMMDD)
# input_time = '16' # 00, 02, 14, 16 형식
# input_train_num = 3 # 검색 결과 상단에서부터 예약 가능 여부 확인할 기차 수

# input_seat_class = '무관' # 특실, 일반실, 무관
# input_seat_num = '기능추가예정' # 좌석수
# input_seat_select = '수동선택' # 수동선택, 자동선택
# want_standing_seat = True # 입석도 괜찮나요? True, False
# want_queue = True # 예약 대기 원하나요? True, False

# =============================================================================
# %% AUTOMATIC EXECUTION
# =============================================================================

    def reserve_fn(self):
            
        # 현재 크롬 버전에 맞게 ChromeDriver 자동 설치
        service = Service(ChromeDriverManager().install())        
        chrome_options = Options() # chrome_options : 실행이 끝난 후에 크롬창을 끌지 말지 선택
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=service, chrome_options=chrome_options)
        
        # 로그인 페이지로 이동
        driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')
        driver.implicitly_wait(15) # 페이지 다 뜰 때 까지 기다림
        
        driver.find_element(By.ID, 'srchDvNm01').send_keys(self.id_input_box.text()) # 회원번호
        driver.find_element(By.ID, 'hmpgPwdCphd01').send_keys(self.pw_input_box.text()) # 비밀번호
        driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]\
                            /div[2]/div/div[2]/input').click() # 확인버튼 (by full XPath)
        driver.implicitly_wait(5)
        
        # 기차 조회 페이지로 이동
        driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do')
        driver.implicitly_wait(5)
        
        dep_stn = driver.find_element(By.ID, 'dptRsStnCdNm') # 출발지
        dep_stn.clear() # default값 지우기
        dep_stn.send_keys(self.dep_input_box.text())
        
        arr_stn = driver.find_element(By.ID, 'arvRsStnCdNm') # 도착지
        arr_stn.clear()
        arr_stn.send_keys(self.arr_input_box.text())
        
        # 출발날짜 입력
        dep_date = driver.find_element(By.ID, 'dptDt') # 출발날짜
        driver.execute_script("arguments[0].setAttribute('style','display: True;')"\
                              , dep_date) # 날짜 드롭다운 리스트 보이게
    
        try: 
            Select(dep_date).select_by_value(self.date_input_box.text()) # 출발날짜 선택
        except:
            self.output_print_box.setText('해당 날짜에 예약이 불가능합니다.')
    
        
        # 출발시간 입력
        dep_time = driver.find_element(By.ID, 'dptTm') # 출발시간
        driver.execute_script("arguments[0].setAttribute('style','display: True;')"\
                              , dep_time)
        Select(dep_time).select_by_visible_text(self.time_input_cbbox.currentText()) # 출발시간 선택(by Visible Text)
        driver.find_element(By.XPATH, "//input[@value='조회하기']").click() # 조회버튼
        driver.implicitly_wait(5)
        
        # =============================================================================
        # # 예약 정보 표시
        # print('기차를 조회합니다\n')
        # print('# 출발역:%s, # 도착역:%s' %(input_dep_stn, input_arr_stn))
        # print('# 인원:%s, # 등급:%s' %(input_seat_num, input_seat_class))
        # print('# 좌석선택:%s, # 입석선택여부:%s' %(input_seat_select, want_standing_seat))
        # print('# 날짜:%s, # 시간:%s시 이후' %(input_dep_date, input_dep_time))
        # print('%s개의 기차 중 예약' %input_num_of_trains)
        # print('# 예약 대기 사용:%s\n' %want_queue)
        # =============================================================================
        
        # =============================================================================
        # %% 예매하기
        # =============================================================================
        # 예매 페이지로 이동
        train_list = driver.find_elements(By.CSS_SELECTOR, '#result-form > fieldset >\
                                          div.tbl_wrap.th_thead > table > tbody > tr')
                                          
        # 좌석 등급에 따라 index assigning
        if self.seat_class_input_cbbox.currentText() == '특실': # td:nth-child(6) = 특실
            seat_class_num = 6
        else: seat_class_num = 7 # 일반실 or 무관
        
        # =============================================================================
        # 기차 예매하기
        is_reserved = False
        counter = 0
        # 검색 결과 상위 x개에 대해 loop
        while True:
            for i in range(1, int(self.train_num_input_cbbox.currentText()) + 1):                
                # 좌석 등급 index에 따라 해당 버튼 text 추출    
                seat_class = driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                                 fieldset > div.tbl_wrap.th_thead >\
                                                 table > tbody > tr:nth-child({i}) >\
                                                 td:nth-child(%s)"
                                                 %seat_class_num).text
                    #result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child(4) > td:nth-child(7) > a
                # 예약 대기 버튼 text 추출
                queue = driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                            fieldset > div.tbl_wrap.th_thead > table >\
                                            tbody > tr:nth-child({i}) >\
                                            td:nth-child(8)").text
                # 수동선택
                if self.seat_select_cbbox.currentText() == '수동선택':    
                    if '예약하기' in seat_class:
                        driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                            fieldset > div.tbl_wrap.th_thead >\
                                            table > tbody > tr:nth-child({i}) >\
                                            td:nth-child(%s) > div > a"
                                            %seat_class_num).click()
                        # =====================================================
                        # 코로나 어쩌구(특실일 경우)(temp)
                        if driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").text == '확인':
                            driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").click()
                        # =====================================================
                            is_reserved = True
                            self.output_print_box.setText('좌석 선택 가능')
                            break
        
                # 자동선택
                else:
                    if self.want_standing_seat_cbbox.currentText() == True:           
                        if ('예약하기' in seat_class) | ('입석' in seat_class):
                            driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                                fieldset > div.tbl_wrap.th_thead >\
                                                table > tbody > tr:nth-child({i}) >\
                                                td:nth-child(%s) > a"
                                                %seat_class_num).click()
                            # =====================================================
                            # 코로나 어쩌구(특실일 경우)(temp)
                            if driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").text == '확인':
                                driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").click()
                            # =====================================================
                            if driver.find_elements(By.ID, 'isFalseGotoMain'):
                                is_reserved = True
                                self.output_print_box.setText('예약 성공')
                                break
                            else:
                                self.output_print_box.setText('잔여석 없음. 다시 검색')
                                driver.back()
                                driver.implicitly_wait(5)
                        
                    else:  
                        if '예약하기' in seat_class:
                            driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                                fieldset > div.tbl_wrap.th_thead >\
                                                table > tbody > tr:nth-child({i}) >\
                                                td:nth-child(%s) > a"
                                                %seat_class_num).click()
                            # =====================================================
                            # 코로나 어쩌구(특실일 경우)(temp)
                            if driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").text == '확인':
                                driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").click()
                            # =====================================================
                            if driver.find_elements(By.ID, 'isFalseGotoMain'):
                                is_reserved = True
                                self.output_print_box.setText('예약 성공')
                                break
                            else:
                                self.output_print_box.setText('잔여석 없음. 다시 검색')
                                driver.back()
                                driver.implicitly_wait(5)
                        
                if self.want_queue_cbbox.currentText() == True:
                    if "신청하기" in queue:
                        driver.find_element(By.CSS_SELECTOR, "#result-form >\
                                            fieldset > div.tbl_wrap.th_thead >\
                                            table > tbody > tr:nth-child({i}) >\
                                            td:nth-child(8) > a").click()
                        is_reserved = True
                        self.output_print_box.setText('예약 대기 성공')
                        break
                        # if driver.find_elements(By.ID, 'isFalseGotoMain'):
                        #     is_reserved = True
                        #     self.output_print_box.setText('예약 대기 성공')
                        #     break
                        # else:
                        #     self.output_print_box.setText('잔여석 없음. 다시 검색')
                        #     driver.back()
                        #     driver.implicitly_wait(5)
                        
                # 좌석등급 무관        
                if self.seat_class_input_cbbox.currentText() == '무관':
                    
                    # 수동선택
                    if self.seat_select_cbbox.currentText() == '수동선택':    
                        if '예약하기' in seat_class:
                            driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                                fieldset > div.tbl_wrap.th_thead >\
                                                table > tbody > tr:nth-child({i}) >\
                                                td:nth-child(6) > div > a").click()
                                                
                            # ==================================================
                            # 코로나 어쩌구(temp)
                            if driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").text == '확인':
                                driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").click()
                            # =================================================
                                is_reserved = True
                                self.output_print_box.setText('좌석 선택 가능')
                                break
                    else:
                        if self.want_standing_seat_cbbox.currentText() == True:           
                            if ('예약하기' in seat_class) | ('입석' in seat_class):
                                driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                                    fieldset > div.tbl_wrap.th_thead >\
                                                    table > tbody > tr:nth-child({i}) >\
                                                    td:nth-child(6) > a").click()
                                # =====================================================
                                # 코로나 어쩌구(특실일 경우)(temp)
                                if driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").text == '확인':
                                    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").click()
                                # =====================================================
                                if driver.find_elements(By.ID, 'isFalseGotoMain'):
                                    is_reserved = True
                                    self.output_print_box.setText('예약 성공')
                                    break
                                else:
                                    self.output_print_box.setText('잔여석 없음. 다시 검색')
                                    driver.back()
                                    driver.implicitly_wait(5)
                            
                        else:  
                            if '예약하기' in seat_class:
                                driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                                    fieldset > div.tbl_wrap.th_thead >\
                                                    table > tbody > tr:nth-child({i}) >\
                                                    td:nth-child(6) > a").click()
                                # =====================================================
                                # 코로나 어쩌구(특실일 경우)(temp)
                                if driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").text == '확인':
                                    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").click()
                                # =====================================================
                                if driver.find_elements(By.ID, 'isFalseGotoMain'):
                                    is_reserved = True
                                    self.output_print_box.setText('예약 성공')
                                    break
                                else:
                                    self.output_print_box.setText('잔여석 없음. 다시 검색')
                                    driver.back()
                                    driver.implicitly_wait(5)
        # =============================================================================
        
            if not is_reserved:
                time.sleep(randint(2, 4)) # 2~4초 랜덤으로 기다리기
                submit = driver.find_element(By.XPATH, "//input[@value='조회하기']") # 다시 조회하기
                driver.execute_script("arguments[0].click();", submit)
                self.output_print_box.setText('새로고침 %s회' %counter)
                counter += 1
                driver.implicitly_wait(8)
                time.sleep(0.5)
                
            else: break

if __name__ == '__main__':
    # driver = open_browswer()
    # driver = 
    app = QApplication(sys.argv) # QApplication : 프로그램을 실행시켜주는 class
    mywindow = main_window() # WindowClass의 인스턴스 생성   
    mywindow.show() # 프로그램 보여주기
    app.exec_() # 프로그램을 작동시키는 코드


# =============================================================================
# USER INPUT
# =============================================================================
# 예약 여부 (False일 시, 조회만 실행)
reserve_train = True

username = '2080926322' # self.id_input_box.text()
password =  '1q2w#E$R' # self.pw_input_box.text()

input_dep_stn = '수서' # self.dep_input_box.text()
input_arr_stn = '부산' # self.arr_input_box.text()

input_date = '20231029' # 1개월 이내(YYYYMMDD)
input_time = '16' # 00, 02, 14, 16 형식

# input_train_num = 1 # 검색 결과 상단에서부터 예약 가능 여부 확인할 기차 수
input_train_num = [9357, 359, 361] # 예약할 기차 번호, list형으로 입력

input_seat_class = '특실' # 특실, 일반실, 무관(입석 포함)
input_seat_num = '기능추가예정' # 좌석수
input_seat_select = '자동선택' # 수동선택, 자동선택
want_queue = False # 예약 대기 원하나요? True, False
# =============================================================================
#%% AUTOMATIC EXECUTION

def reserve_fn(self, reserve_train = True):
        
    # 현재 크롬 버전에 맞게 ChromeDriver 자동 설치
    # service = Service(ChromeDriverManager().install())        
    # chrome_options = Options() # chrome_options : 실행이 끝난 후에 크롬창을 끌지 말지 선택
    # chrome_options.add_experimental_option("detach", True)
    # driver = webdriver.Chrome(service=service, chrome_options=chrome_options)
    
    # Execute Chromedriver
    driver = webdriver.Chrome()

    # 로그인 페이지로 이동
    driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')
    driver.implicitly_wait(15) # 페이지 다 뜰 때 까지 기다림
    
    driver.find_element(By.ID, 'srchDvNm01').send_keys(username) # 회원번호
    driver.find_element(By.ID, 'hmpgPwdCphd01').send_keys(password) # 비밀번호
    driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]\
                        /div[2]/div/div[2]/input').click() # 확인버튼 (by full XPath)
    driver.implicitly_wait(5)
    
    # 기차 조회 페이지로 이동
    driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do')
    driver.implicitly_wait(5)
    
    dep_stn = driver.find_element(By.ID, 'dptRsStnCdNm') # 출발지
    dep_stn.clear() # default값 지우기
    dep_stn.send_keys(input_dep_stn)
    
    arr_stn = driver.find_element(By.ID, 'arvRsStnCdNm') # 도착지
    arr_stn.clear()
    arr_stn.send_keys(input_arr_stn)
    
    # 출발날짜 입력
    dep_date = driver.find_element(By.ID, 'dptDt') # 출발날짜
    driver.execute_script("arguments[0].setAttribute('style','display: True;')"\
                            , dep_date) # 날짜 드롭다운 리스트 보이게

    # 출발시간 입력
    dep_time = driver.find_element(By.ID, 'dptTm') # 출발시간
    driver.execute_script("arguments[0].setAttribute('style','display: True;')"\
                            , dep_time)

    # 입력된 날짜/시간에 예약
    try: 
        Select(dep_date).select_by_value(input_date) # 출발날짜 선택
        Select(dep_time).select_by_visible_text(input_time) # 출발시간 선택(by Visible Text)
        # 조회하기 버튼 클릭
        driver.find_element(By.XPATH, "//input[@value='조회하기']").click() # 조회버튼
        driver.implicitly_wait(5)

    except:
        print('해당 날짜/시간의 예약이 불가능합니다. 다시 입력해주세요.')

    ##### 예매하기 #####
    if reserve_train == True:
                                            
        # 좌석 등급에 따라 index assign
        if input_seat_class == '특실': # td:nth-child(6) = 특실
            seat_class_num = 6
        else: seat_class_num = 7 # 일반실 or 무관

        # 화면에 표시된 기차 개수
        train_list = driver.find_elements(By.CSS_SELECTOR, '#result-form > fieldset > \
                                        div.tbl_wrap.th_thead > table > tbody > tr')
        
        # 기차 번호로 예매할 경우, 기차 번호의 index list 만들기
        try:
            if type(input_train_num) == list:
                i = 1
                train_idx_list = []
                while True:
                    train_idx = int(driver.find_element(By.CSS_SELECTOR, '#result-form > fieldset >\
                                            div.tbl_wrap.th_thead > table > tbody >\
                                            tr:nth-child(%s) > td.trnNo' %i).text)
                    if train_idx in input_train_num:
                        train_idx_list.append(i)

                    if len(train_idx_list) == len(input_train_num):
                        break
                    i += 1

                input_train_num = train_idx_list.copy()
            
            # 기차의 숫자로 예매할 경우, range list 만들기
            if type(input_train_num) == int:
                input_train_num = list(range(1, input_train_num + 1))
        except:
            print('검색할 기차 번호/개수가 잘못 입력되었습니다.')

        # 기차 예매하기
        is_reserved = False
        counter = 1
        while True:
            for i in input_train_num:                
                # 좌석 등급 index에 따라 해당 버튼 text 확인    
                seat_class = driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                                    fieldset > div.tbl_wrap.th_thead >\
                                                    table > tbody > tr:nth-child({i}) >\
                                                    td:nth-child(%s)"
                                                    %seat_class_num).text
                    #result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child(4) > td:nth-child(7) > a
                
                # 수동선택
                if input_seat_select == '수동선택':    
                    if '예약하기' in seat_class:
                        driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                            fieldset > div.tbl_wrap.th_thead >\
                                            table > tbody > tr:nth-child({i}) >\
                                            td:nth-child(%s) > div > a"
                                            %seat_class_num).click()
                        # =====================================================
                        # 코로나 어쩌구(특실일 경우)(temp)
                        # if driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").text == '확인':
                        #     driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").click()
                        # =====================================================
                        is_reserved = True
                        print('~~~ 좌석 선택 가능 ~~~')
                        break
        
                # 자동선택
                else:
                    if input_seat_class == '무관':           
                        if ('예약하기' in seat_class) | ('입석' in seat_class):
                            driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                                fieldset > div.tbl_wrap.th_thead >\
                                                table > tbody > tr:nth-child({i}) >\
                                                td:nth-child(%s) > a"
                                                %seat_class_num).click()
                            # =====================================================
                            # 코로나 어쩌구(특실일 경우)(temp)
                            # if driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").text == '확인':
                            #     driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").click()
                            # =====================================================
                            if driver.find_elements(By.ID, 'isFalseGotoMain'): # 다시계산 버튼이 뜨면 예약 성공
                                is_reserved = True
                                print('~~~ 예약 성공 ~~~')
                                break
                        
                    # else: if input_seat_class == '특실' or '일반실':
                        if '예약하기' in seat_class:
                            driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                                fieldset > div.tbl_wrap.th_thead >\
                                                table > tbody > tr:nth-child({i}) >\
                                                td:nth-child(%s) > a"
                                                %seat_class_num).click()
                            # =====================================================
                            # 코로나 어쩌구(특실일 경우)(temp)
                            # if driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").text == '확인':
                            #     driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]").click()
                            # =====================================================
                            if driver.find_elements(By.ID, 'isFalseGotoMain'):
                                is_reserved = True
                                print('~~~ 예약 성공 ~~~')
                                break
                        
                if want_queue == True:
                    # 예약 대기 버튼 text 확인
                    queue = driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                            fieldset > div.tbl_wrap.th_thead > table >\
                                            tbody > tr:nth-child({i}) >\
                                            td:nth-child(8)").text
                
                    if "신청하기" in queue:
                        driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                            fieldset > div.tbl_wrap.th_thead >\
                                            table > tbody > tr:nth-child({i}) >\
                                            td:nth-child(8) > a").click()
                        
                        is_reserved = True
                        print('~~~ 예약 대기 성공 ~~~')
                        break
                        
            # 예약 실패 시, loop 다시 돌리기
            if not is_reserved:
                time.sleep(randint(2, 4)) # 2~4초 랜덤으로 기다리기
                submit = driver.find_element(By.XPATH, "//input[@value='조회하기']") # 다시 조회하기
                driver.execute_script("arguments[0].click();", submit)
                print('잔여석 없음. 다시 검색. (새로고침 %s회)' %counter)
                counter += 1
                driver.implicitly_wait(8)
                time.sleep(0.5)
            
            # 예약 성공 시, 끝내기
            else: break