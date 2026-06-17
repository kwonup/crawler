# 크롤링 정리

이 문서는 `crawler_competition.py`, `crawler_competition_multiple.py`, `crawler_musinsa.py`, `crawler_saramin.py`에서 사용한 코드를 바탕으로 크롤링의 기본 개념과 자주 쓰는 문법을 정리한 것이다.

처음 크롤링을 공부하는 사람이 봐도 흐름을 이해할 수 있도록 용어 정의부터 정리한다.

## 1. 크롤링이란?

크롤링은 웹사이트에 있는 데이터를 자동으로 가져오는 작업이다.

사람이 브라우저에서 사이트에 들어가서 글자, 링크, 가격, 회사명 등을 복사하는 일을 파이썬 코드가 대신한다고 생각하면 된다.

예를 들어 지금 실습한 크롤링 대상은 다음과 같다.

- 청원 사이트: 카테고리, 제목, 청원 내용 수집
- 무신사: 상품명, 브랜드명, 가격, 링크 수집
- 사람인: 회사명, 공고 제목, 채용 조건, 링크 수집

크롤링의 기본 흐름은 거의 항상 비슷하다.

```python
웹페이지 요청하기
HTML 가져오기
HTML에서 원하는 태그 찾기
텍스트나 속성값 추출하기
리스트에 저장하기
DataFrame으로 변환하기
CSV 파일로 저장하기
```

## 2. HTML이란?

HTML은 웹페이지의 구조를 만드는 문서이다.

브라우저에서 보는 글자, 버튼, 이미지, 링크 등은 대부분 HTML 태그로 구성되어 있다.

예시:

```html
<a href="https://www.musinsa.com/products/6526215">
    <span>빈티지 셔링 셔츠</span>
</a>
```

여기서:

- `<a>`: 링크 태그
- `href`: 링크 주소가 들어있는 속성
- `<span>`: 짧은 텍스트를 담을 때 자주 쓰는 태그
- `빈티지 셔링 셔츠`: 실제 화면에 보이는 텍스트

크롤링은 이런 HTML 구조에서 원하는 부분을 찾아 값을 꺼내는 작업이다.

## 3. 태그, class, id, 속성

HTML 요소를 찾으려면 태그 이름, class, id, 속성을 알아야 한다.

```html
<div class="item_recruit">
    <strong class="corp_name">
        <a href="/company/info">회사명</a>
    </strong>
</div>
```

용어 정리:

- 태그: `div`, `strong`, `a`, `span` 같은 HTML 요소 이름
- class: 여러 요소에 붙일 수 있는 이름, 예: `corp_name`
- id: 보통 한 페이지에서 하나만 쓰는 고유 이름
- 속성: 태그 안에 들어있는 추가 정보, 예: `href`, `data-price`, `aria-label`

예를 들어 무신사 상품 HTML에서 가격은 화면 텍스트가 아니라 속성에 들어있을 수 있다.

```html
<a data-price="29900" data-item-name="셔츠" href="...">
```

이럴 때는 텍스트가 아니라 속성값을 가져온다.

## 4. requests란?

`requests`는 파이썬에서 웹페이지에 요청을 보내는 라이브러리다.

브라우저 주소창에 URL을 입력해서 페이지에 들어가는 것처럼, 파이썬 코드가 URL에 요청을 보낸다.

```python
import requests

url = "https://www.saramin.co.kr/zf_user/search"
response = requests.get(url)
```

`response`에는 서버가 보내준 응답이 들어있다.

```python
print(response)
```

결과가 이렇게 나오면:

```text
<Response [200]>
```

`200`은 요청이 성공했다는 뜻이다.

자주 보는 상태 코드:

- `200`: 성공
- `404`: 페이지를 찾을 수 없음
- `403`: 접근 거부
- `500`: 서버 오류

HTML 내용을 보고 싶으면:

```python
print(response.text)
```

## 5. BeautifulSoup이란?

`BeautifulSoup`은 HTML 문서를 파이썬에서 다루기 쉽게 바꿔주는 라이브러리다.

