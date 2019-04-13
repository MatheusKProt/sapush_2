from urllib.request import Request, urlopen

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def headers():
    return {
        "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
        "Accept": '*/*',
        "Host": 'sapu.ucpel.edu.br',
        "Accept-Language": 'pt-br',
        "Accept-Encoding": 'br, gzip, deflate',
        "Origin": 'https://sapu.ucpel.edu.br',
        'Connection': 'keep-alive',
        'User-Agent': str(UserAgent().random),
        'X-Requested-With': 'XMLHttpRequest'
    }


def proxies():
    proxies_ = []
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', UserAgent().random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    for row in proxies_table.tbody.find_all('tr'):
        proxies_.append({
            'ip': row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
        })

    while proxies_:
        proxy = {
            "https": "https://{}:{}".format(proxies_[0]['ip'], proxies_[0]['port']),
        }
        try:
            print(requests.get('https://sapu.ucpel.edu.br/noticias', proxies=proxy, headers=headers(), timeout=5))
        except:
            print('Erro: ', proxy)
            proxies_.pop(0)
        else:
            return proxy
