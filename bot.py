import requests
import random
import time
import uuid

# بيانات التليجرام
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def notify(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
    except: pass

def inject_exploit():
    # استخدام البروكسيات التي حفظناها (تأكد أن أحدها شغال)
    proxies_to_test = ["177.93.49.203:999", "103.172.42.105:1111", "193.233.254.7:1080"]
    proxy = random.choice(proxies_to_test)
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}

    # توليد معرفات أجهزة وهمية (هذه هي الثغرة لتبدو كجهاز جديد تماماً)
    device_id = str(uuid.uuid4())
    uuid_id = str(uuid.uuid4())
    
    # ترويسات "الثغرة": محاكاة تطبيق الأندرويد لكسر حماية الويب
    headers = {
        "User-Agent": "Instagram 311.1.0.32.118 Android (30/11; 480dpi; 1080x2214; samsung; SM-G998B; o1q; exynos2100; en_US; 546937511)",
        "X-IG-App-ID": "1217981644879628", # ID تطبيق الأندرويد الأصلي
        "X-IG-Capabilities": "3brTvw==",
        "X-IG-Connection-Type": "WIFI",
        "X-Ads-Opt-Out": "0",
        "X-CM-Bandwidth-KBPS": str(random.randint(1000, 5000)),
        "X-IG-Device-ID": device_id,
        "Accept-Language": "en-US",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    # محاولة فحص اليوزر عبر الـ API الداخلي
    target_url = "https://i.instagram.com/api/v1/accounts/check_username/"
    payload = {
        "username": f"jasser_hero_{random.randint(100, 999)}",
        "_uuid": uuid_id,
        "device_id": device_id
    }

    try:
        notify(f"🛠️ جاري زرع الثغرة عبر البروكسي: {proxy}")
        response = requests.post(target_url, headers=headers, data=payload, proxies=proxies, timeout=15)
        
        # إذا كانت الاستجابة تحتوي على 'status': 'ok' فالثغرة تعمل!
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "ok":
                notify(f"🎯 اختراق ناجح! الثغرة تجاوزت الحماية.\nالرد: {response.text}")
            else:
                notify(f"⚠️ الثغرة تم اكتشافها من قبل نظام الحماية: {response.text}")
        else:
            notify(f"❌ فشل الاتصال بالخادم (Status: {response.status_code})")

    except Exception as e:
        notify(f"⚠️ خطأ أثناء زرع الثغرة: {str(e)}")

if __name__ == "__main__":
    inject_exploit()
