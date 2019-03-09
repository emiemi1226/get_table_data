# coding: UTF-8

from urllib.request import urlopen
from urllib.parse import unquote
from bs4 import BeautifulSoup
import csv
import re

# 今回求めた結果を入れる変数
sum_anime_title = 0
sum_anime_story =0

# wikiのURL 取得したhrefに正しくアクセスするために利用
wiki_url = "https://ja.wikipedia.org"

# アニメの一覧が載っているURL
root_url = "https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E3%81%AE%E3%83%86%E3%83%AC%E3%83%93%E3%82%A2%E3%83%8B%E3%83%A1%E4%BD%9C%E5%93%81%E4%B8%80%E8%A6%A7"

# html情報をすべて取得
html = urlopen(root_url)

# Bs4で扱える状態にする
soup = BeautifulSoup(html, "html.parser")

# ulをすべて取得する
uls = soup.findAll("ul")

# アクセスするURLの一覧を配列として保存する
url_list = []

# 取得したulから必要なリンク情報を取得する
for ul in uls:
    csvRow = []
    # 作品一覧の家で必要なリンクを絞り込み
    for link_title in ul.findAll("li", text = re.compile("日本のテレビアニメ作品一覧.*\)")):
        url_list.append(link_title.find("a").get("href"))

# 取得したリンクからデータを所得していく。
for url in url_list:
  calc_num = 0
  print(unquote(url)+" データ取得中...")
  
  # 取得したデータを保存しておくためのファイルを開く  ※計算までこのプログラムで行うので必要は無いが他に役立つかもしれないので一応残留
  csvFileTitle = unquote(url.lstrip("/wiki/"))+".csv"
  csvFile = open(csvFileTitle, 'w', encoding = 'utf-8')
  writer = csv.writer(csvFile)

  # URLにアクセスする 全htmlが帰ってくる
  html = urlopen(wiki_url+url)

  # Bs4で扱える状態にする
  soup = BeautifulSoup(html, "html.parser")

  # 利用するテーブルを取得する 今回は「wikitable」という名前だったのでこちらを利用
  tables = soup.findAll("table",{"class":"wikitable"})

  try:
    # table→tr→tdと階層を降りていく
    for table in tables:
        rows = table.findAll("tr")
        for row in rows:
            csvRow = []
            for cell in row.findAll("td"):
                # 保存するためのリストを作成する
                csvRow.append(cell.get_text().strip())

            # 不要なデータを計算に入れないために、データが入ってないセルの場合は書き込まない。
            if csvRow != []:
                # 総タイトル数を計算
                sum_anime_title += 1
                
                # 総話数を計算
                # 不要な文字列と数字を削除する
                story_num = re.sub(r'\[.*\]', '', str(csvRow[4])).strip()
                story_num = re.sub(r'\D', '', str(story_num).strip())
                if story_num != '':
                    sum_anime_story += int(story_num)
                # 1タイトルごとに書き込みを行う
                writer.writerow(csvRow)
        calc_num += 1
        print(unquote(url)+str(calc_num) + "  年分の計算完了")
    print(unquote(url)+"  正常にデータを取得しました\n")
  except Exception as e:
    print("例外:", e.args)
    print(unquote(url)+"  データの取得に失敗しました。。。。\n")
  finally:
    csvFile.close()


# 結果出力
print("\n\n======== 結果 =========\n")
print("■ 総アニメタイトル数:"+str(sum_anime_title)+"タイトル"+"\n")
print("■ 総アニメ話数     :"+str(sum_anime_story)+"話"+"\n")
print("■ 総放送時間　　　　:"+str(sum_anime_story/2)+"時間\n")
print("======================")



