from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re
import html

app = Flask(__name__)

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
    articles = get_articles()
    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)
