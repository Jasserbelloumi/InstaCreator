import requests
import random
import uuid

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def notify(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
    except: pass

def inject_final_exploit():
    # استخدام بروكسيات SOCKS4 التي أثبتت كفاءتها
    proxy_list = [
        "socks4://192.252.214.20:15864",
        "socks4://192.252.208.70:14282",
        "socks4://72.195.34.58:4145"
    ]
    
    proxy = random.choice(proxy_list)
    proxies = {"http": proxy, "https": proxy}
    
    # الثغرة: استخدام App-ID الويب الرسمي مع ترويسات أندرويد
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "X-IG-App-ID": "936619743392459", # المعرف العالمي لإنستقرام
        "X-ASBD-ID": "129477",
        "X-Instagram-AJAX": "1",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://www.instagram.com/accounts/emailsignup/"
    }

    # الرابط الجديد لتجاوز الـ 404
    target_url = "https://www.instagram.com/api/v1/web/accounts/check_username/"

    payload = {
        "username": f"jasser.pro.{random.randint(1000, 9999)}",
    }

    try:
        notify(f"🛠️ محاولة اختراق الرابط الجديد عبر: {proxy}")
        
        # طلب الثغرة
        response = requests.post(target_url, headers=headers, data=payload, proxies=proxies, timeout=20)
        
        if response.status_code == 200:
            notify(f"🎯 اختراق ناجح! الثغرة تجاوزت الـ 404 والـ 429.\nالرد: {response.text}")
        elif response.status_code == 429:
            notify(f"⚠️ البروكسي {proxy} محظور مؤقتاً (429). جرب مرة أخرى.")
        else:
            notify(f"❌ استجابة غير متوقعة ({response.status_code}): {response.text[:100]}")

    except Exception as e:
        notify(f"⚠️ فشل الحقن: {str(e)}")

if __name__ == "__main__":
    inject_final_exploit()
