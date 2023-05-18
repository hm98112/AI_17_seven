from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
import re

#셀레니움 크롬 드라이버
driver = webdriver.Chrome("C:/Users/hm981/Downloads/chromedriver_win32/chromedriver.exe")
driver.get(f"https://www.getyourguide.com/-l16?lng=en&p=1&date_from=2023-06-01&date_to=2023-08-31&sort=popularity&order=&searchContext=LOCATIONS&activeTab=base")  #호출할 사이트 url
data = []

#1~100번 페이지까지 탐색

for i in range(1, 51):
    #일정 시간 간격을 두어 수집
    driver.implicitly_wait(time_to_wait=10)                                                                  
    time.sleep(1)

    #페이지 소스 추출 및 파싱
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    #요소 찾기
    is_field = soup.find('div', class_ = 'trip-item-activities-desktop__activities-container-content')
    if is_field:
        attractions = is_field.find_all('div', class_ = 'vertical-activity-card__content-wrapper')
    else:
        pass
    for attraction in attractions:
    
        #요소가 없을 경우 None을 반환함 / 모든 요소에 이를 적용하여 값이 있는 경우에만 text를 추출하도록하여 오류 방지
        #투어 이름
        is_name = attraction.find('p')
        if is_name:
            name = is_name.text
        else:
            name = None
        #투어 카테고리
        is_category = attraction.find('div', class_ = 'vertical-activity-card__activity-type-wrapper')
        if is_category:
            category = is_category.text
        else:
            category = None
        #투어 속성(소요 시간 추출용)
        is_attribute = attraction.find('ul', class_ = 'activity-attributes__container')
        if is_attribute:
            attribute = is_attribute.text
        else:
            attribute = None
        #투어 평점
        is_rate = attraction.find('span', class_ = 'rating-overall__rating-number rating-overall__rating-number--right')
        if is_rate:
            rate = is_rate.text
        else:
            rate = 0
        #투어 가격
        is_price = attraction.find('div', class_ = 'baseline-pricing')
        if is_price:
            is_discount_price = is_price.find('div', class_ = 'baseline-pricing__value baseline-pricing__value--low')
            is_base_price = is_price.find('div', class_ = 'baseline-pricing__container')
            if is_discount_price:
                price = is_discount_price.text
            
            elif is_base_price:
                price = is_base_price.text
            else:
                price = 0
                
        else:
            price = 0
        
        data.append([name, category, attribute, rate, price])
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/(4/3));")
    time.sleep(1)

    #다음 페이지 넘어가는 코드
    button = driver.find_element(By.CSS_SELECTOR, '#main-content > div:nth-child(6) > div > div > div.trip-item-activities-desktop__activities-container > div > div.trip-item-pagination.trip-item-activities-desktop__activities-container__pagination > div.trip-item-pagination__controls > button.trip-item-pagination__controls-item.next.c-button.c-button--medium.c-button--outlined-standard')
    button.click()
    time.sleep(1)
driver.quit()


df = pd.DataFrame(data, columns=['name', 'category', 'attribute', 'rate', 'price'])

#카테고리 / 이름  전처리
df.category = df.category.str.replace('\n', ' ').str.lstrip().str.rstrip()
df.name = df.name.str.replace('\n', ' ').str.lstrip().str.rstrip()

#attribute 속성에서 시간 추출 함수
def extract_time(sentence):
    pattern = r'\d+(?:\.\d+)?\s*(?:-\s*)?\d*(?:\.\d+)?\s*(?:hours|hour|minutes|minute|days|day)'
    matches = re.findall(pattern, sentence)
    if matches:
        return matches[0]
    else:
        return None

time = []
#시간 추출 함수 적용
for att in df.attribute:
  res = extract_time(att)
  time.append(res)

df['time'] = time

#추출 끝난 attribute 속성 제거
df.drop(columns='attribute', inplace= True)


#가격 추출 함수
def extract_price(sentence):
    pattern = r'₩\s*([\d,]+)\s*(per person|per group up to \d)'
    matches = re.findall(pattern, sentence)
    if matches:
        return [match[0] +' ' + match[1] for match in matches][0]
    else:
        return None

clean_price = []

#가격 추출 함수 적용
for row in df.price:
  clean_price.append(extract_price(row))

df['price'] = clean_price

#csv 파일 변환
df.to_csv('attraction_clean', index=False)



