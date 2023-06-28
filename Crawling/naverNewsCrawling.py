from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import re
import numpy as np
import pandas as pd
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

#웹드라이버 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# ConnectionError방지
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102" }

#크롤링시 필요한 라이브러리 불러오기
from bs4 import BeautifulSoup
import requests
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

#웹드라이버 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

import pandas as pd
start_date='20220701'
end_date='20230430'
date_list=pd.date_range(start=start_date, end=end_date, freq='D')
date_list_str =[]
# 평일만 추출 시 weekday() <= 4, "7"일때는 모든 날짜
for i in range(len(date_list)):
    if date_list[i].weekday()<=7:    
        s = str(date_list[i])
        s = s[0:10].replace('-','.')
        date_list_str.append(s)

# 생성된 날짜 확인
print(len(date_list_str))
print(date_list_str)

# 페이지 url 형식에 맞게 바꾸어 주는 함수 만들기
  #입력된 수를 1, 11, 21, 31 ...만들어 주는 함수
def makePgNum(num):
    if num == 1:
        return num
    elif num == 0:
        return num+1
    else:
        return num+9*(num-1)


# 날짜 없이 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 시작 페이지, 크롤링 종료 페이지)
def makeUrl(search,start_pg,end_pg):
    if start_pg == end_pg:
        start_page = makePgNum(start_pg)
        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(start_page) 
        print("생성url: ",url)
        return url
    else:
        urls= []
        for i in range(start_pg,end_pg+1):
            page = makePgNum(i)
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(page)
            urls.append(url)
        print("생성url: ",urls)
        return urls
    
    

# 날짜 있이 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 시작 페이지, 크롤링 종료 페이지)
def makeUrl(search,date,start_pg,end_pg):
    if start_pg == end_pg:
        start_page = makePgNum(start_pg) 
        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&sort=0&photo=0&field=0&pd=3&ds="+ date + "&de=" + date + "&cluster_rank=82&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20221218to20221218,a:all&start=" + str(start_page)
        print("생성url: ",url)
        return url
    else:
        urls= []
        for i in range(start_pg,end_pg+1):
            page = makePgNum(i)
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&sort=0&photo=0&field=0&pd=3&ds="+ date + "&de=" + date + "&cluster_rank=82&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20221218to20221218,a:all&start=" + str(page)
            urls.append(url)
        print("생성url: ",urls)
        return urls
    
##########뉴스크롤링 시작###################
search_list = ['인공지능']
search_urls = []
for search in search_list:
    for date in date_list_str:
        page=1
        page2=1
        #검색 시작할 페이지 입력
        #page = int(input("\n크롤링할 시작 페이지를 입력해주세요. ex)1(숫자만입력):")) # ex)1 =1페이지,2=2페이지...
        #print("\n크롤링할 시작 페이지: ",page,"페이지")   
        #검색 종료할 페이지 입력
        #page2 = int(input("\n크롤링할 종료 페이지를 입력해주세요. ex)1(숫자만입력):")) # ex)1 =1페이지,2=2페이지...
        #print("\n크롤링할 종료 페이지: ",page2,"페이지")

        #검색할 날짜 지정
        #date = input("\n크롤링할 날짜를 입력해주세요. ex)2022.12.16(해당양식입력):") # ex)1 =1페이지,2=2페이지...
        # naver url 생성
        t = makeUrl(search,date,page,page2)
        search_urls.append(t)


## selenium으로 navernews만 뽑아오기##
# 버전에 상관 없이 os에 설치된 크롬 브라우저 사용
chrome_options = webdriver.ChromeOptions()
# headless 설정은 백그라운드로 돌릴거면 주석 해제, 주석 시 크롤링 모습 보여줌.
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument("--single-process")
#chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
driver.implicitly_wait(3)

from collections import defaultdict
d = defaultdict(str)


# selenium으로 검색 페이지 불러오기 #

naver_urls=[]

for i in search_urls:
    driver.get(i)
    time.sleep(1) #대기시간 변경 가능
    
    #정규표현식으로 해당 url에서 검색어 추출 (종목 추출)
    name = re.search('(?<=query=)\w+(?=&sort)', i).group()

    # 네이버 기사 눌러서 제목 및 본문 가져오기#
    # 네이버 기사가 있는 기사 css selector 모아오기
    a = driver.find_elements(By.CSS_SELECTOR,'a.info')
    try:
        # 위에서 생성한 css selector list 하나씩 클릭하여 본문 url얻기
        for i in a:
            try:
                i.click()

                # 현재탭에 접근
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(3) #대기시간 변경 가능

                # 네이버 뉴스 url만 가져오기

                url = driver.current_url
                print(url)

                if "news.naver.com" in url:
                    # naver_urls.append(url)
                    d[url] = name
    
                else:
                    pass
                
                # 현재 탭 닫기
                driver.close()

                # 다시처음 탭으로 돌아가기(매우 중요!!!)
                driver.switch_to.window(driver.window_handles[0])
            except:
                pass
    except:
        pass

driver.quit() # 모든 탭 끄는거
# print(f'해당 페이지 네이버 뉴스 개수는 {len(naver_urls)}개, 주소 리스트는{naver_urls}')
print(d)

naver_urls = list(d.keys())
stock = list(d.values())

###naver 기사 본문 및 제목 가져오기###
stocks =[]
titles = []
contents=[]
dates=[]

# ConnectionError방지
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102" }

for i in range(len(naver_urls)):
    original_html = requests.get(naver_urls[i],headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")
    # 검색결과확인시
    #print(html)
    
    #종목명 가져오기
    stocks.append(stock[i])
    
    #뉴스 제목 가져오기
    title = html.select("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2") # F12에서 제목 파트 클릭 후 우클릭 > copy > copy selector 눌러서 나오는 정보 가져오면 됨.
    # list합치기
    title = ''.join(str(title))
    # html태그제거
    pattern1 = '<[^>]*>'
    title = re.sub(pattern=pattern1,repl='',string=title)
    titles.append(title)
    
    #뉴스 날짜 가져오기
    date = html.select("#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
    try: #뉴스 날짜가 없는 경우가 있어서 try except로 처리
        date = re.search('date-time="(.+)"',str(date[0])).groups()[0] #정규표현식, 동호가 알려줌.
        dates.append(date) #날짜가 있으면 dates에 추가
    except:
        dates.append('None') #날짜가 없으면 dates에 None 추가

    #뉴스 본문 가져오기

    content = html.select("#dic_area") # F12에서 본문 파트 클릭 후 우클릭 > copy > copy selector 눌러서 나오는 정보 가져오면 됨.

    # 기사 텍스트만 가져오기
    # list합치기
    content = ''.join(str(content))
    
    #html태그제거 및 텍스트 다듬기
    content = re.sub(pattern=pattern1,repl='',string=content)
    pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
    content = content.replace(pattern2,'')

    contents.append(content)
    
    #

'''for i in range(2):
    print(titles[i])
    print(contents[i])'''
print('title의 길이는',len(titles))
print('dates의 길이는',len(dates))
print('contents의 길이는',len(contents))
print('stocks의 길이는',len(stocks))

import pandas as pd

#df 저장
df04 = pd.DataFrame({'title':titles, 'date':dates, 'content':contents, 'name':stocks, 'url':naver_urls})
df04.to_csv('/home/dan/텍스트마이닝/3_final_project/Crawling/AInews_crawling.csv', encoding='utf-8')