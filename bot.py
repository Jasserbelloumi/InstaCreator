import requests
import random
import time

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

# قائمة البروكسيات الذهبية التي حفظناها + إمكانية إضافة المزيد
PROXY_LIST = [
    "177.93.49.203:999",
    "103.172.42.105:1111",
    "192.252.214.20:15864",
    "192.252.208.70:14282",
    "193.233.254.7:1080"
]

def notify(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
    except: pass

def attempt_exploit():
    random.shuffle(PROXY_LIST) # تبديل الترتيب لضمان عدم تكرار الفشل
    
    headers = {
        "User-Agent": "Instagram 311.1.0.32.118 Android (30/11; 480dpi; 1080x2214; samsung; SM-G998B; o1q; exynos2100; en_US; 546937511)",
        "X-IG-App-ID": "936619743392459",
        "X-ASBD-ID": "129477",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
    }

    for proxy in PROXY_LIST:
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        print(f"Testing Proxy: {proxy}")
        
        try:
            # محاولة سريعة لفحص اليوزر (الثغرة)
            check_url = "https://www.instagram.com/api/v1/web/accounts/check_username/"
            response = requests.post(check_url, headers=headers, data={"username": f"jasser_test_{random.randint(100,999)}"}, proxies=proxies, timeout=10)
            
            if response.status_code == 200:
                notify(f"✅ تم كسر الحماية بنجاح باستخدام بروكسي شغال: {proxy}")
                return True
            else:
                print(f"Proxy {proxy} returned status {response.status_code}")
        except Exception:
            print(f"Proxy {proxy} failed (Timeout/Refused)")
            continue
            
    notify("⚠️ جميع البروكسيات الحالية معطلة. أحتاج لسحب قائمة جديدة.")
    return False

if __name__ == "__main__":
    attempt_exploit()
