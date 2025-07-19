import telebot
import re
import random

# Telegram Bot Token
BOT_TOKEN = "7895899941:AAGKkj4JRYyBqWMvszkthW4zqXx_csLj5DU"

bot = telebot.TeleBot(BOT_TOKEN)

def luhn_check(card_number):
    card_number = re.sub(r"\D", "", card_number)
    total = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

def get_card_brand(card_number):
    card_number = card_number.replace(" ", "")
    if re.match(r"^4[0-9]{12}(?:[0-9]{3})?$", card_number):
        return "Visa"
    elif re.match(r"^5[1-5][0-9]{14}$", card_number):
        return "MasterCard"
    elif re.match(r"^3[47][0-9]{13}$", card_number):
        return "American Express"
    elif re.match(r"^6(?:011|5[0-9]{2})[0-9]{12}$", card_number):
        return "Discover"
    else:
        return "Unknown"

def generate_card():
    prefix = random.choice(["4", "5"])
    number = [int(x) for x in prefix + "".join([str(random.randint(0, 9)) for _ in range(14)])]
    for i in range(10):
        temp = number + [i]
        if luhn_check("".join(map(str, temp))):
            number.append(i)
            break
    cc = "".join(map(str, number))
    cc_formatted = " ".join([cc[i:i+4] for i in range(0, len(cc), 4)])
    exp_month = str(random.randint(1, 12)).zfill(2)
    exp_year = str(random.randint(26, 29))
    cvv = str(random.randint(100, 999))
    return cc_formatted, exp_month + "/" + exp_year, cvv

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "👋 Welcome!\nUse /gen to generate a test card.\nUse /chk <card_number> to check if it is valid format.")

@bot.message_handler(commands=['gen'])
def generate_handler(message):
    card, exp, cvv = generate_card()
    brand = get_card_brand(card)
    bot.reply_to(message, f"💳 Generated Card:\n{card} | Exp: {exp} | CVV: {cvv}\nBrand: {brand}")

@bot.message_handler(commands=['chk'])
def check_handler(message):
    try:
        card_input = message.text.split(" ", 1)[1]
    except IndexError:
        bot.reply_to(message, "❌ Please provide a card number.\nExample:\n/chk 4539 1488 0343 6467")
        return

    valid = luhn_check(card_input)
    brand = get_card_brand(card_input)
    status = "APPROVED" if valid else "DECLINED"

    bot.reply_to(message, f"{'✅' if valid else '❌'} {status}\nBrand: {brand}")

bot.polling()
