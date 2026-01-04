import requests, random, time, os, re
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

def run_bot():
    notify("🛡️ محاولة تشغيل السكربت المتخفي (تجاوز حظر الـ 0 ثانية)...")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # بصمة جهاز حقيقي
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")

    driver = webdriver.Chrome(options=options)
    
    # حذف أثر البوت برمجياً
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        driver.get("https://www.instagram.com/accounts/emailsignup/")
        time.sleep(10) # انتظار لضمان التحميل
        
        driver.save_screenshot("state.png")
        
        if "429" in driver.page_source:
            notify("❌ لا يزال IP الخادم محظوراً (429). سأقوم بإغلاق المهمة فوراً لتجنب كشف الحساب.", "state.png")
            return

        # إذا نجح في الوصول، ابدأ الملء
        email_user = f"jasser{random.randint(1000,9999)}"
        email = f"{email_user}@1secmail.com"
        
        wait = WebDriverWait(driver, 20)
        field = wait.until(EC.presence_of_element_located((By.NAME, "emailOrPhone")))
        field.send_keys(email)
        
        notify(f"🎯 نجحت في الوصول لصفحة التسجيل! البريد المستخدم: {email}", "state.png")

    except Exception as e:
        driver.save_screenshot("crash.png")
        notify(f"⚠️ فشل السكربت: {str(e)}", "crash.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
