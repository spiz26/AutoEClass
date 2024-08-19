import requests
import time
import json
import pause
from datetime import timedelta
from datetime import datetime as dt
from datetime import time as tt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from HelperClass import *

"""
=============================================================================
기본 정보 세팅을 위한 코드입니다.
=============================================================================
"""

url = "https://eclass.seoultech.ac.kr/ilos/main/member/login_form.acl"
user_data_path = "user_data.json"

with open(user_data_path, "r") as f:
    user_data = json.load(f)

# user data 파일 읽기
yourID = user_data["ID"]
yourPW = user_data["Password"]

"""
=============================================================================
기본 정보 세팅이 모두 끝나셨나요? 돌아오시면 모든 강의가 수강되어 있을거예요!
=============================================================================
"""

def main():
    """
    버튼 세팅입니다. eclass 사이트가 수정되었을시, HTML ID, Class 이름이 바뀔 수 있기 때문에 변수로 저장합니다.
    """

    # 로그인 태그
    userID = "usr_id"
    userPW = "usr_pwd"
    login = "btntype"

    # 과목 들어가기
    open_subject = "sub_open"
    seoultech_logo = "logo_link"

    # 수업 주차 들어가기
    lecuture_room = "menu_lecture_weeks"
    week_lecture = "wb-week"

    # 해당 수업 선택하기
    lecture_num = "site-mouseover-color"
    complete_tag = "per_text"
    lecture_rest_time = "//div[@style='float: left;margin-left: 7px;margin-top:3px;']"

    play = "vc-front-screen-play-btn"
    """
    button setting이 완료 되셨나요? 곧 시작합니다.
    """
    
    res = requests.get(url)
    if res.status_code == requests.codes.ok:
        print("e-class ping 정상")

    else:
        print("서버와 통신이 되지 않습니다.")
        return
    
    # 브라우저 세팅
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    service = Service("chromedriver.exe")

    # e-class 접속
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.get(url)
    browser.maximize_window()
    browser.implicitly_wait(5)

    # e-class 로그인
    browser.find_element(By.ID, userID).send_keys(yourID)
    browser.find_element(By.ID, userPW).send_keys(yourPW)
    browser.find_element(By.CLASS_NAME, login).click()
    browser.implicitly_wait(5)

    # 과목 찾기
    subjects = browser.find_elements(By.CLASS_NAME, open_subject)
    num_subjects = len(subjects)
    
    # 과목명 저장
    subject_dict = {}

    for i in range(num_subjects):
        title_text = subjects[i].get_attribute("title")
        subject_name = title_text.replace(" 강의실 들어가기", "")
        subject_dict[i] = subject_name

    first = True
    # 과목 듣기
    for sub_i in range(num_subjects):
        browser.find_element(By.ID, seoultech_logo).click()
        browser.implicitly_wait(5)

        # 과목 다시 찾기
        subjects = browser.find_elements(By.CLASS_NAME, open_subject) # 페이지가 reload되어 다시 찾아야 함.

        subject = subjects[sub_i]
        subject.click()
        browser.implicitly_wait(5)

        # lecture room
        browser.find_element(By.ID, lecuture_room).click()
        lectures_weeks = browser.find_elements(By.CLASS_NAME, week_lecture)

        week_list = [week.text.replace("주", "") for week in lectures_weeks]

        # 과목의 해당 주차 듣기
        for week in week_list:
            # 해당 주차 수업 들어가기
            browser.find_element(By.ID, f"week-{week}").click()
            browser.implicitly_wait(5)

            lectures_per_week = browser.find_elements(By.CLASS_NAME, lecture_num)
            num_lectures = len(lectures_per_week)
            completes = browser.find_elements(By.ID, complete_tag)
            rest_time = browser.find_elements(By.XPATH, lecture_rest_time)

            complete_list = [com.text for com in completes]
            rest_time_list = [time.text for time in rest_time]

            # 해당 주차의 수업 듣기
            for lecture_i in range(num_lectures):
                lectures_per_week = browser.find_elements(By.CLASS_NAME, lecture_num)

                if complete_list[lecture_i] == "100%":
                    continue

                else:
                    lec_rest_time, listen_time, total_time = RestTime(rest_time_list[lecture_i])
                    lectures_per_week[lecture_i].click()
                    browser.implicitly_wait(5)

                    if first:
                        print("\n\n\n\n")
                        first = False

                    output_template = (
                        "+-------------------------------------------------------+\n"
                        "| 과목: {subject}, {curr}/{tot} | 주차: {week} | 수업: {lecture}/{total_lectures} |\n"
                        "+-------------------------------------------------------+\n"
                        "| 남은 시간: {remain} | 들은 시간: {listen} | 전체 시간: {total} | \n"
                        "+-------------------------------------------------------+\n"
                    )
                    play_button = browser.find_element(By.CLASS_NAME, play)
                    play_button.click()
                    
                    while lec_rest_time > 0:
                        delay_datetime = dt.now() + timedelta(seconds=1)
                        pause.until(delay_datetime)
                        lec_rest_time -= 1
                        trans_lec_rest_time = convert_seconds(lec_rest_time)
                        output = output_template.format(subject=subject_dict[sub_i], week=week, lecture=lecture_i+1,
                                                        curr=sub_i+1, tot=len(subject_dict),total_lectures=num_lectures,
                                                        remain=trans_lec_rest_time, listen=listen_time, total=total_time)

                        print("\033[F" * output.count('\n'), end='')  
                        print(output, end="", flush=True)

                    time.sleep(1)
                    close_button = browser.find_element(By.ID, "close_")
                    close_button.click()

                    try:
                        alert = Alert(browser)
                        alert.accept()

                    except:
                        pass

                    time.sleep(1)

if __name__ == "__main__":
    main()