import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def notify(msg, img=None):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
        if img:
            with open(img, 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID}, files={'photo': f})
    except: pass

def start_attack():
    # استخدام البروكسي الذي نجح معك
    proxy = "177.93.49.203:999"
    notify(f"🛡️ محاولة تجاوز الحظر الداخلي باستخدام البروكسي الناجح: {proxy}")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument(f'--proxy-server=http://{proxy}')
    
    # إعدادات التخفي المتقدمة
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # بصمة iPhone 15 Pro Max (الأحدث والأكثر ثقة)
    ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
    options.add_argument(f"user-agent={ua}")

    driver = webdriver.Chrome(options=options)

    # كود حقن لتعطيل كاشفات السيلينيوم تماماً
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', {get: () => ['ar-SA', 'en-US']});
            Object.defineProperty(navigator, 'vendor', {get: () => 'Apple Computer, Inc.'});
        """
    })

    try:
        # الدخول ببطء لمحاكاة سرعة الإنسان
        driver.get("https://www.instagram.com/accounts/emailsignup/")
        time.sleep(random.randint(10, 20)) 
        
        # محاكاة حركة عشوائية (Scroll) قبل أي فعل
        driver.execute_script("window.scrollTo(0, 200);")
        time.sleep(2)
        
        driver.save_screenshot("bypass_result.png")
        
        if "429" in driver.page_source or "blocked" in driver.page_source.lower():
            notify("❌ البروكسي فتح الصفحة لكن إنستا كشف "بصمة البوت". أحتاج لتغيير إستراتيجية الحقن.", "bypass_result.png")
        else:
            notify("🔥 نجاح باهر! تم فتح الواجهة وتجاوز الحظر تماماً!", "bypass_result.png")
            # هنا يبدأ كود الملء التلقائي...

    except Exception as e:
        notify(f"⚠️ خطأ غير متوقع: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    start_attack()