`requests`로 가져온 HTML은 그냥 긴 문자열이다. 그 상태로는 원하는 태그를 찾기 어렵다. `BeautifulSoup`을 사용하면 `find`, `select` 같은 기능으로 원하는 태그를 쉽게 찾을 수 있다.

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, "html.parser")
```

이제 `soup`에서 원하는 태그를 찾을 수 있다.

```python
titles = soup.find_all("span", class_="subject")
```

BeautifulSoup은 주로 정적 페이지를 크롤링할 때 사용한다.

## 6. Selenium이란?

`Selenium`은 실제 브라우저를 자동으로 조작하는 도구다.

`requests`는 서버에서 HTML만 받아오지만, `Selenium`은 Chrome 같은 브라우저를 직접 열어서 페이지를 로딩하고, 스크롤하고, 클릭할 수 있다.

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.musinsa.com/categories/item/001")
```

Selenium은 JavaScript로 데이터가 나중에 생기는 동적 페이지에서 많이 사용한다.

예를 들어 무신사처럼 상품 목록이 스크롤 후 나타나거나, 페이지 로딩 후 JavaScript가 상품을 그리는 경우에는 `requests`만으로 데이터가 안 잡힐 수 있다.

## 7. BeautifulSoup과 Selenium의 차이

둘 다 HTML에서 데이터를 찾는 데 사용하지만 역할이 다르다.

| 구분 | BeautifulSoup | Selenium |
|---|---|---|
| 역할 | HTML 파싱 | 브라우저 자동 조작 |
| 브라우저 실행 | 안 함 | 실제 Chrome 실행 |
| 속도 | 빠름 | 상대적으로 느림 |
| JavaScript 처리 | 못 함 | 가능 |
| 사용 상황 | HTML에 데이터가 바로 있을 때 | 스크롤, 클릭, 동적 로딩이 필요할 때 |
| 대표 코드 | `soup.select()` | `driver.find_elements()` |

정리하면:

```text
HTML 안에 데이터가 바로 있다 -> requests + BeautifulSoup
브라우저에서 봐야 데이터가 생긴다 -> Selenium
```

## 8. 정적 페이지와 동적 페이지

정적 페이지는 서버가 처음부터 완성된 HTML을 보내준다.

```python
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
```

동적 페이지는 처음 받은 HTML에는 데이터가 없고, JavaScript가 실행된 뒤 데이터가 생긴다.

이 경우 Selenium을 사용한다.

```python
driver.get(url)
time.sleep(2)
html = driver.page_source
```

크롤링했는데 결과가 비어 있다면, 다음 가능성을 확인해야 한다.

- 선택자가 틀렸는지
- 실제 HTML에 데이터가 없는지
- JavaScript로 나중에 데이터가 생기는지
- 로딩 전에 너무 빨리 찾은 것은 아닌지

## 9. find와 find_all

`find()`와 `find_all()`은 BeautifulSoup에서 태그를 찾을 때 사용한다.

`find()`는 조건에 맞는 첫 번째 요소 하나를 가져온다.

```python
title = soup.find("span", class_="subject")
```

`find_all()`은 조건에 맞는 모든 요소를 리스트로 가져온다.

```python
titles = soup.find_all("span", class_="subject")
```

반복되는 데이터를 수집할 때는 보통 `find_all()`을 쓴다.

```python
category = soup.find_all("span", class_="category")
subject = soup.find_all("span", class_="subject")
petition = soup.find_all("span", class_="text")

for c, s, t in zip(category, subject, petition):
    print(c.text, s.text, t.text)
```

## 10. select와 select_one

`select()`와 `select_one()`은 CSS 선택자 방식으로 태그를 찾는다.

`select_one()`은 조건에 맞는 첫 번째 요소 하나를 가져온다.

```python
title_tag = item.select_one(".job_tit a")
```

`select()`는 조건에 맞는 모든 요소를 리스트로 가져온다.

```python
items = soup.select("div.item_recruit")
```

정리하면:

```python
select_one()  # 하나만 필요할 때
select()      # 여러 개를 반복문으로 돌릴 때
```

사람인 크롤링에서는 공고가 여러 개이므로 먼저 `select()`로 공고 목록을 가져온다.

```python
items = soup.select("div.item_recruit")
```

그리고 반복문 안에서 회사명, 공고 제목 같은 값은 하나씩 가져온다.

```python
for item in items:
    company_tag = item.select_one(".area_corp .corp_name a")
    title_tag = item.select_one(".area_job .job_tit a")
```

## 11. find와 select 중 뭐가 더 좋은가?

둘 다 가능하다.

단순히 태그 하나를 찾을 때는 `find()`가 이해하기 쉽다.

