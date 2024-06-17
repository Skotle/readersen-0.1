import time
import requests
import random
from bs4 import BeautifulSoup
import openpyxl
import numpy as np
import os
import matplotlib.pyplot as plt
from custom_classes.custom_analyzer import CustomAnalyzer

start_page = int(input('시작 페이지 : '))
page = start_page
end_page = int(input('종료 페이지 : '))

baseurl = "https://gall.dcinside.com/"
middleurl = "mini/board/lists/?id=2008"

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"}

analyzer = CustomAnalyzer()

total = [0,0,0,0]

day = []
toti = 0
while True:
    key = baseurl+middleurl+"&page="+str(page)
    response = requests.get(key, headers=headers)
    html = BeautifulSoup(response.content, 'html.parser')

    tr = html.find('tbody').find_all('tr')

    name = []
    view = []
    recoms = []
    com = []
    for i in range(len(tr)):
        if tr[i].find('td', {'class':'gall_subject'}).text not in ['공지','고정','설문','이슈']:
            nk = tr[i].find('td', {'class' : 'gall_writer ub-writer'}).text[1:-1]
            co = int(tr[i].find('td', {'class' : 'gall_count'}).text)
            ro = int(tr[i].find('td', {'class':'gall_recommend'}).text)
            rp = tr[i].find('span', {'class':'reply_num'})
            total[0] += 1
            total[1] += co
            total[2] += ro
            
            if rp != None:
                rp = int(rp.text[1])
                total[3] += rp
            else:
                rp = 0

            if nk[:2] not in ['ㅇㅇ'] and nk != '익명의팔붕이':
                name.append(nk)
                view.append(co)
                recoms.append(ro)
                com.append(rp)
                day.append(tr[i].find('td', {'class' : 'gall_date'}).text)

    analyzer.analyze_data(name, view, recoms, com)
    print(f"진행도 : {page - start_page + 1}/{end_page - start_page + 1}")
    if page >= end_page:
        break
    page += 1

result_sorted = analyzer.get_classes_sorted_by_num()

n = 1
d = '%'

viag = total[1] / total[0]
reag = total[2] / total[0]
plag = total[3] / total[0]

savefile = openpyxl.Workbook()
sheet = savefile.active
data = []
data1 = []
data2 = []
data3 = []
sheet.append(['순위', '이름', '글 수', '전체 지분율', '평균 조회수', '편차율', '평균 추천 수', '편차율', '평균 댓글 수', '편차율'])

for seunil in result_sorted:
    data.append(seunil.num)
    data1.append(seunil.view)
    data2.append(seunil.recom)
    data3.append(seunil.reple)

dev = np.std(data)
dev1 = np.std(data1)
dev2 = np.std(data2)
dev3 = np.std(data3)

for seunil in result_sorted:
    print("%d위 / %s : %d글(%.2f%s)" % (n, seunil.name, seunil.num, seunil.num / total[0] * 100, d))
    
    if (seunil.view / seunil.num - viag) / viag * 100 >= 0:
        mov = '+' + str('%.2f' % ((seunil.view / seunil.num - viag) / viag * 100)) + "%"
    else:
        mov = str('%.2f' % ((seunil.view / seunil.num - viag) / viag * 100)) + "%"

    if (seunil.recom / seunil.num - reag) / reag * 100 >= 0:
        rev = '+' + str('%.2f' % ((seunil.recom / seunil.num - reag) / reag * 100)) + "%"
    else:
        rev = str('%.2f' % ((seunil.recom / seunil.num - reag) / reag * 100)) + "%"

    if (seunil.reple / seunil.num - plag) / plag * 100 >= 0:
        plv = '+' + str('%.2f' % ((seunil.reple / seunil.num - plag) / plag * 100)) + "%"
    else:
        plv = str('%.2f' % ((seunil.reple / seunil.num - plag) / plag * 100)) + "%"
    
    sheet.append([n, seunil.name, seunil.num, str(round(seunil.num / total[0] * 100, 2)) + "%", seunil.view, mov, seunil.recom, rev, seunil.reple, plv])
    print("평균 조회수 : %.2f회(%s)\n평균 추천 수 : %.2f개(%s)\n평균 댓글 수 : %.2f개(%s)\n\n" % (seunil.view / seunil.num, mov, seunil.recom / seunil.num, rev, seunil.reple / seunil.num, plv))
    n += 1
    
sheet.append(['-', "전체 평균값", '-', '-', round(viag, 2), '0%', round(reag, 2), '0%', round(plag, 2), '0%'])
sheet.append(['-', "표준 편차", '-', '-', "±" + str(round(dev1, 2)), "±" + str(round(dev1 / viag * 100, 2)) + "%", "±" + str(round(dev2, 2)), "±" + str(round(dev2 / reag * 100 - 100, 2)) + "%", "±" + str(round(dev3, 2)), "±" + str(round(dev3 / plag * 100, 2)) + "%"])
savefile.save('example.xlsx')

print("총계\n누적 게시글 : %d글\n누적 조회수 : %d회\n누적 추천 수 : %d개\n누적 댓글 수 : %d개" % (total[0], total[1], total[2], total[3]))
