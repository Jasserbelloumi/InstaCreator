import requests, random, time, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def notify(msg, img=None):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
        if img and os.path.exists(img):
            with open(img, 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID}, files={'photo': f})
    except: pass

def get_free_proxies():
    """جلب قائمة بروكسيات مجانية لكسر حظر IP"""
    try:
        response = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
        return response.text.split('\r\n')
    except: return []

def run_broken_shield():
    notify("⚔️ محاولة كسر الحماية باستخدام نظام البروكسي المتغير...")
    
    proxies = get_free_proxies()
    random.shuffle(proxies)
    
    for proxy in proxies[:10]: # تجربة أفضل 10 بروكسيات
        if not proxy: continue
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument(f'--proxy-server={proxy}')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")
        
        # بصمة آيفون متغيرة
        ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        options.add_argument(f"user-agent={ua}")

        try:
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(30)
            
            print(f"Trying Proxy: {proxy}")
            driver.get("https://www.instagram.com/accounts/emailsignup/")
            time.sleep(10)
            
            driver.save_screenshot("bypass_attempt.png")
            
            if "429" not in driver.page_source and "Instagram" in driver.title:
                notify(f"🔥 تم كسر الحماية باستخدام البروكسي: {proxy}", "bypass_attempt.png")
                # هنا يكمل السكربت عملية التسجيل...
                break
            else:
                print("Still blocked or proxy slow, trying next...")
                driver.quit()
        except:
            print("Proxy connection failed, retrying...")
            continue

    notify("🏁 انتهت محاولات كسر الحماية. إذا لم تنجح، نحتاج بروكسي مدفوع (Residential).")

if __name__ == "__main__":
    run_broken_shield()