```python
soup.find("span", class_="subject")
```

HTML 구조를 따라 들어가야 할 때는 `select_one()`이 더 편하다.

```python
item.select_one(".area_job .job_tit a")
```

예를 들어:

```html
<div class="area_job">
    <h2 class="job_tit">
        <a>공고 제목</a>
    </h2>
</div>
```

이 구조에서 `a` 태그를 찾을 때:

```python
# find 방식
job_area = item.find("div", class_="area_job")
job_tit = job_area.find("h2", class_="job_tit")
title = job_tit.find("a")

# select_one 방식
title = item.select_one(".area_job .job_tit a")
```

중첩 구조에서는 `select_one()`이 더 짧고 보기 좋다.

## 12. Selenium에서 요소 찾기

Selenium에서는 BeautifulSoup의 `find()`를 쓰면 안 된다.

Selenium의 요소는 `WebElement`라고 부른다.

`WebElement`에서는 `find_element()` 또는 `find_elements()`를 써야 한다.

```python
from selenium.webdriver.common.by import By

item.find_element(By.CSS_SELECTOR, "a span")
```

잘못된 예:

```python
item.find("a")
```

이렇게 쓰면 다음 에러가 날 수 있다.

```text
'WebElement' object has no attribute 'find'
```

이 뜻은 Selenium 객체에는 `find()`라는 기능이 없다는 뜻이다.

## 13. find_element와 find_elements

Selenium에서:

- `find_element()`: 하나만 찾음, 못 찾으면 에러
- `find_elements()`: 여러 개를 리스트로 찾음, 못 찾으면 빈 리스트

```python
a_tag = item.find_element(By.CSS_SELECTOR, "a[data-original-price]")
```

요소가 없을 수도 있으면 `find_elements()`가 더 안전하다.

```python
spans = item.find_elements(By.CSS_SELECTOR, "span")

if spans:
    name = spans[0].text.strip()
else:
    name = ""
```

## 14. 텍스트 가져오기

BeautifulSoup에서 텍스트를 가져올 때:

```python
title = title_tag.get_text(strip=True)
```

또는:

```python
title = title_tag.text.strip()
```

Selenium에서 텍스트를 가져올 때:

```python
name = element.text.strip()
```

`strip()`은 앞뒤 공백과 줄바꿈을 제거한다.

## 15. 속성값 가져오기

HTML에는 화면에 보이는 텍스트 말고 속성에 중요한 값이 들어있는 경우가 많다.

예시:

```html
<a href="https://www.musinsa.com/products/123"
   data-price="29900"
   data-item-name="셔츠">
```

BeautifulSoup에서 속성값 가져오기:

```python
link = tag.get("href")
```

Selenium에서 속성값 가져오기:

```python
link = a_tag.get_attribute("href")
price = a_tag.get_attribute("data-price")
name = a_tag.get_attribute("data-item-name")
```

무신사처럼 상품 정보가 `data-price`, `data-item-name`, `aria-label` 같은 속성에 들어있는 경우에는 `.text`보다 속성을 가져오는 것이 더 안정적일 수 있다.

## 16. headers란?

`headers`는 웹사이트에 요청을 보낼 때 “나는 이런 브라우저로 접속하는 사용자다”라고 알려주는 정보다.

일부 사이트는 파이썬 코드가 보낸 기본 요청을 막거나, 브라우저가 아닌 요청에 다른 결과를 줄 수 있다.

그래서 사람인 코드처럼 `User-Agent`를 넣어준다.

```python
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}

response = requests.get(base_url, headers=headers)
```

## 17. params란?

`params`는 URL 뒤에 붙는 검색 조건을 딕셔너리로 전달하는 기능이다.

예를 들어 사람인에서 `AI`를 검색할 때:

```python
response = requests.get(
    base_url,
    headers=headers,
    params={"searchword": "AI"},
    timeout=10
)
```

이 코드는 대략 이런 URL을 요청하는 것과 비슷하다.

```text
https://www.saramin.co.kr/zf_user/search?searchword=AI
```

## 18. timeout이란?

`timeout`은 응답을 기다릴 최대 시간이다.

```python
response = requests.get(url, timeout=10)
```

10초 안에 응답이 없으면 무한정 기다리지 않고 에러를 낸다.

크롤링할 때는 네트워크가 느려질 수 있으므로 `timeout`을 넣는 습관이 좋다.

