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
    for a in soup.find_all('a', href=True):
        title = html.unescape(a.text.strip())  # タイトルの文字列をデコード
        link = a['href']
        if re.match(r'https://www\.jec\.ac\.jp/urgent-news/\d+', link):  # 指定された形式のリンクのみを抽出
            articles.append({
                'title': title,
                'link': link
            })
    
    return articles

@app.route('/api/articles', methods=['GET'])
def articles():
    articles=get_articles()
    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)
