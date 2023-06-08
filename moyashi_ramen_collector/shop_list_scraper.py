import os
import re
from typing import Union
from bs4 import BeautifulSoup, NavigableString, Tag

import pandas as pd

from moyashi_ramen_collector import config


def extract_shops(div: Union[Tag, NavigableString, None]) -> pd.DataFrame:
    if isinstance(div, NavigableString):
        raise Exception("invalid HTML format.")
    elif div is None:
        raise Exception("invalid HTML format.")
    else:
        # スクレイピング結果をpandas dataframeに格納していく
        result_dic: dict = dict()
        for ind, s in enumerate(div.find_all('li', {'class': 'border-box'})):
            print(f"{ind} of {len(div.find_all('li', {'class': 'border-box'}))} shop scraping has started...")
            result_dic[ind] = dict()
            result_dic[ind]['name'] = s.find('div', {'class': 'name'}).find('h4').text
            result_dic[ind]['pref'] = s.find('div', {'class': 'area'}).find('a').text
            result_dic[ind]['review_score'] = s.find('div', {'class': 'point-val'}).text
            result_dic[ind]['review_num'] = s.find('div', {'class': 'val'}).text
            result_dic[ind]['url'] = 'https://ramendb.supleks.jp' + s.find('a', {'class': 'bglink'}).get('href')
        return pd.DataFrame.from_dict(result_dic, orient='index')


def scrape_shop_list() -> None:
    # スクレイピング対象のファイルリスト
    files = sorted([config.SHOP_LIST_HTML_DIR + x for x in os.listdir(config.SHOP_LIST_HTML_DIR) if re.search('html$', x)])
    result_df = pd.DataFrame()
    for file in files:
        print(f'{file} scraping has started...')
        with open(file, 'r') as f:
            soup = BeautifulSoup(f.read(), 'lxml')

        div = soup.find('div', {'class': 'wrap'})
        shop_df = extract_shops(div)
        result_df = pd.concat([result_df, shop_df])
    # 何故か重複が発生するので落とす。TODO: 要調査
    result_df = result_df.drop_duplicates()
    result_df.to_csv("data/shop_list/result.csv", index=False)
