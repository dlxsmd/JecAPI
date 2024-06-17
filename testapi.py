from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import html

app = Flask(__name__)

# 記事一覧を取得する関数
def get_articles():
    url = "https://www.jec.ac.jp/urgent-news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    for a in soup.find_all('a', href=True):
        title = a.text.strip()
        link = a['href']
        if link.startswith('/urgent-news/'):  # 絶対URLにする
            link = "https://www.jec.ac.jp" + link
            article_id = link.split('/')[-2]  # URLから記事IDを取得
            articles.append({
                'id': article_id,
                'title': title,
                'link': link
            })
    
    return articles

# 記事詳細を取得する関数
def get_article_detail(article_id):
    url = "https://www.jec.ac.jp/urgent-news/{article_id}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('h1').text.strip()
    content = soup.find('div', class_='entry-content').text.strip()
    
    return {
        'id': article_id,
        'title': title,
        'content': content
    }

@app.route('/api/articles', methods=['GET'])
def articles():
    articles = get_articles()
    return jsonify(articles)

@app.route('/api/articles/detail', methods=['GET'])
def article_detail():
    article_id = request.args.get('id')
    if not article_id:
        return jsonify({'error': '記事IDが指定されていません'}), 400
    
    detail = get_article_detail(article_id)
    return jsonify(detail)

if __name__ == '__main__':
    app.run(debug=True)
