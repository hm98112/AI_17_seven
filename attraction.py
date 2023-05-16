from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import subprocess

driver = webdriver.Chrome("C:/Users/hm981/Downloads/chromedriver_win32/chromedriver.exe")



#페이지 요소
"""
<a href="https://kr.trip.com/travel-guide/attraction/paris-308/tourist-attractions/1.html/">2</a>

<div class="poi-name margin-bottom-gap"><h3>19. 파리 자유의 여신상</h3><span>추천</span></div>

"""




for i in range(1, 101):
    driver.get("https://kr.trip.com/travel-guide/attraction/paris-308/tourist-attractions/"+str(i)+".html")
    driver.implicitly_wait(time_to_wait=10)
    time.sleep(1)
    texts = driver.find_elements(By.CLASS_NAME, "card-right")

    for text in texts:
        print(text.text)
    
    
driver.quit()




# 현재 환경에 설치된 패키지 목록을 얻습니다.
packages = subprocess.check_output(['pip', 'freeze']).decode('utf-8').split('\n')

# requirements.txt 파일을 생성하고 패키지 목록을 저장합니다.
with open('requirements.txt', 'w') as file:
    for package in packages:
        file.write(package + '\n')



