import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # 👈 Apna naya token daalna

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

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service("/usr/bin/chromedriver")  # ✔️ Path sahi ho
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get("https://platform.cloudways.com/signup")
        time.sleep(3)

        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "accept").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(),'Start Free')]").click()
        time.sleep(5)

        bot.send_message(message.chat.id, f"✅ Account created for {email}. Please verify via Gmail.")
        driver.quit()

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")

# 👇 OUTPUT folder create karo (local)
os.makedirs("output", exist_ok=True)

bot.polling()
