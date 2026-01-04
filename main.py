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



import time
import threading
import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag


# ===== 設定 =====
BASE_URLS = [
    "https://murakami.mypl.net/shop/00000377236/",
    "https://www.itec1999.com/",
]

MIN_INTERVAL = 10
MAX_INTERVAL = 30
MAX_REFRESHES = 1

MAX_DISCOVER_PAGES = 200   # ★ 無限ループ防止（安全装置）
# =================


def collect_urls_from_page(page_url, base_url):
    """1ページから、BASEで始まるURLを集める"""
    urls = []
    try:
        res = requests.get(page_url, timeout=10)
        if res.status_code != 200:
            return urls

        soup = BeautifulSoup(res.text, "html.parser")
        for a in soup.select("a[href]"):
            href = a.get("href")
            if not href:
                continue

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


if __name__ == "__main__":
    # === URL探索フェーズ ===
    target_urls = []

    # まずBASEを追加
    for base in BASE_URLS:
        target_urls.append(base)

    target_urls = list(dict.fromkeys(target_urls))

    index = 0
    while index < len(target_urls) and index < MAX_DISCOVER_PAGES:
        current_url = target_urls[index]

        # どのBASEに属するか判定
        base_for_url = None
        for base in BASE_URLS:
            if current_url.startswith(base):
                base_for_url = base
                break

        if base_for_url:
            new_urls = collect_urls_from_page(current_url, base_for_url)
            before = len(target_urls)
            target_urls.extend(new_urls)
            target_urls = list(dict.fromkeys(target_urls))
            after = len(target_urls)

            if after > before:
                print(f"URL追加: {after - before} 件（合計 {after}）")

        index += 1

    print("\n=== 探索完了（重複なしURL一覧）===")
    for u in target_urls:
        print(u)

    # === アクセスフェーズ ===
    run_auto_refresh(
        target_urls,
        MIN_INTERVAL,
        MAX_INTERVAL,
        MAX_REFRESHES
    )
