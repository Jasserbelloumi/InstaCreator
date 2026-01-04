import requests
import random
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# بياناتك الخاصة
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

# البروكسيات الذهبية التي زودتني بها
PROXIES = [
    "177.93.49.203:999",
    "103.172.42.105:1111",
    "192.252.214.20:15864",
    "192.252.208.70:14282"
]

def send_telegram(message, photo=None):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message}, timeout=10)
        if photo and os.path.exists(photo):
            url_photo = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
            with open(photo, 'rb') as f:
                requests.post(url_photo, data={"chat_id": CHAT_ID}, files={"photo": f}, timeout=10)
    except Exception as e:
        print(f"Telegram Error: {e}")

def main():
    # إرسال إشعار البدء فوراً للتأكد من الاتصال
    send_telegram("🚀 بدأت عملية كسر الحماية الآن... جاري تجربة البروكسيات.")

    for proxy in PROXIES:
        send_telegram(f"⏳ جاري التجربة باستخدام البروكسي: {proxy}")
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument(f"--proxy-server=http://{proxy}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1")

        driver = webdriver.Chrome(options=options)
        
        try:
            driver.get("https://www.instagram.com/accounts/emailsignup/")
            time.sleep(15)
            
            driver.save_screenshot("check.png")
            
            if "429" in driver.page_source:
                send_telegram(f"❌ البروكسي {proxy} محظور (429).", "check.png")
                driver.quit()
                continue
            
            # إذا نجح في الوصول للواجهة
            send_telegram(f"🔥 نجاح! البروكسي {proxy} كسر الحماية وفتح الصفحة!", "check.png")
            # هنا يمكنك إضافة كود الملء التلقائي
            break
            
        except Exception as e:
            send_telegram(f"⚠️ خطأ مع البروكسي {proxy}: {str(e)}")
            driver.quit()
    
    send_telegram("🏁 انتهت جميع المحاولات.")

if __name__ == "__main__":
    main()
