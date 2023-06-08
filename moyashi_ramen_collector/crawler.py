

import time
import pandas as pd

import requests

from moyashi_ramen_collector import config


def crawl_shop_list(page_depth: int, request_interval: int = 3) -> None:
    """
    ラーメンデータベースの「二郎系」タグがついたラーメン店を探す
    """
    for n in range(1, page_depth):
        url = config.SHOT_LIST_URL_BASE.format(n)
        result = requests.get(url)
        c = result.content
        # ローカルディレクトリにクローリング結果をそのまま格納していく
        with open(config.SHOP_LIST_HTML_FILEPATH.format(n), 'w') as f:
            f.write(c.decode('UTF-8'))
            time.sleep(request_interval)


def crawl_shop_details(request_interval: int = 3) -> None:
    """
    ラーメンデータベースのラーメン店の個別ページをクローリングする
    """
    shop_list_df = pd.read_csv(config.SHOP_LIST_CSV_FILEPATH)
    print(shop_list_df.shape)
    for row in shop_list_df.itertuples():
        result = requests.get(row.url)
        c = result.content
        with open(config.SHOP_DETAILS_HTML_FILEPATH.format(row.name).replace("/", ""), 'w') as f:
            f.write(c.decode('UTF-8'))
            time.sleep(request_interval)
        print(f"crawling on page: {row.url} was finished!")
