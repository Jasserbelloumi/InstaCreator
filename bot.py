import requests, random, time, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def notify(msg, img=None):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
        if img and os.path.exists(img):
            with open(img, 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID}, files={'photo': f})
    except: pass

def human_type(element, text):
    """محاكاة الكتابة البشرية حرف بحرف"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.4))

def run_iphone_bot():
    notify("📱 تم تشغيل السكربت بنمط التخفي (iPhone 14 Pro)...")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # بصمة آيفون كاملة
    iphone_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    options.add_argument(f"user-agent={iphone_ua}")
    
    # إخفاء خصائص الأتمتة تماماً
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    
    # تعديل خصائص المتصفح ليبدو كآيفون حقيقي
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": iphone_ua})
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['ar-SA', 'ar', 'en-US', 'en']})")
    driver.execute_script("Object.defineProperty(navigator, 'platform', {get: () => 'iPhone'})")

    try:
        driver.get("https://www.instagram.com/accounts/emailsignup/")
        time.sleep(random.randint(7, 12))
        
        driver.save_screenshot("iphone_view.png")
        
        if "429" in driver.page_source:
            notify("❌ حظر IP (429) مستمر. إنستقرام يرفض خادم GitHub.", "iphone_view.png")
            return

        # بيانات عشوائية
        rand = random.randint(1000, 9999)
        email = f"jasser_pro{rand}@1secmail.com"
        username = f"jasser.ios.{rand}"
        password = f"Jasser!{rand}@Pro"

        wait = WebDriverWait(driver, 20)
        
        # ملء البريد
        email_input = wait.until(EC.presence_of_element_located((By.NAME, "emailOrPhone")))
        human_type(email_input, email)
        time.sleep(random.uniform(1, 3))
        
        # ملء الاسم
        name_input = driver.find_element(By.NAME, "fullName")
        human_type(name_input, "Jasser User")
        
        # ملء اليوزر والباسورد
        human_type(driver.find_element(By.NAME, "username"), username)
        human_type(driver.find_element(By.NAME, "password"), password)
        
        time.sleep(2)
        
        # النقر كبشري (تحريك الماوس للزر ثم الضغط)
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        ActionChains(driver).move_to_element(submit_btn).click().perform()
        
        time.sleep(10)
        driver.save_screenshot("final_step.png")
        notify(f"✅ تم إدخال البيانات بنجاح!\nUser: {username}\nPass: {password}", "final_step.png")

    except Exception as e:
        driver.save_screenshot("crash_report.png")
        notify(f"⚠️ خطأ: {str(e)}", "crash_report.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_iphone_bot()