## 19. sleep을 쓰는 이유

`sleep`은 일정 시간 기다리는 함수다.

```python
import time

time.sleep(2)
```

크롤링에서는 다음 상황에서 사용한다.

- 페이지가 완전히 로딩될 때까지 기다릴 때
- 스크롤 후 새로운 상품이 나타날 때까지 기다릴 때
- 너무 빠른 요청으로 서버에 부담을 주지 않기 위해

무신사 코드에서는 페이지 로딩 후, 스크롤 후에 기다리는 용도로 사용했다.

```python
driver.get(base_url)
time.sleep(2)

driver.execute_script("window.scrollTo(0, 2000)")
time.sleep(2)
```

## 20. 스크롤이 필요한 이유

일부 사이트는 처음부터 모든 상품을 보여주지 않고, 사용자가 아래로 스크롤하면 상품을 더 불러온다.

Selenium에서는 JavaScript를 실행해서 스크롤할 수 있다.

```python
driver.execute_script("window.scrollTo(0, 2000)")
```

뜻은 브라우저 창을 세로 위치 2000까지 내리라는 의미다.

## 21. driver.quit 위치

`driver.quit()`은 Selenium 브라우저를 종료하는 코드다.

반복문 안에 넣으면 첫 번째 상품을 처리하고 브라우저가 꺼진다. 그러면 다음 상품을 처리할 때 ChromeDriver와 연결이 끊겨 에러가 난다.

잘못된 예:

```python
for item in items:
    # 데이터 수집
    driver.quit()
```

올바른 예:

```python
for item in items:
    # 데이터 수집
    pass

driver.quit()
```

즉, `driver.quit()`은 모든 크롤링이 끝난 뒤 한 번만 실행한다.

## 22. 반복 데이터 수집 방식

크롤링에서는 보통 반복되는 큰 단위를 먼저 찾는다.

사람인:

```python
items = soup.select("div.item_recruit")
```

무신사:

```python
items = driver.find_elements(By.CSS_SELECTOR, ".sc-bSFBcf.iEkOIH")
```

그 다음 각 item 안에서 필요한 값을 뽑는다.

```python
for item in items:
    title = item.select_one(".job_tit a")
```

핵심은 “전체 페이지에서 아무거나 찾기”가 아니라 “공고 하나, 상품 하나 단위 안에서 찾기”다. 그래야 데이터가 서로 섞이지 않는다.

## 23. DataFrame이란?

`DataFrame`은 pandas에서 표 형태 데이터를 다루는 객체다.

엑셀 표처럼 행과 열이 있는 데이터라고 생각하면 된다.

```python
import pandas as pd

df = pd.DataFrame(rows)
```

예시:

```python
rows = [
    {"상품명": "셔츠", "가격": "29900"},
    {"상품명": "바지", "가격": "39000"},
]

df = pd.DataFrame(rows)
```

결과는 이런 표가 된다.

| 상품명 | 가격 |
|---|---|
| 셔츠 | 29900 |
| 바지 | 39000 |

## 24. CSV 저장

CSV는 표 데이터를 저장하는 파일 형식이다.

```python
df.to_csv("./musinsa_result.csv", index=False, encoding="utf-8-sig")
```

옵션 의미:

- `index=False`: 왼쪽에 0, 1, 2 같은 인덱스 번호를 저장하지 않음
- `encoding="utf-8-sig"`: 엑셀에서 한글이 깨지지 않게 저장

## 25. 딕셔너리와 중괄호 실수

수집한 데이터는 보통 딕셔너리로 저장한다.

올바른 예:

```python
item_list.append({
    "상품명": name,
    "브랜드명": brand,
    "가격": price,
    "링크": link
})
```

잘못된 예:

```python
item_list.append({
    "상품명": {name},
    "가격": {price}
})
```

`{name}`처럼 쓰면 문자열 치환이 아니라 `set` 자료형이 된다.

그래서 CSV에 이런 식으로 저장된다.

```text
{'셔츠'}
{'29900'}
```

변수 값을 넣을 때는 중괄호 없이 `name`이라고만 써야 한다.

중괄호는 f-string에서 사용한다.

```python
print(f"상품명: {name}")
```

## 26. DataFrame 컬럼명이 비는 이유

DataFrame을 만들 때 `columns`를 직접 지정하면, 딕셔너리의 key와 컬럼명이 정확히 같아야 한다.

