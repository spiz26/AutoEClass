
from datetime import datetime
from datetime import timedelta
import time
from selenium.common.exceptions import NoAlertPresentException

def RestTime(time_string):
    """남은 시간 계산을 계산합니다"""
    time_string = time_string.replace(" ", "").split("/")
    numerator = time_string[0]
    denominator = time_string[1]

    #시간 세팅
    time_format1 = timeformat(numerator)
    time_format2 = timeformat(denominator)

    # 시간 문자열과 포맷이 일치하는지 확인
    try:
        numer_time = datetime.strptime(numerator, time_format1)
        denom_time = datetime.strptime(denominator, time_format2)
        
    except ValueError as e:
        print(f"Error parsing time: {e}")
        return None
    
    remain_time = (denom_time - numer_time).seconds + 2
    
    # 시간 차이 계산
    return remain_time, numerator, denominator

def timeformat(time: str) -> str:
    if time.count(":") == 2:
        time_format = "%H:%M:%S"

    elif time.count(":") == 1:
        time_format = "%M:%S"

    else:
        time_format = "%S"
    return time_format

def convert_seconds(seconds: int) -> str:
    time_delta = timedelta(seconds=seconds)
    total_seconds = int(time_delta.total_seconds())
    
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    elif minutes > 0:
        return f"{minutes:02}:{seconds:02}"
    else:
        return f"{seconds:02}"

def AlertProcessing(browser):
    try:
        alert = browser.switch_to.alert
        print(f"Alert text: {alert.text}")
        alert.dismiss()
        print("제때 강의를 들었어야죠ㅠㅠ")
        time.sleep(0.2)
        return True

    except NoAlertPresentException:
        return False

def other_device(browser):
    try:
        time.sleep(0.5)
        alert = browser.switch_to.alert
        print(f"Alert text: {alert.text}")
        alert.accept()
        print("다른 기기에서의 연결을 해제합니다.")

    except NoAlertPresentException:
        pass