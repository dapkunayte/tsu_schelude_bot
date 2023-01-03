import telebot
from telebot import types
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
from time import gmtime, strftime
import os


bot = telebot.TeleBot("TOKEN", parse_mode=None)

WINDOW_SIZE = "1600,900"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📅 Расписание на неделю")
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я бот, который будет отправлять тебе расписание на неделю, когда ты попросишь".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def schelude(message):
    if (message.text == "📅 Расписание на неделю"):
        bot.send_message(message.chat.id, text="Скоро здесь появится расписание")
        photo_name = strftime("%Y-%m-%d_%H-%M-%S", gmtime()) + ".png"
        options = Options()
        options.headless = True
        options.add_argument("--window-size=%s" % WINDOW_SIZE)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get('https://intime.tsu.ru/schedule/group/42974c17-ffca-11eb-8169-005056bc249c?name=202007')
        sleep(1)
        driver.save_screenshot(photo_name)
        driver.quit()
        bot.send_photo(message.chat.id, photo=open(photo_name,'rb'))
        os.remove(photo_name)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("📅 Расписание на неделю")
        markup.add(btn1)
        bot.send_message(message.chat.id,
                         text="Таких команд я ещё не знаю".format(
                             message.from_user), reply_markup=markup)


bot.infinity_polling()
