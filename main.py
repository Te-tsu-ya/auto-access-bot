#import time
#import threading
#import requests
#
#def auto_refresh(url, interval=3, max_refreshes=15):
#    for i in range(max_refreshes):
#        try:
#            res = requests.get(url)
#            print(f"{url} にアクセス {i+1}/{max_refreshes} - ステータス: {res.status_code}")
#        except Exception as e:
#            print(f"{url} アクセス失敗: {e}")
#        time.sleep(interval)
#
#def run_auto_refresh(urls, interval=3, max_refreshes=15):
#    threads = []
#    for url in urls:
#        t = threading.Thread(target=auto_refresh, args=(url, interval, max_refreshes))
#        t.start()
#        threads.append(t)
#
#    for t in threads:
#        t.join()
#
#if __name__ == "__main__":
#    target_urls = [
#        "https://murakami.mypl.net/shop/00000377236/",
#        "https://murakami.mypl.net/shop/00000377236/news",
#        "https://murakami.mypl.net/shop/00000377236/news?d=2886516",
#        "https://murakami.mypl.net/shop/00000377236/news?d=2907185",
#        "https://murakami.mypl.net/shop/00000377236/news?d=2911222",
#        "https://murakami.mypl.net/shop/00000377236/news?d=2889022",
#        "https://murakami.mypl.net/shop/00000377236/news?d=2926707",
#        "https://murakami.mypl.net/shop/00000377236/news?d=2926707",
#        "https://murakami.mypl.net/shop/00000377236/news?d=2926707",
#        "https://murakami.mypl.net/shop/00000377236/news?d=2926707",
#        "https://www.itec1999.com/",
#        "https://www.itec1999.com/company/",
#        "https://www.itec1999.com/business/",
#        "https://www.itec1999.com/news/",
#        "https://www.itec1999.com/news/245/",
#        "https://www.itec1999.com/news/243/",
#        "https://www.itec1999.com/news/240/",
#        "https://www.itec1999.com/news/240/",
#        "https://www.itec1999.com/news/238/",
#        "https://www.itec1999.com/recruit/merit/",
#        "https://www.itec1999.com/recruit/jobs/",
#        "https://www.itec1999.com/recruit/environment/",
#        "https://www.itec1999.com/recruit/requirements/",
#        "https://www.itec1999.com/recruit/"
#    ]
#    run_auto_refresh(target_urls, interval=3, max_refreshes=15)


# import time
# import threading
# import requests
# import random
# from urllib.parse import urljoin, urldefrag
# from html.parser import HTMLParser


# # ===== 設定 =====
# BASE_URLS = [
#     "https://murakami.mypl.net/shop/00000377236/",
#     "https://www.itec1999.com/",
# ]

# MIN_INTERVAL = 10
# MAX_INTERVAL = 30
# MAX_REFRESHES = 1

# MAX_DISCOVER_PAGES = 200   # 無限ループ防止
# # =================


# class LinkExtractor(HTMLParser):
#     """HTMLからaタグのhrefだけを抜き出す（標準ライブラリのみ）"""
#     def __init__(self):
#         super().__init__()
#         self.hrefs = []

#     def handle_starttag(self, tag, attrs):
#         if tag.lower() != "a":
#             return
#         for k, v in attrs:
#             if k.lower() == "href" and v:
#                 self.hrefs.append(v)


# def collect_urls_from_page(page_url, base_url):
#     """1ページから、BASEで始まるURLを集める（bs4不要）"""
#     urls = []
#     try:
#         res = requests.get(page_url, timeout=10)
#         if res.status_code != 200:
#             return urls

#         parser = LinkExtractor()
#         parser.feed(res.text)

#         for href in parser.hrefs:
#             full_url = urljoin(page_url, href)
#             full_url, _ = urldefrag(full_url)

#             if full_url.startswith(base_url):
#                 urls.append(full_url)

#     except Exception as e:
#         print(f"{page_url} のURL取得失敗: {e}")

#     return urls


# def auto_refresh(url, min_interval, max_interval, max_refreshes):
#     for i in range(max_refreshes):
#         try:
#             res = requests.get(url, timeout=10)
#             print(f"{url} にアクセス {i+1}/{max_refreshes} - {res.status_code}")
#         except Exception as e:
#             print(f"{url} アクセス失敗: {e}")

#         wait = random.uniform(min_interval, max_interval)
#         time.sleep(wait)


# def run_auto_refresh(urls, min_interval, max_interval, max_refreshes):
#     threads = []
#     for url in urls:
#         t = threading.Thread(
#             target=auto_refresh,
#             args=(url, min_interval, max_interval, max_refreshes)
#         )
#         t.start()
#         threads.append(t)

#     for t in threads:
#         t.join()


# if __name__ == "__main__":
#     # === URL探索フェーズ ===
#     target_urls = []

#     # まずBASEを追加
#     for base in BASE_URLS:
#         target_urls.append(base)

