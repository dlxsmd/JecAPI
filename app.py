from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re
import html
import time

app = Flask(__name__)

# キャッシュ変数を初期化
cache = {
    "data": None,
    "timestamp": None
}
CACHE_TIMEOUT = 300  # キャッシュの有効期間（秒）

def get_articles():
    url = "https://www.jec.ac.jp/urgent-news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    article_elements = soup.find_all('dl', class_='urgentNewsWrap')  # 記事のリストを含む要素を取得

    for element in article_elements:
        date_element = element.find('dt', class_='urgentNews__date')
        date = date_element.text.strip() if date_element else 'No Date'
        
        a = element.find('a', href=True)
        if a:
            title = html.unescape(a.text.strip())  # タイトルの文字列をデコード
            link = a['href']
            if re.match(r'https://www\.jec\.ac\.jp/urgent-news/\d+', link):  # 指定された形式のリンクのみを抽出
                articles.append({
                    'title': title,
                    'link': link,
                    'date': date
                })

    return articles

@app.route('/api/articles', methods=['GET'])
def articles():
    current_time = time.time()
    # キャッシュが有効か確認
    if cache["data"] and cache["timestamp"] and (current_time - cache["timestamp"] < CACHE_TIMEOUT):
        return jsonify(cache["data"])

    # キャッシュが無効な場合、データを取得
    articles = get_articles()
    cache["data"] = articles
    cache["timestamp"] = current_time

    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)
