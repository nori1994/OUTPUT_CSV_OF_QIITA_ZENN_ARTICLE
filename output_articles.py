import feedparser
import sys
import requests
import json
import os
import urllib.parse
from datetime import datetime
from dateutil import tz

QIITA_PAGE = 1
QIITA_PER_PAGE = 100

def get_qiita_articles(user_id, page, per_page):
  res = requests.get(f"https://qiita.com/api/v2/users/{user_id}/items?page={page}&per_page={per_page}")
  articles_json = json.loads(res.text)
  total_article_num = int(res.headers['Total-Count'])
  return total_article_num, articles_json

def write_qiita_articles(user_id, write):
    total_article_num, articles_json = get_qiita_articles(user_id, QIITA_PAGE, QIITA_PER_PAGE)
    for item in articles_json:
        write(f"{datetime.strptime(item['created_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y/%m/%d')}, {item['title']},\n")

    pagination_num = total_article_num/QIITA_PER_PAGE + 1

    if pagination_num > QIITA_PER_PAGE:
        for page_num in range(QIITA_PAGE + 1, pagination_num):
            articles_json = get_qiita_articles(page_num, QIITA_PER_PAGE)
            for item in articles_json:
                write(f"{datetime.strptime(item['created_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y/%m/%d')}, {item['title']},\n")


def write_zenn_articles(user_id, write):
    response = requests.get(f"https://zenn.dev/{user_id}/feed?all=1")
    response.encoding = response.apparent_encoding
    feed = feedparser.parse(response.text)
    for entry in feed.entries:
        entry_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
        from_zone = tz.gettz('UTC')
        utc = entry_date.replace(tzinfo=from_zone)
        to_zone = tz.gettz('Asia/Tokyo')
        write(f"{utc.astimezone(to_zone).strftime('%Y/%m/%d')}, {entry.title},\n")

if len(sys.argv) != 3:
    print('ArgumentError: No Argument. First argument must be either qiita or zenn. Second argument must be user_id.')
    sys.exit()

site = sys.argv[1]
if not site in ['qiita', 'zenn']:
    print('ArgumentError: Argument must be either qiita or zenn')
    sys.exit()

if not os.path.exists('output'):
    os.mkdir('output')

user_id = urllib.parse.quote(sys.argv[2])
with open(f'output/{site}_articles.csv', mode='w', newline='\n', encoding='utf-8') as f:
    f.write("published, title,\n")
    if site == 'qiita':
        write_qiita_articles(user_id, f.write)
    else:
        write_zenn_articles(user_id, f.write)
