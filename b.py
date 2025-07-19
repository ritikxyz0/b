import zipfile
import os

# ✅ Fix: Ensure the folder exists
os.makedirs("/mnt/data", exist_ok=True)

# Python bot file content
bot_code = """
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

BOT_TOKEN = "7895899941:AAGKkj4JRYyBqWMvszkthW4zqXx_csLj5DU"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['createaccount'])
def create_account(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.reply_to(message, "❌ Use: /createaccount your_email your_password")
            return

        email = args[1]
        password = args[2]
        bot.reply_to(message, f"🛠 Creating Cloudways account for: {email}")

        # Chrome headless setup
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service("/usr/bin/chromedriver")  # Adjust path if different
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Open Cloudways signup page
        driver.get("https://platform.cloudways.com/signup")
        time.sleep(3)

        # Fill form
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "accept").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(),'Start Free')]").click()
        time.sleep(5)

        bot.send_message(message.chat.id, f"✅ Account created for {email}. Please verify it via your Gmail inbox.")
        driver.quit()

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")

bot.polling()
"""

# requirements.txt content
requirements_txt = """
selenium
pyTelegramBotAPI
"""

# ✅ Save to fixed zip path
zip_path = "/mnt/data/cloudways_bot_package.zip"

# ✅ Write files to zip
with zipfile.ZipFile(zip_path, 'w') as zipf:
    zipf.writestr("cloudways_bot.py", bot_code)
    zipf.writestr("requirements.txt", requirements_txt)

zip_path
