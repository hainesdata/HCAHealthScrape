import requests
import os
from requests.exceptions import ProxyError

def disable_proxy():
    print(f'Disabling proxies...')
    os.system("networksetup -setwebproxystate Wi-Fi off")
    os.system("networksetup -setsecurewebproxystate Wi-Fi off")
    os.system("networksetup -setsocksfirewallproxystate Wi-Fi off")
    print('Done.')


# Get list of ten working proxies for webscraping
def get_proxies(region):
    disable_proxy()

    # Get proxies from proxyscrape
    url = 'https://google.com'
    proxies_url = f'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country={region}&ssl=all&anonymity=all'
    response = requests.get(proxies_url)
    proxies = response.text.split('\r\n')

    # Test proxies and return first one working
    for proxy in proxies:
        try:
            r = requests.get(url, proxies={'http': proxy, 'https': proxy}, timeout=5)
            print(r)
            check = u'\u2713'
            print(f'{check}\t Proxy {proxy} is working. Adding to OS...')
            return proxy
        except:
            check = u'\u2717'
            print(f'{check}\t Proxy {proxy} is not working')
    raise ProxyError('Proxy list exhausted, no working proxies found.')


def enable_proxy(region):
    # Replace "proxy_address" with the actual proxy address returned by your Python script
    proxy_address = f"{get_proxies(region)}"

    print('Enabling proxy...')

    # Split the proxy_address string into IP address and port number
    ip_address, port_number = proxy_address.split(':')

    # Set the HTTP and HTTPS proxy settings
    os.system("networksetup -setwebproxy Wi-Fi " + ip_address + " " + port_number)
    os.system("networksetup -setsecurewebproxy Wi-Fi " + ip_address + " " + port_number)

    # Set the SOCKS proxy settings
    os.system("networksetup -setsocksfirewallproxy Wi-Fi " + ip_address + " " + port_number)
    os.system("networksetup -setsocksfirewallproxystate Wi-Fi on")

    print('Done.')

enable_proxy('us')