```python
item_list.append({
    "상품명": name,
    "브랜드명": brand
})

df = pd.DataFrame(item_list, columns=["상품명", "브랜드명"])
```

만약 딕셔너리에는 `"브랜드명"`으로 저장했는데 DataFrame에서는 `"브랜드"`라고 쓰면 값이 비어 보일 수 있다.

## 27. 사람인 크롤링 코드 흐름

사람인 코드는 `requests + BeautifulSoup` 방식이다.

이유는 검색 결과 HTML 안에서 회사명, 공고 제목, 조건을 찾을 수 있기 때문이다.

기본 흐름:

```python
response = requests.get(
    base_url,
    headers=headers,
    params={"searchword": "AI"},
    timeout=10
)

soup = BeautifulSoup(response.text, "html.parser")
items = soup.select("div.item_recruit")
```

공고 하나에서 값 추출:

```python
for item in items:
    company_tag = item.select_one(".area_corp .corp_name a")
    title_tag = item.select_one(".area_job .job_tit a")
    condition_tag = item.select_one(".area_job .job_condition")

    company = company_tag.get_text(strip=True) if company_tag else ""
    title = title_tag.get_text(strip=True) if title_tag else ""
    condition = condition_tag.get_text(" ", strip=True) if condition_tag else ""
```

링크가 `/zf_user/...`처럼 상대경로이면 앞에 도메인을 붙인다.

```python
if link.startswith("/"):
    link = "https://www.saramin.co.kr" + link
```

## 28. 무신사 크롤링 코드 흐름

무신사 코드는 `Selenium` 방식이다.

이유는 상품 목록이 JavaScript와 스크롤에 의해 동적으로 나타날 수 있기 때문이다.

기본 흐름:

```python
driver = webdriver.Chrome(options=option)
driver.get(base_url)
time.sleep(2)

driver.execute_script("window.scrollTo(0, 2000)")
time.sleep(2)

items = driver.find_elements(By.CSS_SELECTOR, ".sc-bSFBcf.iEkOIH")
```

상품 하나에서 값 추출:

```python
for item in items:
    a_tag = item.find_element(By.CSS_SELECTOR, "a[data-original-price]")

    name = a_tag.get_attribute("aria-label")
    brand = a_tag.get_attribute("data-brand-id")
    price = a_tag.get_attribute("data-price")
    link = a_tag.get_attribute("href")
```

상품명 뒤에 불필요한 문구가 붙으면 제거한다.

```python
name = name.replace("상품상세로 이동", "").strip()
```

## 29. 청원 사이트 여러 페이지 크롤링 흐름

여러 페이지를 크롤링할 때는 URL 안의 페이지 번호를 바꿔가며 요청한다.

```python
max_pages = int(input("몇 페이지까지 크롤링할까요?"))
all_corpus = []

for page in range(1, max_pages + 1):
    url = f"https://www.cheongwon.go.kr/portal/petition/open/view?pageIndex={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
```

각 페이지에서 데이터를 뽑고 전체 리스트에 추가한다.

```python
category = soup.find_all("span", class_="category")
subject = soup.find_all("span", class_="subject")
petition = soup.find_all("span", class_="text")

for c, s, t in zip(category, subject, petition):
    all_corpus.append([c.text, s.text, t.text])
```

`tqdm`을 쓰면 진행 상황을 볼 수 있다.

```python
from tqdm import tqdm

for page in tqdm(range(1, max_pages + 1), desc="크롤링 진행중"):
    pass
```

## 30. 예외 처리

크롤링 중에는 어떤 상품이나 공고에서 원하는 태그가 없을 수 있다.

이때 프로그램이 바로 종료되지 않게 `try-except`를 사용한다.

```python
try:
    a_tag = item.find_element(By.CSS_SELECTOR, "a[data-original-price]")
    name = a_tag.get_attribute("aria-label")
except Exception as e:
    print(f"에러가 발생했습니다: {e}")
```

단, 모든 에러를 무조건 무시하면 진짜 문제를 놓칠 수 있다. 처음 공부할 때는 에러 메시지를 출력해서 원인을 확인하는 것이 좋다.

## 31. 안전하게 값 가져오기

태그가 없으면 `.text`를 바로 호출할 때 에러가 난다.

위험한 코드:

```python
title = item.select_one(".job_tit a").get_text(strip=True)
```

안전한 코드:

