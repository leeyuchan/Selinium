from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 구글 시트 인증 및 연결 설정
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

doc = client.open("Selenium 결과 입력")
sheet = doc.get_worksheet(0)

driver = webdriver.Edge()

try:
    # 사이트 접속
    driver.get('https://sten.or.kr/home/kor/main.do')
    driver.maximize_window()
    driver.implicitly_wait(10)

    # 로그인 페이지 진입을 위한 로그인 버튼 클릭
    driver.find_element(By.XPATH, "//li[contains(text(), '로그인')]").click()

    # 로그인 정보 입력
    driver.find_element(By.ID, 'user_id').send_keys('dbcksehdrp')
    driver.find_element(By.ID, 'user_pw').send_keys('Qweasd598211@')

    # 로그인 버튼 클릭
    driver.find_element(By.CLASS_NAME, 'btn1').click()

    # 알림창 처리
    time.sleep(2)
    alert = driver.switch_to.alert
    alert.accept()

    # 결과 판단 및 시트 기록
    login_buttons = driver.find_elements(By.XPATH, "//li[contains(text(), '로그인')]")

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    test_name = "STEN 로그인 테스트"

    if not login_buttons:
        result = "PASS"
    else:
        result = "FAIL"

    sheet.update_acell('E2', result)
    sheet.update_acell('F2', now)

except Exception as e:
    print(f"오류 발생: {e}")