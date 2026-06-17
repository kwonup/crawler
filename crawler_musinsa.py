#브랜드명
#제품이름
#가격
import requests
from bs4 import BeautifulSoup

#웹브라우저 통신
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#시간,판다스 
import time
import pandas as pd 
from tqdm import tqdm

#브라우저의 옵션(크롬브라우저 옵션)
#동적으로 selenium을 기반으로 작업할때 아래와 같은 규칙 적용
option = Options()
option.add_argument('--no-sandbox') #샌드박스 비활성화(보안 끄셈)
option.add_argument('--disable-dev-shm-usage') #공유메모리 꺼
option.add_argument('--disable-gpu') #GPU 쓰지마(굳이 이런일에)
option.add_argument('--enable-unsafe-swiftshader') #GPU안쓰니깐 대용

driver = webdriver.Chrome(options=option)
base_url = 'https://www.musinsa.com/categories/item/001'

driver.get(base_url)
time.sleep(2) #크롤링할 데이터가 화면/HTML에 생길 때까지 기다리는 것

#윈도우 스크롤 내리는 스크립트 추가
#window.scrollTo(시작점,끝점)
driver.execute_script('window.scrollTo(0,2000)')
time.sleep(2) #사람인 티 내기 위해 대기시간 일부러 부여

#창에 보이는 아이템 가져오기
#정적(bs4),동적(selenium), .find('구분자')
items = driver.find_elements(By.CSS_SELECTOR,".sc-bSFBcf.iEkOIH")
item_list = []

for item in items:
    #아래의 코드를 실행해봐
    try:
        #개별 상품에 대한 정보를 get
        #find_element(CSS를 기준으로 찾아줘,a['이름']:'이름'을 가지고 있는 블럭)
        a_tag = item.find_element(By.CSS_SELECTOR,"a[data-original-price]")
        #상품이름
        #예외처리
        #str(name) : name에 뭐가 들어오든 str처리
        #replace : "제거할 데이터", ""
        #strip : 양쪽공백 제거
        #name = a_tag.find_element(By.CSS_SELECTOR, 'span').text.strip()
        name = a_tag.get_attribute("aria-label")
        name = (str(name).replace("상품상세로 이동","").strip() if name else "이름없음")
        #브랜드 이름
        brand = a_tag.get_attribute("data-brand-id")
        brand = str(brand).strip() if brand else "브랜드 없음" 
        #가격
        price = a_tag.get_attribute("data-price") 
        price = str(price).strip() if price else "브랜드 없음" 
        #상세페이지
        link = a_tag.get_attribute("href")
        link = str(link).strip() if link else "링크없음"
        # print(f''' name: {name}
        #         brand: {brand}
        #         price: {price}
        #         link: {link}''')
        
        item_list.append({
            '상품명': name,
            '브랜드': brand,
            '가격': price,
            '링크': link
        })

    #실행하다 '에러'발생하면 이렇게 해(예외처리)
    except Exception as e:
        print(f'에러가 발생했습니다. :{e}')

#드라이버 종료
driver.quit()

df=pd.DataFrame(item_list,columns=['상품명','브랜드','가격','링크'])
df.to_csv('./musinsa_result.csv',index=False,encoding='utf-8-sig')