```python
title_tag = item.select_one(".job_tit a")
title = title_tag.get_text(strip=True) if title_tag else ""
```

Selenium에서도 마찬가지다.

```python
spans = item.find_elements(By.CSS_SELECTOR, "span")
name = spans[0].text.strip() if spans else ""
```

## 32. 자주 만난 에러와 의미

### `<Response [200]>`가 출력됨

에러가 아니다. 요청 성공이라는 뜻이다.

```python
print(response)
```

HTML을 보고 싶으면:

```python
print(response.text)
```

### `df.head()`가 출력되지 않음

`.py` 파일에서는 마지막 줄에 `df.head()`만 쓰면 자동 출력되지 않는다.

```python
print(df.head())
```

또는 DataFrame이 비어 있을 수도 있으니 길이를 확인한다.

```python
print(len(df))
```

### `'WebElement' object has no attribute 'find'`

Selenium 요소에 BeautifulSoup 문법을 쓴 경우다.

```python
# 잘못된 코드
item.find("a")

# 올바른 코드
item.find_element(By.CSS_SELECTOR, "a")
```

### `no such element`

선택자에 해당하는 요소를 찾지 못했다는 뜻이다.

원인:

- 선택자가 틀림
- 해당 item에는 그 태그가 없음
- 아직 로딩되지 않음
- 내가 생각한 HTML 구조와 실제 구조가 다름

디버깅:

```python
print(a_tag.get_attribute("outerHTML"))
```

### `HTTPConnectionPool(host='localhost'...)`

Selenium의 ChromeDriver 연결이 끊긴 상태에서 계속 명령을 보낼 때 발생할 수 있다.

대표 원인:

```python
for item in items:
    driver.quit()
```

`driver.quit()`은 반복문 밖으로 빼야 한다.

## 33. 크롤링할 때 확인할 순서

데이터가 안 나올 때는 다음 순서로 확인한다.

1. `response.status_code`가 200인지 확인
2. `response.text[:1000]`으로 HTML 일부 확인
3. 개발자도구에서 실제 태그/class 확인
4. `find_all` 또는 `select` 결과 개수 확인
5. 정적 페이지인지 동적 페이지인지 확인
6. Selenium이라면 로딩 시간과 스크롤 여부 확인
7. 태그가 없는 경우를 대비해 예외 처리 추가

## 34. 크롤링 기본 템플릿

### requests + BeautifulSoup 템플릿

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "크롤링할_URL"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, "html.parser")

items = soup.select("반복_단위_선택자")
rows = []

for item in items:
    title_tag = item.select_one("제목_선택자")
    title = title_tag.get_text(strip=True) if title_tag else ""

    rows.append({
        "제목": title
    })

df = pd.DataFrame(rows)
df.to_csv("result.csv", index=False, encoding="utf-8-sig")
```

### Selenium 템플릿

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

option = Options()
driver = webdriver.Chrome(options=option)

driver.get("크롤링할_URL")
time.sleep(2)

items = driver.find_elements(By.CSS_SELECTOR, "반복_단위_선택자")
rows = []

for item in items:
    try:
        title_tag = item.find_element(By.CSS_SELECTOR, "제목_선택자")
        title = title_tag.text.strip()

        rows.append({
            "제목": title
        })

    except Exception as e:
        print(f"에러 발생: {e}")

driver.quit()

df = pd.DataFrame(rows)
df.to_csv("result.csv", index=False, encoding="utf-8-sig")
```

## 35. 핵심 요약

크롤링은 웹페이지의 HTML에서 원하는 데이터를 자동으로 뽑아내는 작업이다.

`requests`는 웹페이지를 요청하고, `BeautifulSoup`은 받은 HTML을 분석한다.

`Selenium`은 실제 브라우저를 조작해서 JavaScript로 만들어지는 데이터까지 가져올 수 있다.

정적 페이지는 `requests + BeautifulSoup`, 동적 페이지는 `Selenium`을 사용한다.

여러 데이터를 가져올 때는 반복되는 큰 단위를 먼저 찾고, 그 안에서 필요한 값을 하나씩 추출한다.

수집한 데이터는 리스트와 딕셔너리에 담고, `pandas.DataFrame`으로 표를 만든 뒤 CSV로 저장한다.

크롤링에서 가장 중요한 습관은 “내가 찾는 태그가 실제 HTML에 있는지 먼저 확인하는 것”이다.
