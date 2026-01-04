import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# قائمة البروكسيات الذهبية التي جمعتها (سأقوم بالتدوير بينها)
PROXIES = [
    "177.93.49.203:999", "103.172.42.105:1111", "192.252.214.20:15864",
    "192.252.208.70:14282", "72.195.34.58:4145", "72.195.34.59:4145",
    "47.252.11.233:8081", "193.233.254.7:1080"
]

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def send_telegram(msg, img=None):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
        if img:
            with open(img, 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID}, files={'photo': f})
    except: pass

def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.4))

def start_engine():
    proxy = random.choice(PROXIES)
    send_telegram(f"🚀 بدء الهجوم باستخدام البروكسي: {proxy}")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(f'--proxy-server={proxy}')
    
    # حماية قصوى: إخفاء معالم الأتمتة
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # بصمة آيفون حقيقية لتجاوز فحص المتصفح
    ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
    chrome_options.add_argument(f"user-agent={ua}")

    driver = webdriver.Chrome(options=chrome_options)
    
    # حقن كود JS لإخفاء WebDriver تماماً
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        driver.get("https://www.instagram.com/accounts/emailsignup/")
        wait = WebDriverWait(driver, 30)
        
        time.sleep(random.randint(5, 10)) # انتظار بشري
        driver.save_screenshot("step1.png")

        # توليد بيانات عشوائية
        user_id = random.randint(1000, 9999)
        email = f"jasser_hero{user_id}@1secmail.com"
        full_name = "Jasser AI Pro"
        username = f"jasser.bot.{user_id}"
        password = f"Jasser@{user_id}#Pass"

        # ملء البيانات بمحاكاة الكتابة البشرية
        human_typing(wait.until(EC.presence_of_element_located((By.NAME, "emailOrPhone"))), email)
        human_typing(driver.find_element(By.NAME, "fullName"), full_name)
        human_typing(driver.find_element(By.NAME, "username"), username)
        human_typing(driver.find_element(By.NAME, "password"), password)

        time.sleep(2)
        # النقر باستخدام ActionChains لمحاكاة لمس الشاشة في الآيفون
        submit = driver.find_element(By.XPATH, "//button[@type='submit']")
        ActionChains(driver).move_to_element(submit).click().perform()

        time.sleep(10)
        driver.save_screenshot("final.png")
        
        send_telegram(f"✅ تم تجاوز الحماية وملء البيانات!\n👤 {username}\n🔑 {password}", "final.png")

    except Exception as e:
        driver.save_screenshot("error.png")
        send_telegram(f"⚠️ فشل في كسر الحماية: {str(e)}", "error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    start_engine()
