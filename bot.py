import time
import random
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# بيانات التليجرام
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

# البروكسيات الذهبية التي قدمتها
PROXIES = [
    "177.93.49.203:999", "103.172.42.105:1111", 
    "192.252.214.20:15864", "192.252.208.70:14282"
]

def notify(msg, img=None):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
        if img and os.path.exists(img):
            with open(img, 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID}, files={'photo': f})
    except: pass

def run_pro_bot():
    proxy = random.choice(PROXIES)
    notify(f"🚀 محاولة كسر الحماية العميقة باستخدام البروكسي: {proxy}")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f'--proxy-server={proxy}')
    
    # حذف أي أثر للـ WebDriver
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # بصمة iPhone متقدمة
    ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    options.add_argument(f"user-agent={ua}")

    driver = webdriver.Chrome(options=options)
    
    # أقوى كود لإخفاء هوية البوت (تعديل الـ Runtime)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', {get: () => ['ar-SA', 'ar', 'en-US']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        """
    })

    try:
        # الدخول برابط مباشر لتجنب الـ Redirect الذي يكشف البوت
        driver.get("https://www.instagram.com/accounts/emailsignup/")
        
        # انتظار طويل ومحاكاة تفاعل بشري عشوائي قبل الفحص
        time.sleep(random.randint(15, 25))
        
        driver.save_screenshot("view.png")
        
        if "429" in driver.page_source or "ERR_CONNECTION_RESET" in driver.page_source:
            notify("❌ لا يزال النظام يكتشف "بصمة الخادم". سأحاول تغيير إستراتيجية الحقن.", "view.png")
            return

        # إذا نجح، ابدأ ملء البيانات
        wait = WebDriverWait(driver, 20)
        # (هنا نضع أكواد الملء التي كتبناها سابقاً)
        notify("🔥 مذهل! تم فتح الواجهة بنجاح وتجاوز كاشف البوتات!", "view.png")

    except Exception as e:
        driver.save_screenshot("fail.png")
        notify(f"⚠️ فشل كسر الحماية: {str(e)}", "fail.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_pro_bot()
