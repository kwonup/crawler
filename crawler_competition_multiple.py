#인터넷 요청 -> requests
import requests
#정적 웹페이지 크롤링 -> bs
from bs4 import BeautifulSoup
#동적 웹페이지 크롤링
from selenium import webdriver

#시간 라이브러리
import time
#진행률을 표시하는 라이브러리 + for문
from tqdm import tqdm

#크롤링한 내용을 엑셀 파일로 저장하기 위해서.
#xlsx -> openpyxl(파이썬으로 엑셀 컨트롤)
#csv -> pandsd를 사용
import pandas as pd

#requests 라이브러리를 사용해서 웹페이지를 읽어와라(get)
max_pages = int(input('몇페이지까지 크롤링할까요?\n'))
all_corpus = [] #1,2,3...max_pages까지의 크롤링 내역을 한꺼번에 저장 list

#tqdm이 전체 실행시간 대비, 현재 진행 상황을 알려줌(게이지 올라감)
for page in tqdm(range(1,max_pages+1),desc='크롤링 진행중...'):
    url = f'https://www.cheongwon.go.kr/portal/petition/open/view?pageIndex={page}'

    response = requests.get(url)

    #웹페이지를 분해할 bs4객체 생성
    #파싱 : 어떤 정보 덩어리에서 원하는 정보를 추출하는것
    soup = BeautifulSoup(response.text,'html.parser')
    #print(response.text)

    #soup라는 파싱 객체가, 'span'이라는 양식의 class를 찾아서
    #class = 'category'라고 적힌 내용을 category라는 변수 이름에 저장
    category = soup.find_all('span',class_ = 'category') 
    subject = soup.find_all('span',class_ = 'subject')
    petition = soup.find_all('span',class_ = 'text') #청원
    #print(category,subject,petition)

    #크롤링한 결과물을 보기 쉬운 형태로 변환
    corpus = [] #corpus:말뭉치,자연어데이터 뭉치
    for c,s,t in zip(category,subject,petition):
        corpus.append([c.text,s.text,t.text])
    all_corpus.extend(corpus)
    time.sleep(1) #2초정도 정지

df = pd.DataFrame(all_corpus,columns=['카테고리','제목','청원내용'])
#print(df)
df.to_csv('./crawling_sample.csv',index=False,encoding='utf-8-sig')