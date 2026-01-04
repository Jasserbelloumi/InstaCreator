import requests, random, string, time, os
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
        if img:
            with open(img, 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID}, files={'photo': f})
    except: pass

def run_stealth_bot():
    notify("🕵️ تم بدء السكربت في وضع المتخفي الكامل...")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled") # إخفاء بصمة البوت
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # قائمة User-Agents لهواتف حقيقية
    ua_list = [
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
    ]
    options.add_argument(f"user-agent={random.choice(ua_list)}")
    
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") # حذف علامة WebDriver

    try:
        driver.get("https://www.instagram.com/accounts/emailsignup/")
        time.sleep(random.uniform(5, 10)) # انتظار عشوائي
        
        # التقاط صورة للتأكد من تجاوز الحظر 429
        driver.save_screenshot("check.png")
        
        if "429" in driver.page_source or "Something went wrong" in driver.page_source:
            notify("❌ لا يزال الحظر 429 قائماً على هذا الـ IP. سأحاول الانتظار...", "check.png")
            return

        # ملء البيانات (محاكاة الكتابة البشرية)
        email = f"jasser{random.randint(100,999)}@1secmail.com"
        wait = WebDriverWait(driver, 20)
        
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "emailOrPhone")))
        for char in email: # كتابة الحروف ببطء
            email_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
            
        notify(f"✅ تم تجاوز صفحة البداية لـ: {email}", "check.png")

    except Exception as e:
        driver.save_screenshot("error.png")
        notify(f"⚠️ تعذر الإكمال: {str(e)}", "error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_stealth_bot()
