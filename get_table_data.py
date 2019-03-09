import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen

# ファイル名を指定
# file = open('test.html')

# URLで
root_url = "https://www.lpga.or.jp/tournament/reranking/2019/qt"
html = urlopen(root_url)

# html = file.read()
# file.close()

# ビューティフルスープでテーブルの内容をCSV化
soup = BeautifulSoup(html, "html.parser")
tables = soup.findAll("table")

# 保存するファイルの形式
csvFile = open("201903_table.csv", 'wt', encoding = 'utf-8')
writer = csv.writer(csvFile)
for table in tables:
    for rows in table.findAll(['tr']):
        csvRow = []
        for cell in rows.findAll(['td']):
            csvRow.append(cell.get_text())
        writer.writerow(csvRow)
        # コマンドラインに出力
        print(csvRow)
# ファイルを閉じる
csvFile.close()