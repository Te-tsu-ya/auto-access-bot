import time
import threading
import requests

def auto_refresh(url, interval=3, max_refreshes=15):
    for i in range(max_refreshes):
        try:
            res = requests.get(url)
            print(f"{url} にアクセス {i+1}/{max_refreshes} - ステータス: {res.status_code}")
        except Exception as e:
            print(f"{url} アクセス失敗: {e}")
        time.sleep(interval)

def run_auto_refresh(urls, interval=3, max_refreshes=15):
    threads = []
    for url in urls:
        t = threading.Thread(target=auto_refresh, args=(url, interval, max_refreshes))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    target_urls = [
        "https://murakami.mypl.net/shop/00000377236/",
        "https://murakami.mypl.net/shop/00000377236/news",
        "https://murakami.mypl.net/shop/00000377236/news?d=2886516",
        "https://murakami.mypl.net/shop/00000377236/news?d=2907185",
        "https://murakami.mypl.net/shop/00000377236/news?d=2911222",
        "https://murakami.mypl.net/shop/00000377236/news?d=2889022",
        "https://murakami.mypl.net/shop/00000377236/news?d=2926707",
        "https://murakami.mypl.net/shop/00000377236/news?d=2926707",
        "https://murakami.mypl.net/shop/00000377236/news?d=2926707",
        "https://murakami.mypl.net/shop/00000377236/news?d=2926707"
    ]
    run_auto_refresh(target_urls, interval=3, max_refreshes=15)

