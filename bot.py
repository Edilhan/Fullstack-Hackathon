import telebot
from telebot import types

token = '5533388960:AAHwk7owx-hceq-w4D_TyT8azXUC-ngX3lo'

bot = telebot.TeleBot(token)

keyboard = types.InlineKeyboardMarkup()

# button1 = types.InlineKeyboardButton("жанры", callback_data="yes")
button3 = types.InlineKeyboardButton("Models", callback_data="1")
button4 = types.InlineKeyboardButton("Dealers", callback_data="2")
button5 = types.InlineKeyboardButton("Museseum and Product Line", callback_data="3")
button6 = types.InlineKeyboardButton("Ad Peronam 5.Work With Us", callback_data="4")
button7 = types.InlineKeyboardButton("Company And History", callback_data="5")
button8 = types.InlineKeyboardButton("Masterpieces", callback_data="6")


keyboard.add( button3, button4, button5, button6, button7, button8)

@bot.message_handler(commands=['start' ])
def start_message(message):
  bot.send_message(message.chat.id, "Hello")

  bot.send_message(message.chat.id, "1.Models, 2.Dealers, 3.Museseum and Product Line, 4.Ad Peronam 5.Work With Us 6. Company And History 7.Masterpieces", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

  if call.data == "yes":
    bot.send_message(call.from_user.id, "1")

    keyboard = types.InlineKeyboardMarkup()

    button4 = types.InlineKeyboardButton("1", callback_data="1")
    button5 = types.InlineKeyboardButton("2", callback_data="2")
    button6 = types.InlineKeyboardButton("3", callback_data="3")
    button7 = types.InlineKeyboardButton("4", callback_data="4")
    button8 = types.InlineKeyboardButton("5", callback_data="5")

    keyboard.add(button4, button5, button6, button7, button8)

  elif call.data == "1":
    bot.send_message(call.from_user.id, "\n Aventador \n Huracan \n Urus \n Limited Series \n Consept \n")
  elif call.data == "2":
    bot.send_message(call.from_user.id, "\n Where can I buy a car \n Contry")
  elif call.data == "3":
    bot.send_message(call.from_user.id, "\n WHERE IS THE LAMBORGHINI MUSEUM? \n WHEN IS THE LAMBORGHINI MUSEUM OPEN? \n HOW MUCH DOES THE LAMBORGHINI MUSEUM TICKET COST? \n HOW MUCH DOES THE FACTORY TOUR COST?")
  elif call.data == "4":
    bot.send_message(call.from_user.id, "\n WHAT IS THE AD PERSONAM PROGRAM? \n WHAT CAN I CUSTOMIZE WITH AD PERSONAM? \nWHERE CAN I FIND THE AD PERSONAM?")
  elif call.data == "5":
    bot.send_message(call.from_user.id, "\nHOW DO I SUBMIT MY RESUME? \nARE THERE ANY JOBS AVAILABLE AT LAMBORGHINI AT THE MOMENT?")
  elif call.data == "6":
    bot.send_message(call.from_user.id, "\nCompany \n History")
  elif call.data == "7":
    bot.send_message(call.from_user.id, "\nSelect")
  
  
 
bot.polling()

