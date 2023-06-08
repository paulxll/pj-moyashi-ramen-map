from bs4 import BeautifulSoup
import requests


def coordinate(address: str, dest_url: str = 'http://www.geocoding.jp/api/') -> tuple(str, str):
    """
    addressに住所を指定すると緯度経度を返す。

    >>> coordinate('東京都文京区本郷7-3-1')
    ['35.712056', '139.762775']
    """
    payload = {'q': address}
    html = requests.get(dest_url, params=payload)
    soup = BeautifulSoup(html.content, "html.parser")
    if not soup.find('lat'):
        print(f"Invalid address submitted. {address}")
        return ('0', '0')
    latitude = soup.find('lat').string
    longitude = soup.find('lng').string
    return (latitude, longitude)
