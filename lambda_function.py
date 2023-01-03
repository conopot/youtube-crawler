import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_driver():
    # chrome driver option 설정
    try:
        options = Options()
        options.binary_location = '/opt/headless-chromium'
        options.add_argument('lang=en')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1500,1000")
        options.add_argument(
            'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)
        return driver
        
    except Exception as e:
        return e

def lambda_handler(event, context):
    # driver 설정
    driver = get_driver()
    # 검색 키워드 설정: 키워드 내 띄어쓰기는 URL에서 '+'로 표시되기 때문에 이에 맞게 변환
    event = json.loads(event['body'])
    keyword = event['title']
    SEARCH_KEYWORD = keyword.replace(' ', '+')
    # 스크래핑 할 URL 세팅
    URL = "https://www.youtube.com/results?search_query=" + SEARCH_KEYWORD
    # 크롬 드라이버를 통해 지정한 URL의 웹 페이지 오픈
    driver.get(URL)
    time.sleep(3)
    # 페이지 소스 추출
    html_source = driver.page_source
    soup_source = BeautifulSoup(html_source, 'html.parser')
    
    driver.close()
    driver.quit()
    
    # 모든 콘텐츠 정보
    content_total = soup_source.find_all(class_ = 'yt-simple-endpoint style-scope ytd-video-renderer')
    # 콘텐츠 링크만 추출
    content_total_link = list(map(lambda data: "https://youtube.com" + data["href"], content_total))
 
    
    response = {
        "statusCode": 200,
        "body": json.dumps(content_total_link[1])
    }

    return response