#     # 重複削除（順序維持）
#     target_urls = list(dict.fromkeys(target_urls))

#     index = 0
#     while index < len(target_urls) and index < MAX_DISCOVER_PAGES:
#         current_url = target_urls[index]

#         # どのBASEに属するか判定
#         base_for_url = None
#         for base in BASE_URLS:
#             if current_url.startswith(base):
#                 base_for_url = base
#                 break

#         if base_for_url:
#             new_urls = collect_urls_from_page(current_url, base_for_url)
#             before = len(target_urls)
#             target_urls.extend(new_urls)
#             target_urls = list(dict.fromkeys(target_urls))
#             after = len(target_urls)

#             if after > before:
#                 print(f"URL追加: {after - before} 件（合計 {after}）")

#         index += 1

#     print("\n=== 探索完了（重複なしURL一覧）===")
#     for u in target_urls:
#         print(u)

#     # === アクセスフェーズ ===
#     run_auto_refresh(
#         target_urls,
#         MIN_INTERVAL,
#         MAX_INTERVAL,
#         MAX_REFRESHES
#     )




import time
import threading
import requests
import random
from urllib.parse import urljoin, urldefrag
from html.parser import HTMLParser


# ===== 設定 =====
BASE_CONFIGS = [
    {
        "base_url": "https://murakami.mypl.net/shop/00000377236/",
        "max_discover_pages": 200,
    },
    {
        "base_url": "https://murakami.mypl.net/shop/00000372475/",
        "max_discover_pages": 100,
    },
    {
        "base_url": "https://www.itec1999.com/",
        "max_discover_pages": 100,
    },
]

MIN_INTERVAL = 10
MAX_INTERVAL = 30
MAX_REFRESHES = 1
# =================


class LinkExtractor(HTMLParser):
    """HTMLからaタグのhrefだけを抜き出す（標準ライブラリのみ）"""
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        for k, v in attrs:
            if k.lower() == "href" and v:
                self.hrefs.append(v)


def collect_urls_from_page(page_url, base_url):
    """1ページから、base_urlで始まるURLを集める（bs4不要）"""
    urls = []
    try:
        res = requests.get(page_url, timeout=10)
        if res.status_code != 200:
            return urls

        parser = LinkExtractor()
        parser.feed(res.text)

        for href in parser.hrefs:
            full_url = urljoin(page_url, href)
            full_url, _ = urldefrag(full_url)

            if full_url.startswith(base_url):
                urls.append(full_url)

    except Exception as e:
        print(f"{page_url} のURL取得失敗: {e}")

    return urls


def auto_refresh(url, min_interval, max_interval, max_refreshes):
    for i in range(max_refreshes):
        try:
            res = requests.get(url, timeout=10)
            print(f"{url} にアクセス {i+1}/{max_refreshes} - {res.status_code}")
        except Exception as e:
            print(f"{url} アクセス失敗: {e}")

        wait = random.uniform(min_interval, max_interval)
        time.sleep(wait)


def run_auto_refresh(urls, min_interval, max_interval, max_refreshes):
    threads = []
    for url in urls:
        t = threading.Thread(
            target=auto_refresh,
            args=(url, min_interval, max_interval, max_refreshes)
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def discover_urls_for_base(base_url, max_discover_pages):
    """
    base_url配下のURLを探索する（baseごとに上限を適用）
    max_discover_pages は「探索対象URLの最大数」
    """
    target_urls = [base_url]
    target_urls = list(dict.fromkeys(target_urls))

    index = 0
    while index < len(target_urls) and index < max_discover_pages:
        current_url = target_urls[index]

        new_urls = collect_urls_from_page(current_url, base_url)
        before = len(target_urls)
        target_urls.extend(new_urls)
        target_urls = list(dict.fromkeys(target_urls))
        after = len(target_urls)

        if after > before:
            print(f"[{base_url}] URL追加: {after - before} 件（合計 {after} / 上限 {max_discover_pages}）")

        index += 1

    # 上限を超えて増えてしまった分があれば切る（安全）
    target_urls = target_urls[:max_discover_pages]
    return target_urls


if __name__ == "__main__":
    all_target_urls = []

    # === BASEごとに探索 ===
    for conf in BASE_CONFIGS:
        base_url = conf["base_url"]
        max_pages = conf["max_discover_pages"]

        print(f"\n=== 探索開始: {base_url}（最大 {max_pages}）===")
        urls = discover_urls_for_base(base_url, max_pages)

        print(f"\n=== 探索完了: {base_url}（重複なし {len(urls)} 件）===")
        for u in urls:
            print(u)

        all_target_urls.extend(urls)

    # 全体でも重複排除
    all_target_urls = list(dict.fromkeys(all_target_urls))

    # === アクセスフェーズ ===
    print(f"\n=== アクセス開始（合計 {len(all_target_urls)} URL）===")
    run_auto_refresh(
        all_target_urls,
        MIN_INTERVAL,
        MAX_INTERVAL,
        MAX_REFRESHES
    )
