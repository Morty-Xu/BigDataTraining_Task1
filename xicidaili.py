import requests
import csv
from bs4 import BeautifulSoup

def checkValidity(ip):
    proxies = "http://" + str(ip)
    try:
        requests.get('https://www.baidu.com/', proxies={"http": proxies})
    except:
        return False
    else:
        return True

headers = {
    'Connection': 'keep-alive',
    # 模拟浏览器操作
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.142 Safari/537.36'
}

nn = requests.get('https://www.xicidaili.com/nn/', headers = headers)

soup_nn = BeautifulSoup(nn.text, 'lxml')

table_nn = soup_nn.find('table', id='ip_list')
# 提取国内高匿代理页面的表头
ths = table_nn.find_all('th', limit=6)
headers = []
for n in ths:
    headers.append(n.string)
    # print(n.string)
# 去除 国家 元素
headers.remove('国家')

# 提取国内高匿代理页面的表格值
rows = []
for idx, tr in enumerate(table_nn.find_all('tr')):
    if idx != 0:
        tds = tr.find_all('td', limit=6)
        row = []
        for num, n in enumerate(tds):
            if num != 0:
                if num == 3:
                    row.append(n.find('a'))
                else:
                    row.append(n.string)
        if checkValidity(row[1]):
            rows.append(row)

csv_file = open('nn_csv.csv', 'a', newline='')
csv_write = csv.writer(csv_file, dialect='excel')
csv_write.writerow(headers)
csv_write.writerows(rows)
csv_file.close()