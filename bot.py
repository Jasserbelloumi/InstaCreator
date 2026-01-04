import requests
import random
import time

# بيانات التليجرام
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def notify(msg):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})

def exploit_signup():
    # البروكسي الذي نجح معك سابقاً
    proxy = "177.93.49.203:999"
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}

    # هذه هي "الثغرة": محاكاة ترويسات تطبيق إنستقرام الرسمي تماماً
    headers = {
        "User-Agent": "Instagram 311.1.0.32.118 Android (30/11; 480dpi; 1080x2214; samsung; SM-G998B; o1q; exynos2100; en_US; 546937511)",
        "X-IG-App-ID": "936619743392459", # ID تطبيق الويب الرسمي
        "X-ASBD-ID": "129477",
        "X-IG-WWW-Claim": "0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
    }

    # بيانات الحساب الجديد
    user_id = random.randint(100, 999)
    data = {
        "email": f"jasser.pro{user_id}@1secmail.com",
        "first_name": "Jasser Pro",
        "username": f"jasser_exploit_{user_id}",
        "opt_into_hashtags": "false",
    }

    try:
        # محاولة إرسال طلب "فحص اليوزر" أولاً (لخداع النظام)
        check_url = "https://www.instagram.com/api/v1/web/accounts/check_username/"
        res = requests.post(check_url, headers=headers, data={"username": data["username"]}, proxies=proxies, timeout=15)
        
        if res.status_code == 200:
            notify(f"🎯 الثغرة نجحت في تخطي الحظر! اليوزر متاح: {data['username']}")
            # هنا ننتقل لخطوة التسجيل الفعلي
        else:
            notify(f"❌ الموقع كشف الطلب (Status: {res.status_code}). الـ IP لا يزال مراقباً.")
            
    except Exception as e:
        notify(f"⚠️ خطأ في الاتصال بالثغرة: {str(e)}")

if __name__ == "__main__":
    exploit_signup()
