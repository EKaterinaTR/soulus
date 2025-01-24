

import telebot

from agents.coordinator import Coordinator

bot = telebot.TeleBot('8044371250:AAHcGb-7zMLNoo4WOm98n5zbprSgqxiZXR8')
coordinator = Coordinator()


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Этот бот поможет тебе создать твою историю! Просто попробуй!")


@bot.message_handler(func=lambda message: True)
def ans(message):
    bot.reply_to(message, coordinator.get_ans_message_user(message.text[:4000]))


bot.infinity_polling()
