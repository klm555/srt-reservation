# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 18:22:31 2022

@author: hwlee
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
from random import randint

# =============================================================================
# %% 예매하기
# =============================================================================
# 예매 페이지로 이동
train_list = driver.find_elements(By.CSS_SELECTOR, '#result-form > fieldset >\
                                  div.tbl_wrap.th_thead > table > tbody > tr')
                                  
# 좌석 등급에 따라 index assigning
if input_seat_class == '특실': # td:nth-child(6) = 특실
    seat_class_num = 6
else: seat_class_num = 7 # 일반실 or 무관

# =============================================================================
# 기차 예매하기
is_reserved = False
counter = 0
while True:
    for i in range(1, input_train_num + 1): # 검색 결과 상위 x개에 대해 loop
        # 좌석 등급 index에 따라 해당 버튼 text 추출    
        seat_class = driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                         fieldset > div.tbl_wrap.th_thead >\
                                         table > tbody > tr:nth-child({i}) >\
                                         td:nth-child(%s)" 
                                         %seat_class_num).text
        # 예약 대기 버튼 text 추출
        queue = driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                    fieldset > div.tbl_wrap.th_thead > table >\
                                    tbody > tr:nth-child({i}) >\
                                    td:nth-child(8)").text
        # 수동선택
        if input_seat_select == '수동선택':    
            if '예약하기' in seat_class:
                print('예약 가능')
                driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div/\
                                    div[3]/div[1]/form/fieldset/div[6]/table/\
                                    tbody/tr[{i}]/td[%s]/div/a/span" 
                                    %seat_class_num).click()
                is_reserved = True
                break

        # 자동선택
        elif input_seat_select == '자동선택':
            if want_standing_seat == True:           
                if ('예약하기' in seat_class) | ('입석+좌석' in seat_class):
                    print('예약 가능')
                    driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/\
                                        div/div[3]/div[1]/form/fieldset/\
                                        div[6]/table/tbody/tr[{i}]/td[%s]/a/\
                                        span" %seat_class_num).click()
                    is_reserved = True
                    break
                
            elif want_standing_seat == False:  
                if '예약하기' in seat_class:
                    print('예약 가능')
                    driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/\
                                        div/div[3]/div[1]/form/fieldset/\
                                        div[6]/table/tbody/tr[{i}]/td[%s]/a/\
                                        span" %seat_class_num).click()
                    is_reserved = True
                    break
                
        if want_queue == True:
            if "신청하기" in queue:
                print("예약 대기 완료")
                driver.find_element(By.CSS_SELECTOR, f"#result-form >\
                                    fieldset > div.tbl_wrap.th_thead >\
                                    table > tbody > tr:nth-child({i}) >\
                                    td:nth-child(8) > a").click()
                is_reserved = True
                break
                
        # 좌석등급 무관        
        if input_seat_class == '무관':
            
            if input_seat_select == '수동선택':    
                if '예약하기' in seat_class:
                    print('예약 가능')
                    driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/\
                                        div/div[3]/div[1]/form/fieldset/\
                                        div[6]/table/tbody/tr[{i}]/td[6]/div/\
                                        a/span").click()
                    is_reserved = True
                    break
                
            elif input_seat_select == '자동선택':
                if want_standing_seat == True:           
                    if ('예약하기' in seat_class) | ('입석+좌석' in seat_class):
                        print('예약 가능')
                        driver.find_element(By.XPATH, f"/html/body/div[1]/\
                                            div[4]/div/div[3]/div[1]/form/\
                                            fieldset/div[6]/table/tbody/\
                                            tr[{i}]/td[6]/a/span" 
                                            %seat_class_num).click()
                        is_reserved = True
                        break
                    
                elif want_standing_seat == False:  
                    if '예약하기' in seat_class:
                        print('예약 가능')
                        driver.find_element(By.XPATH, f"/html/body/div[1]/\
                                            div[4]/div/div[3]/div[1]/form/\
                                            fieldset/div[6]/table/tbody/\
                                            tr[{i}]/td[6]/a/span" 
                                            %seat_class_num).click()
                        is_reserved = True
                        break
# =============================================================================

    if not is_reserved:
        time.sleep(randint(2, 4)) # 2~4초 랜덤으로 기다리기
        submit = driver.find_element(By.XPATH, "//input[@value='조회하기']") # 다시 조회하기
        driver.execute_script("arguments[0].click();", submit)
        print('새로고침 %s회' %counter)
        counter += 1
        driver.implicitly_wait(8)
        time.sleep(0.5)
        
    else: break

