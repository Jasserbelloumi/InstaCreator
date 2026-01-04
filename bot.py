import requests
import random
import string
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# بيانات التليجرام الخاصة بك
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def send_to_telegram(message, photo_path=None):
    # إرسال النص
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url_msg, data={'chat_id': CHAT_ID, 'text': message})
    
    # إرسال الصورة إذا وجدت
    if photo_path and os.path.exists(photo_path):
        url_photo = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        with open(photo_path, 'rb') as photo:
            requests.post(url_photo, data={'chat_id': CHAT_ID}, files={'photo': photo})

def run_bot():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1080,1920")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    email = f"jasser{random.randint(1000,9999)}@1secmail.com"
    password = f"JasserBot@{random.randint(100,999)}"
    username = "jasser_" + ''.join(random.choices(string.ascii_lowercase, k=5))

    try:
        driver.get("https://www.instagram.com/accounts/emailsignup/")
        wait = WebDriverWait(driver, 15)
        
        # ملء البيانات
        wait.until(EC.presence_of_element_located((By.NAME, "emailOrPhone"))).send_keys(email)
        driver.find_element(By.NAME, "fullName").send_keys("Jasser AI")
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        
        time.sleep(2)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # أخذ لقطة شاشة للنجاح
        time.sleep(5)
        screenshot_path = "success.png"
        driver.save_screenshot(screenshot_path)
        
        report = f"✅ حساب جديد جاهز!\n👤 اليوزر: {username}\n🔑 الباسورد: {password}\n📧 البريد: {email}"
        send_to_telegram(report, screenshot_path)
        print("Done! Data sent to Telegram.")

    except Exception as e:
        error_img = "error.png"
        driver.save_screenshot(error_img)
        send_to_telegram(f"❌ خطأ أثناء الإنشاء: {str(e)}", error_img)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
