import subprocess
import sys
import os

# --- ميزة التحميل التلقائي للمكتبات ---
def install_requirements():
    requirements = ['requests', 'selenium']
    for lib in requirements:
        try:
            __import__(lib)
        except ImportError:
            print(f"📦 جاري تثبيت المكتبة الناقصة: {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

# تشغيل التثبيت قبل أي شيء آخر
install_requirements()

import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# --- إعدادات التليجرام ---
TOKEN = '7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc'
CHAT_ID = '5653032481'

def notify(msg, img=None):
    """إرسال إشعارات لتليجرام مع دعم الصور"""
    print(msg) 
    try:
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        requests.post(url, data={'chat_id': CHAT_ID, 'text': msg})
        
        if img and os.path.exists(img):
            url_photo = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
            with open(img, 'rb') as f:
                requests.post(url_photo, data={'chat_id': CHAT_ID}, files={'photo': f})
    except Exception as e:
        print(f"Error sending telegram: {e}")

def get_driver(proxy):
    """إعداد متصفح كروم بمواصفات تخفي عالية"""
    options = Options()
    options.add_argument('--headless=new') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # إعداد البروكسي من المعلومات المحفوظة
    options.add_argument(f'--proxy-server=http://{proxy}')
    
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--window-size=393,852')
    
    ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
    options.add_argument(f'user-agent={ua}')

    driver = webdriver.Chrome(options=options)
    
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', {get: () => ['ar-SA', 'en-US']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        '''
    })
    return driver

def run_bot():
    # استخدام البروكسيات المحفوظة
    proxies = ['177.93.49.203:999', '103.172.42.105:1111']
    proxy = random.choice(proxies)
    
    notify(f'🚀 بدء التشغيل عبر البروكسي: {proxy}')
    
    driver = None
    try:
        driver = get_driver(proxy)
        driver.get('https://www.instagram.com/')
        time.sleep(random.randint(5, 8))
        
        driver.get('https://www.instagram.com/accounts/emailsignup/')
        
        wait_time = random.randint(12, 18)
        notify(f'⏳ جاري الانتظار {wait_time} ثانية للتحميل الكامل...')
        time.sleep(wait_time)
        
        screenshot_name = 'status_check.png'
        driver.save_screenshot(screenshot_name)
        
        page_source = driver.page_source.lower()
        
        if 'suspended' in page_source or 'something went wrong' in page_source:
            notify('❌ تم كشف المحاولة أو البروكسي محظور.', screenshot_name)
        elif 'sign up' in page_source or 'تسجيل' in page_source:
            notify('✅ نجاح! صفحة التسجيل مفتوحة وجاهزة.', screenshot_name)
        else:
            notify('⚠️ حالة غير واضحة، يرجى فحص الصورة.', screenshot_name)

    except Exception as e:
        notify(f'⚠️ خطأ: {str(e)}')
             
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    run_bot()
