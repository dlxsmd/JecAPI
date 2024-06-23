from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import re
import html
import time

app = Flask(__name__)

# キャッシュ変数を初期化
cache = {
    "important": {
        "data": None,
        "timestamp": None
    },
    "news": {}
}
CACHE_TIMEOUT = 300  # キャッシュの有効期間（秒）

def get_important():
    url = f"https://www.jec.ac.jp/urgent-news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    important = []
    article_elements = soup.find_all('dl', class_='urgentNewsWrap')  # 記事のリストを含む要素を取得

    for element in article_elements:
        date_element = element.find('dt', class_='urgentNews__date')
        date = date_element.text.strip() if date_element else 'No Date'
        
        a = element.find('a', href=True)
        if a:
            title = html.unescape(a.text.strip())  # タイトルの文字列をデコード
            link = a['href']
            if re.match(r'https://www\.jec\.ac\.jp/urgent-news/\d+', link):  # 指定された形式のリンクのみを抽出
                important.append({
                    'title': title,
                    'link': link,
                    'date': date
                })

    return important

def get_news(page):
    url = f"https://www.jec.ac.jp/collegenews/page/{page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    news = []
    news_elements = soup.find_all('div', class_='p-NewsContSpList')  # ニュースのリストを含む要素を取得

    for element in news_elements:
        date_element = element.find('div', class_='c-news__data')
        date = date_element.text.strip() if date_element else 'No Date'
        
        a = element.find('a', href=True)
        if a:
            title = html.unescape(a.find('p').text.strip())  # タイトルの文字列をデコード
            link = a['href']
            image_element = element.find('div', class_='c-newsContImg')
            image_url = image_element['style'].split('url(')[-1].split(')')[0].strip("'") if image_element else ''
            if re.match(r'https://www\.jec\.ac\.jp/collegenews/[\w/]+/\d+/', link):  # 指定された形式のリンクのみを抽出
                news.append({
                    'title': title,
                    'link': link,
                    'date': date,
                    'image': image_url
                })

    return news

@app.route('/api/important', methods=['GET'])
def important():
    current_time = time.time()
    # キャッシュが有効か確認
    if cache["important"]["data"] and cache["important"]["timestamp"] and (current_time - cache["important"]["timestamp"] < CACHE_TIMEOUT):
        return jsonify(cache["important"]["data"])

    # キャッシュが無効な場合、データを取得
    important = get_important()
    cache["important"]["data"] = important
    cache["important"]["timestamp"] = current_time

    return jsonify(important)

@app.route('/api/news', methods=['GET'])
def news():
    page = request.args.get('page', default=1, type=int)
    news_data = get_news(page)
    return jsonify(news_data)

if __name__ == '__main__':
    app.run(debug=True)
