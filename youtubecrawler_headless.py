from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import string

# 최신 크롬 드라이버 사용하도록 세팅: 현재 OS에 설치된 크롬 브라우저 버전에 맞게 cache에 드라이버 설치
from selenium.webdriver.chrome.service import Service
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")


f = open("musicbook_TJ.txt", "r")
strings = f.readlines()
f.close()
f = open("youtube_Url.txt", "a")
f2 = open("fail.txt", "a")


for info in strings:
    keyword = ""
    number = "" 
    count = 0
    # 문자열에서 키워드와 번호 파싱
    for e in info:
        if (e == '^'): 
            count += 1
            if (count == 1): 
                keyword += " "
            elif (count == 3):
                break
            continue
        else:
            if (count == 2):
                number += e
            else:
                keyword += e
    driver = webdriver.Chrome(service=service, options=options)
    # 검색시 특수문자가 있으면 검색이 안되기 때문에 특수문자 제거
    for character in string.punctuation:
        keyword = keyword.replace(character, ' ')
    # 검색 키워드 설정: 키워드 내 띄어쓰기는 URL에서 '+'로 표시되기 때문에 이에 맞게 변환
    SEARCH_KEYWORD = keyword.replace(' ', '+')
    # 스크래핑 할 URL 세팅
    URL = "https://www.youtube.com/results?search_query=" + SEARCH_KEYWORD
    # 크롬 드라이버를 통해 지정한 URL의 웹 페이지 오픈
    driver.get(URL)
    time.sleep(2)
    # 페이지 소스 추출
    html_source = driver.page_source
    soup_source = BeautifulSoup(html_source, 'html.parser')
    # 모든 콘텐츠 정보
    content_total = soup_source.find_all(class_ = 'yt-simple-endpoint style-scope ytd-video-renderer')
    # 콘텐츠 링크만 추출
    content_total_link = list(map(lambda data: "https://youtube.com" + data["href"], content_total))
    driver.quit()
    # 크롤링 실패시 fail.txt에 저장
    if (not content_total_link):
        f2.write(info)
        print(info + "크롤링 실패!!!")
        continue
    # 반복되는 url 문자열 제거
    url = str(content_total_link[0]).replace('https://youtube.com/watch?v=','')
    f.write(number + '^' + url + '^' + '\n')
f.close()
f2.close()
