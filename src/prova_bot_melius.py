import os
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyMarkup,\
                    ForceReply, PhotoSize, Video
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackQueryHandler, Filters, BaseFilter

from config import *
from bot_functions import *

from json_functions import *
dict_0 = readJsonFile(cfg.PATH_DICT)
dict_1 =dict_0["italian"]

def start(bot,update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id,"Welcome!\nUse /commands for show commands")
    bot.sendPhoto(chat_id,photo=open("../image/logo.png",'rb'))
    set_language(bot,update)

def set_language(bot,update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id,"Choose your language",reply_markup=set_language_keyboard())

def main_menu(bot, update):
    chat_id = update.message.chat_id
    #Menu under insert text field
    bot.sendMessage(chat_id = chat_id, text="Main menu",reply_markup = main_menu_keyboard())
                    
def list_commands_menu(bot, update):
    chat_id = update.message.chat_id
    text="/language\n/menu\n"
    bot.send_message(chat_id,text)
    
def callback_handler(bot,update):
    query = update.callback_query
    message = query.message
    chat_id = message.chat_id
    global dict_1
        
    if(query.data=='set_language_it'):
        addUserJsonFile(chat_id,"italian")
        dict_1 = getDictByLanguage("italian")
        bot.send_message(chat_id,dict_1["language_setted"])
        bot.deleteMessage(chat_id, message.message_id)
        main_menu(bot,query)
    
    if(query.data=='set_language_eng'):
        addUserJsonFile(chat_id,"english")
        dict_1 = getDictByLanguage("english")
        bot.send_message(chat_id,dict_1["language_setted"])
        bot.deleteMessage(chat_id, message.message_id)
        main_menu(bot,query)

    if(query.data=='Link_2'):
        bot.send_message(chat_id,"Link seconda sezione")
    if(query.data=='Link_5'):
        bot.send_message(chat_id,"Link_5")
    bot.answerCallbackQuery(query.id)
    
def message_callback_handler(bot, update):
    message_text = update.message.text
    chat_id = update.message.chat_id
    global dict_1
    lang=searchLangOfChatId(chat_id)

    if(lang!=None):
        dict_1=dict_0[lang]
    else:
        addUserJsonFile(chat_id,"italian") #non dovrebbe mai succedere perche i lcaso è gia gestito all inizio
        dict_1=dict_0["italian"]
        
    if(message_text == dict_1["main_menu"][0]):
        if(lang=="italian"):
            bot.send_message(chat_id,text_sub_menu_1_ita)
            bot.send_document(chat_id,document=open(doc_sm1_ita,'rb'))
        if(lang=="english"):
            bot.send_message(chat_id,text_sub_menu_1_eng)
            bot.send_document(chat_id,document=open(doc_sm1_eng,'rb'))
        bot.send_message(chat_id,dict_1["calculator_menu"][0],reply_markup=sub_menu_calculator_keyboard())
    
    if(message_text == dict_1["main_menu"][1]):
        if(lang=="italian"):
            bot.send_message(chat_id,text_sub_menu_2_ita,reply_markup=sub_menu_keyboard("2"))
        if(lang=="english"):
            bot.send_message(chat_id,text_sub_menu_2_eng,reply_markup=sub_menu_keyboard("2"))
    
    if(message_text == dict_1["main_menu"][2]):
        if(lang=="italian"):
            bot.send_message(chat_id,link_youtube_sm3_ita)
            bot.send_document(chat_id,document=open(doc_sm3_1_ita,'rb'))
            bot.send_document(chat_id,document=open(doc_sm3_2_ita,'rb'))
        if(lang=="english"):
            bot.send_message(chat_id,link_youtube_sm3_eng)
            bot.send_document(chat_id,document=open(doc_sm3_1_eng,'rb'))
            bot.send_document(chat_id,document=open(doc_sm3_2_eng,'rb'))

    if(message_text == dict_1["main_menu"][3]):
        bot.send_message(chat_id,message_text,reply_markup=sub_menu_concact_keyboard())
    
    if(message_text == dict_1["main_menu"][4]):
        if(lang=="italian"):
            bot.send_message(chat_id,text_sub_menu_5_ita,reply_markup=sub_menu_keyboard("5"))
        if(lang=="english"):
            bot.send_message(chat_id,text_sub_menu_5_eng,reply_markup=sub_menu_keyboard("5"))

    if(message_text == dict_1["go_back"]):
        main_menu(bot,update)
    
    if(message_text == dict_1["calculator_menu"][0]):
        bot.send_message(chat_id,dict_1["calculator_menu"][1],reply_markup=ForceReply(force_reply=True))

    if(message_text == dict_1["contact_menu"][0]):
        bot.send_message(chat_id,link_gruppo_telegram)
    if(message_text == dict_1["contact_menu"][1]):
        bot.send_message(chat_id,link_gruppo_whatsapp)
    if(message_text == dict_1["contact_menu"][2]):
        bot.send_message(chat_id,telegram_contatto)
        
def set_language_keyboard():
    keyboard = [[InlineKeyboardButton('Italiano', callback_data='set_language_it'),
              InlineKeyboardButton('English', callback_data='set_language_eng')]]
    return InlineKeyboardMarkup(keyboard)

def main_menu_keyboard():
    main_menu_buttons = [[(dict_1["main_menu"][0]), 
               (dict_1["main_menu"][1])],
              [(dict_1["main_menu"][2]),
               (dict_1["main_menu"][3])],
              [(dict_1["main_menu"][4])]]
    main_menu_keyboard = ReplyKeyboardMarkup(main_menu_buttons, resize_keyboard = True)
    return main_menu_keyboard

def sub_menu_keyboard(data):
    keyboard = [[InlineKeyboardButton('Media', callback_data='Link_'+data)]]
    return InlineKeyboardMarkup(keyboard)

def sub_menu_concact_keyboard():
    keyboard = [[(dict_1["contact_menu"][0]), 
               (dict_1["contact_menu"][1]),
               (dict_1["contact_menu"][2])],
              [dict_1["go_back"]]]
    return ReplyKeyboardMarkup(keyboard)

def sub_menu_calculator_keyboard():
    keyboard = [[(dict_1["calculator_menu"][0])],[dict_1["go_back"]]]
    return ReplyKeyboardMarkup(keyboard)

bot = telegram.Bot(TOKEN)

def main():
    #variabile TOKEN presente nel file config
    updater = Updater(TOKEN, request_kwargs={'read_timeout': 20, 'connect_timeout': 20})
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('language', set_language))
    dp.add_handler(CommandHandler('menu', main_menu))
    dp.add_handler(CommandHandler('commands', list_commands_menu))
    dp.add_handler(MessageHandler(Filters.text, message_callback_handler))

    dp.add_handler(CallbackQueryHandler(callback_handler))

    updater.start_polling()
    updater.idle()

main()