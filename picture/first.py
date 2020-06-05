import requests
from bs4 import BeautifulSoup
import os
import sys

def download_site_imgs(url, path):
    img_urls = []

    # パス（保存先）が存在しなければ新規作成
    if not os.path.exists(path):
        os.makedirs(path)

    # htmlのパース
    soup = BeautifulSoup(requests.get(url).content,'lxml')

    # 画像リンクなら(拡張子がjpgなど)リストに追加
    for img_url in soup.find_all("img"):
        # imgタグのsrc要素を抽出
        src = img_url.get("src")
        #src要素に画像の拡張子が含まれていたらリストに追加
        if 'jpg' in src:
            img_urls.append(src)
        elif 'png' in src:
            img_urls.append(src)


    # 画像リンク先のデータをダウンロード
    for img_url in img_urls:
        re = requests.get(img_url)
        print('Download:', img_url)
        with open(path + img_url.split('/')[-1], 'wb') as f: # imgフォルダに格納
            f.write(re.content)


if __name__ == '__main__':
    download_site_imgs('http://kazukipk.blog.fc2.com/blog-entry-433.html', 'stamp/')
