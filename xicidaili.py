import requests
import csv
from bs4 import BeautifulSoup

headers = {
    'Connection': 'keep-alive',
    # 模拟浏览器操作
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.142 Safari/537.36'
}

url = [
    'https://www.xicidaili.com/nn/',
    'https://www.xicidaili.com/nt/',
    'https://www.xicidaili.com/wn/',
    'https://www.xicidaili.com/wt/'
]

save_file = [
    'nn_csv.csv', 'nt_csv.csv', 'wn_csv.csv', 'wt_csv.csv'
]


def check_validity(type, ip, port):
    proxies = type + "://" + str(ip) + ':' + port
    try:
        requests.get('https://www.baidu.com/', proxies={type: proxies})
    except:
        return False
    else:
        return True


def spider (url, file_path, headers):
    r = requests.get(url, headers = headers)

    soup = BeautifulSoup(r.text, 'lxml')

    table = soup.find('table', id='ip_list')
    # 提取页面表头
    ths = table.find_all('th', limit=6)
    headers = []
    for n in ths:
        headers.append(n.string)
    # 去除 国家 元素
    headers.remove('国家')
    headers.append('有效性')

    # 提取页面表格值
    rows = []
    for idx, tr in enumerate(table.find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td', limit=6)
            row = []
            for num, n in enumerate(tds):
                if num != 0:
                    if num == 3:
                        row.append(n.find('a'))
                    else:
                        row.append(n.string)
            if check_validity(row[4], row[0], row[1]):
                row.append('有效')
            else:
                row.append('无效')
            rows.append(row)
    csv_file = open(file_path, 'a', newline='')
    csv_write = csv.writer(csv_file, dialect='excel')
    csv_write.writerow(headers)
    csv_write.writerows(rows)
    csv_file.close()
    return


for i in range(len(url)):
    spider(url[i], save_file[i], headers)


