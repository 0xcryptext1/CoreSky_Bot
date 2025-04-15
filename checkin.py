import json
import time
import requests
from eth_account import Account
from eth_account.messages import encode_defunct
import random
import os


def load_proxies():
    proxies = []
    try:
        if os.path.exists('proxy.txt'):
            with open('proxy.txt', 'r') as f:
                for line in f:
                    if line.strip():
                        proxies.append(line.strip())
            print(f"{len(proxies)} adet proxy yüklendi.")
        else:
            print("proxy.txt dosyası bulunamadı.")
    except Exception as e:
        print(f"Proxy dosyası okuma hatası: {e}")
    return proxies

def get_proxy(index, proxies, use_proxy):
    """İşlem için proxy bilgisini döndürür."""
    if not use_proxy or not proxies:
        return None
    
    if index % 4 == 3:  
        return None
    
    proxy_index = (index % len(proxies))
    proxy = proxies[proxy_index]
    ip, port, username, password = proxy.split(':')
    
    return {
        'http': f'http://{username}:{password}@{ip}:{port}',
        'https': f'http://{username}:{password}@{ip}:{port}'
    }

def sign_message(private_key: str, message: str):
    """Belirtilen özel anahtar ile mesajı Ethereum formatında imzalar."""
    encoded_message = encode_defunct(text=message)
    signed_message = Account.sign_message(encoded_message, private_key=private_key)
    return signed_message.signature.hex()


def login(address, signature, proxies=None):
    url = "https://www.coresky.com/api/user/login"
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://www.coresky.com",
        "referer": "https://www.coresky.com/tasks-rewards",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    
    signature = signature if signature.startswith("0x") else "0x" + signature
    
    data = {
        "address": address,
        "signature": signature,
        "refCode": "",
        "projectId": ""
    }

    response = requests.post(url, headers=headers, json=data, proxies=proxies)
    return response.json()


def sign_taskwall(token, proxies=None):
    url = "https://www.coresky.com/api/taskwall/meme/sign"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "tr-TR,tr;q=0.9",
        "content-length": "0",
        "origin": "https://www.coresky.com",
        "referer": "https://www.coresky.com/tasks-rewards",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "token": token
    }

    response = requests.post(url, headers=headers, proxies=proxies)
    return response.json()


def get_score(token, address, proxies=None):
    url = "https://www.coresky.com/api/user/score/detail"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "tr-TR,tr;q=0.9",
        "content-type": "application/json",
        "origin": "https://www.coresky.com",
        "referer": "https://www.coresky.com/tasks-rewards",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "token": token
    }
    
    data = {
        "page": 1,
        "limit": 10,
        "address": address
    }

    response = requests.post(url, headers=headers, json=data, proxies=proxies)
    return response.json()


LOGIN_MESSAGE = "Welcome to CoreSky!\n\nClick to sign in and accept the CoreSky Terms of Service.\n\nThis request will not trigger a blockchain transaction or cost any gas fees.\n\nYour authentication status will reset after 24 hours.\n\nWallet address:\n\n{address}"


print("CoreSky Login ve Checkin İşlemi")
print("=" * 50)

def get_user_settings():
    print("\nProgram Ayarları:")
    print("-" * 30)
    
    use_proxy = input("Proxy kullanmak istiyor musunuz? (E/H): ").strip().lower() == 'e'
    
    min_wait = 30  
    max_wait = 45  
    
    try:
        min_wait = int(input("Minimum bekleme süresi (saniye): "))
        max_wait = int(input("Maksimum bekleme süresi (saniye): "))
        
        if min_wait < 0 or max_wait < min_wait:
            print("Geçersiz değerler, varsayılan değerler kullanılacak (30-45 saniye)")
            min_wait = 30
            max_wait = 45
    except ValueError:
        print("Geçersiz değerler, varsayılan değerler kullanılacak (30-45 saniye)")
        min_wait = 30
        max_wait = 45
    
    return use_proxy, min_wait, max_wait


proxies = load_proxies()

use_proxy, min_wait, max_wait = get_user_settings()

with open('wallets.txt', 'r') as f:
    wallets = f.readlines()

try:
    with open('position.txt', 'r') as pos_file:
        position = int(pos_file.read().strip())
except FileNotFoundError:
    position = 0  

print(f"İşlem yapılacak {len(wallets)} cüzdan bulundu.\n")
print(f"Bekleme süresi: {min_wait}-{max_wait} saniye")
print(f"Proxy kullanımı: {'Aktif' if use_proxy else 'Kapalı'}")
print("-" * 50)

for i in range(position, len(wallets)):
    wallet = wallets[i]
    try:
        address, private_key = wallet.strip().split(',')
        print(f"İşlem: {i + 1}/{len(wallets)} - {address}")
        
        proxies_config = get_proxy(i, proxies, use_proxy)
        proxy_info = "Proxy kullanılmıyor" if proxies_config is None else f"Proxy: {list(proxies_config.values())[0]}"
        print(f"✓ {proxy_info}")
        
        message = LOGIN_MESSAGE.format(address=address)
        signature = sign_message(private_key, message)
        print("✓ İmza oluşturuldu")
        
        login_response = login(address, signature, proxies_config)
        
        if login_response.get("code") == 200:
            print("✓ Giriş başarılı")
            
            token = None
            if "data" in login_response and login_response["data"] is not None:
                token = login_response["data"].get("token")
            elif "debug" in login_response and login_response["debug"] is not None:
                token = login_response["debug"].get("token")  
            
            if token:
                taskwall_response = sign_taskwall(token, proxies_config)
                
                if taskwall_response.get("code") == 200:
                    print("✓ imzalama başarılı")
                else:
                    print(f"✗ İmzalama hatası: {taskwall_response.get('message', 'Bilinmeyen hata')}")
                
                score_response = get_score(token, address, proxies_config)
                if score_response.get("code") == 200:
                    score = score_response.get("debug", {}).get("score", "Puan bulunamadı")
                    print(f"✓ Güncel puan: {score}")
                else:
                    print(f"✗ Puan alma hatası: {score_response.get('message', 'Bilinmeyen hata')}")
            else:
                print("✗ Token bulunamadı")
        else:
            print(f"✗ Giriş hatası: {login_response.get('message', 'Bilinmeyen hata')}")
        
        print("-" * 50)
        
        with open('position.txt', 'w') as pos_file:
            pos_file.write(str(i + 1))
        
        wait_time = random.randint(min_wait, max_wait)
        print(f"Sonraki işlem için {wait_time} saniye bekleniyor...")
        time.sleep(wait_time)
        
    except Exception as e:
        print(f"✗ Hata: {str(e)}")
        print("-" * 50)
        continue

with open('position.txt', 'w') as pos_file:
    pos_file.write("0")

print("Tüm işlemler tamamlandı!")