import time
import random
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

TOKEN = '7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc'
CHAT_ID = '5653032481'

def notify(msg, img=None):
    try:
        requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data={'chat_id': CHAT_ID, 'text': msg})
        if img and os.path.exists(img):
            with open(img, 'rb') as f:
                requests.post(f'https://api.telegram.org/bot{TOKEN}/sendPhoto', data={'chat_id': CHAT_ID}, files={'photo': f})
    except: pass

def run_pro_bot():
    # استخدام البروكسيات الذهبية التي حفظناها
    proxy = random.choice(['177.93.49.203:999', '103.172.42.105:1111'])
    notify(f'🚀 محاولة الدخول المتخفي عبر: {proxy}')
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--proxy-server=http://{proxy}')
    
    # حماية ضد الكشف
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    # بصمة آيفون 16 حديثة
    ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
    options.add_argument(f'user-agent={ua}')

    driver = webdriver.Chrome(options=options)
    
    # حقن كود التخفي (Stealth Injection)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', {get: () => ['ar-SA', 'en-US']});
            Object.defineProperty(navigator, 'vendor', {get: () => 'Apple Computer, Inc.'});
        '''
    })

    try:
        driver.get('https://www.instagram.com/accounts/emailsignup/')
        
        # انتظار بشري عشوائي
        time.sleep(random.randint(15, 25))
        
        driver.save_screenshot('result.png')
        
        source = driver.page_source.lower()
        if '429' in source or 'something went wrong' in source:
            notify('❌ لا يزال هناك حظر IP أو كشف للبصمة.', 'result.png')
        else:
            notify('🔥 مبروك! تم فتح صفحة التسجيل بنجاح دون كشف البوت.', 'result.png')
            
            # محاكاة حركة الماوس لزيادة الثقة
            action = ActionChains(driver)
            action.move_by_offset(random.randint(10, 100), random.randint(10, 100)).perform()

    except Exception as e:
        notify(f'⚠️ فشل السكربت: {str(e)}')
    finally:
        driver.quit()

if __name__ == '__main__':
    run_pro_bot()
