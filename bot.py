import requests
import random
import urllib3

# تعطيل تحذيرات SSL تماماً لجعل المحاكاة سريعة ونظيفة
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def notify(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
    except: pass

def inject_simulation():
    # قائمة البروكسيات Socks4 التي أرسلتها لي
    proxy_list = [
        "socks4://192.252.214.20:15864",
        "socks4://192.252.208.70:14282",
        "socks4://72.195.34.58:4145"
    ]
    
    proxy = random.choice(proxy_list)
    proxies = {"http": proxy, "https": proxy}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-IG-App-ID": "936619743392459",
        "X-Instagram-AJAX": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
    }

    target_url = "https://www.instagram.com/api/v1/web/accounts/check_username/"
    payload = {"username": f"user_test_{random.randint(1000, 9999)}"}

    try:
        notify(f"🛠️ محاكاة الحقن عبر {proxy} (تجاوز SSL فعال)")
        
        # السر هنا في verify=False لتخطي الخطأ الذي ظهر لك
        response = requests.post(target_url, headers=headers, data=payload, proxies=proxies, timeout=20, verify=False)
        
        if response.status_code == 200:
            notify(f"🎯 مذهل! المحاكاة نجحت والرد وصل:\n{response.text}")
        else:
            notify(f"⚠️ الخادم رد بـ {response.status_code}. الـ IP قد يحتاج لتغيير.")

    except Exception as e:
        notify(f"⚠️ فشل في المحاكاة: {str(e)}")

if __name__ == "__main__":
    inject_simulation()
