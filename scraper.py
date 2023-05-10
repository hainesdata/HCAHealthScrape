import pandas as pd
import requests

from bs4 import BeautifulSoup
from autoproxy import get_proxies


def get_page(url, proxy='None'):
    print(f'[REQUEST]: {url}')
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    if proxy == 'none':
        resp = requests.get(url, headers=hdr)
        return resp
    resp = requests.get(url, headers=hdr, proxies={'http': f'{proxy}', 'https': f'{proxy}'})
    print(f'[REQUEST]: {resp}')
    return resp


def get_names(proxy, field, offices, n, lat, lon, d):
    print('Gathering practitioner names...')
    url = f"https://www.hcahealthcare.co.uk/finder/search?sortType=relevance&search={field}&keywordId=2924&practice=\
    {offices}&lat={lat}&lon={lon}&distance={d}&limit={n}"
    resp = get_page(url, proxy)
    soup = BeautifulSoup(resp.text, "html.parser")
    u = []
    names = soup.select('div[class*="result-card__header-info-details-name"]')
    for i in names:
        u.append(i.get('href'))
    print('Done.')
    return u


def get_addresses(name, proxy):
    print('Gathering locations...')
    url = f'https://www.hcahealthcare.co.uk{name}'
    resp = get_page(url, proxy)
    soup = BeautifulSoup(resp.text, 'html.parser')
    u = []
    a = soup.select('p[class*="consultant-finder__address"]')
    for i in a:
        u.append(i)
    print('Done.')
    return u


def get_phone(practice, proxy):
    print('Gathering contact info...')
    url = f'https://www.hcahealthcare.co.uk/facilities/{practice}'
    resp = get_page(url, proxy)
    soup = BeautifulSoup(resp.text, 'html.parser')
    u = []
    p = soup.select('a[class*=["g-expanding-button__content-item"]')
    for i in p:
        u.append(i.get('href'))
    print('Done.')
    return u


def scrape(proxy_region, field, offices, n=100, lat='51.5072178', lon='-0.1275862', d=700):
    print('SCRAPE START----------------')
    proxy = get_proxies(proxy_region)
    names = get_names(proxy, field=field, offices=offices, n=n, lat=lat, lon=lon, d=d)
    info = []
    for name in names:
        a = get_addresses(name, proxy)
        p = get_phone(name, proxy)
        info.append([name, a, p])
    print('SCRAPE FINISH---------------')
    return info


o = "the-harley-street-clinic-3%2C\
the-lister-hospital%2C\
london-bridge-hospital%2C\
the-portland-hospital-for-women-and-children-1%2C\
the-princess-grace-hospital-1%2C\
the-wellington-hospital%2C\
the-wilmslow-hospital%2C\
the-christie-private-care%2C\
hca-uk-at-university-college-hospital%2C\
loc-leaders-in-oncology-care%2C\
golders-green-outpatients-and-diagnostics-centre%2C\
hca-chiswick-outpatients-and-diagnostics-centre%2C\
the-institute-of-sport-exercise-and-health-iseh%2C\
The-wellington-hospital-elstree-waterfront\
"

scrape('us', 'dermatology', o)
