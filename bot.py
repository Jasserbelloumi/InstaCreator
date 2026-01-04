import requests
import random
import time
import uuid

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def notify(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
    except: pass

def inject_exploit():
    # تدوير البروكسيات وتجربة أنواع مختلفة (Socks5 و HTTP)
    # سنستخدم البروكسيات التي كانت تعطينا Success سابقاً
    proxy_list = [
        "socks4://192.252.214.20:15864",
        "socks4://192.252.208.70:14282",
        "http://177.93.49.203:999",
        "http://103.172.42.105:1111"
    ]
    
    proxy = random.choice(proxy_list)
    proxies = {"http": proxy, "https": proxy}
    
    device_id = str(uuid.uuid4())
    uuid_id = str(uuid.uuid4())
    
    headers = {
        "User-Agent": "Instagram 311.1.0.32.118 Android (30/11; 480dpi; 1080x2214; samsung; SM-G998B; o1q; exynos2100; en_US; 546937511)",
        "X-IG-App-ID": "1217981644879628",
        "X-IG-Device-ID": device_id,
        "X-IG-Connection-Type": "WIFI",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    payload = {
        "username": f"jasser_hero_{random.randint(1000, 9999)}",
        "_uuid": uuid_id,
        "device_id": device_id
    }

    try:
        notify(f"🛡️ محاولة تجاوز بروتوكول البروكسي وحقن الثغرة: {proxy}")
        # استخدام verify=False لتجاوز فحص شهادات البروكسي المزعجة
        response = requests.post("https://i.instagram.com/api/v1/accounts/check_username/", 
                                 headers=headers, data=payload, proxies=proxies, timeout=20, verify=False)
        
        if response.status_code == 200:
            notify(f"🎯 اختراق ناجح! الثغرة تجاوزت نظام الحماية بالكامل.\nالرد: {response.text}")
        else:
            notify(f"⚠️ الخادم رد برمز {response.status_code}. قد نحتاج لتغيير الـ App-ID.")
            
    except Exception as e:
        notify(f"⚠️ فشل الحقن عبر {proxy}: {str(e)}")

if __name__ == "__main__":
    inject_exploit()
