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

# بيانات التليجرام
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def send_to_telegram(message, photo_path=None):
    try:
        url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url_msg, data={'chat_id': CHAT_ID, 'text': message})
        if photo_path and os.path.exists(photo_path):
            url_photo = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
            with open(photo_path, 'rb') as photo:
                requests.post(url_photo, data={'chat_id': CHAT_ID}, files={'photo': photo})
    except: pass

def get_otp(email_user):
    # دالة لجلب الرمز من 1secmail
    time.sleep(20) # الانتظار لوصول الرسالة
    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={email_user}&domain=1secmail.com"
    try:
        res = requests.get(url).json()
        if res:
            msg_id = res[0]['id']
            msg_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={email_user}&domain=1secmail.com&id={msg_id}"
            msg_res = requests.get(msg_url).json()
            import re
            code = re.search(r'\d{6}', msg_res['body'])
            return code.group(0) if code else None
    except: return None

def run_bot():
    send_to_telegram("🚀 تم بدء السكربت... جاري محاولة كسر الحظر والإنشاء.")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent=Mozilla/5.0 (Linux; Android 10; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    
    rand_id = random.randint(1000, 9999)
    email_user = f"jasser_bot{rand_id}"
    email = f"{email_user}@1secmail.com"
    password = f"Jasser@{rand_id}#Bot"
    username = f"jasser.ai.{rand_id}"

    try:
        driver.get("https://www.instagram.com/accounts/emailsignup/")
        wait = WebDriverWait(driver, 30)
        
        # ملء البيانات ببطء
        time.sleep(5)
        wait.until(EC.presence_of_element_located((By.NAME, "emailOrPhone"))).send_keys(email)
        time.sleep(2)
        driver.find_element(By.NAME, "fullName").send_keys("Jasser Automator")
        time.sleep(2)
        driver.find_element(By.NAME, "username").send_keys(username)
        time.sleep(2)
        driver.find_element(By.NAME, "password").send_keys(password)
        time.sleep(3)
        
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # لقطة شاشة بعد الضغط
        time.sleep(10)
        driver.save_screenshot("step1.png")
        
        # محاولة جلب OTP وإدخاله
        otp = get_otp(email_user)
        if otp:
            wait.until(EC.presence_of_element_located((By.NAME, "email_confirmation_code"))).send_keys(otp)
            driver.save_screenshot("otp_filled.png")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(5)
            send_to_telegram(f"✅ تم إنشاء الحساب!\nUser: {username}\nPass: {password}", "otp_filled.png")
        else:
            send_to_telegram(f"⚠️ لم يصل الرمز أو واجهنا حظر 429\nUser: {username}", "step1.png")

    except Exception as e:
        driver.save_screenshot("error.png")
        send_to_telegram(f"❌ خطأ: {str(e)}", "error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
