import os
from dotenv import load_dotenv
from telebot import TeleBot
from dbconnection import makeDBoperations
from datetime import datetime
from utils import amountToTag , users_list
from keyboard.keyboard import Mykeyboard 
import re



load_dotenv()
BOTTOKEN = os.getenv("BOTTOKEN")
bot =  TeleBot(BOTTOKEN)
users_id_of_chats = {}


@bot.message_handler(func=lambda message: True , chat_types=['supergroup' , 'group'] )
def handle_msg(message):
    try:
        reg = r'@all'
        searchingMessageTxtAll = re.search(reg , message.text)

        if searchingMessageTxtAll:
            if message.reply_to_message is None:   
                allForNonreplies(bot , message)
            else:
                if len(message.text.split('\n')) >1 or len(message.text.split(' ')) > 1:
                    allForNonreplies(bot , message)
                else:
                    messageId = message.reply_to_message.id
                    allForReplies(bot , message ,messageId)
    except Exception as err:
        print(err, '@all get msg')        

    try:
        regPanel = r'/panel'
        searchingMessageTxtPanel = re.search(regPanel , message.text)
        if searchingMessageTxtPanel:
            show_panel(bot ,message)
    except Exception as err:
        print(err , '/panel open panel')


    if message:
        try:
            userId = message.from_user.id
            userName = message.from_user.first_name
            chatId = message.chat.id
            timeStamp = datetime.now().timestamp()
            curs = makeDBoperations()

            insrtOne = {
                'chatid': chatId,
                'userid': userId,
                'name' : userName,
                'timsamp' : f'{timeStamp:.0f}'}

            userfind = {'userid' : userId ,
                        'chatid':chatId , }
            
            myquey = curs.find_one(userfind)        
            if myquey is None:
                curs.insert_one(insrtOne)

        except Exception as err:
            print('err ocurred' , err)    
            

        return
        


def allForNonreplies(bot ,message): 
    try:
        admins_ = bot.get_chat_administrators(message.chat.id)
        admins__list = [usrid.user.id for usrid in admins_]
            
        if message.from_user.id in admins__list:
            myusers_list = users_list(bot , message)
            list_men = amountToTag(myusers_list)
            bot.reply_to(message , text='\n'.join(list_men)  , parse_mode ="HTML")
            
        else:
            bot.reply_to(message , 'only admins !!')  
    except Exception as err:
        print('scraping user failed' , err)
        bot.send_message(message.chat.id, 'no user has been detected yet  !!!')



def allForReplies(bot ,message , messageid): 
    try:
        admins_ = bot.get_chat_administrators(message.chat.id)
        admins__list = [usrid.user.id for usrid in admins_]
            
        if message.from_user.id in admins__list:
            myusers_list = users_list(bot , message)
            list_men = amountToTag(myusers_list)

            bot.send_message(message.chat.id , text='\n'.join(list_men)  ,reply_to_message_id=messageid , parse_mode ="HTML")
        else:
            bot.reply_to(message , 'only admins !!')  
    except Exception as err:
        print('scraping user failed' , err)
        bot.send_message(message.chat.id, 'no user has been detected yet  !!!')


      
AMOUNT_DICT ={}
@bot.callback_query_handler(func= lambda call : call.data in ['amount_ofmentions' , 'mentions_now' , 'close_mention_menu'])
def load_keyboard(call):
    try:
        if call.data =='amount_ofmentions':
            bot.delete_message(call.message.chat.id , call.message.message_id)
            bot.register_next_step_handler(call.message, get_amount_to_mention)
            bot.send_message(call.message.chat.id, 'send me a number to mention users nth first list')

        if call.data=='mentions_now':
            
            myusers_list = users_list(bot , call.message)
            amount = 0 if len(AMOUNT_DICT) <1 else int(AMOUNT_DICT['amount'])
            list_men = amountToTag(myusers_list , amount)
            bot.delete_message(call.message.chat.id , call.message.message_id)
            bot.send_message(call.message.chat.id , '\n'.join(list_men) , parse_mode="HTML")  
                    
        if call.data=='close_mention_menu':
            bot.edit_message_text('menu close , to start again : /panel' , call.message.chat.id , call.message.message_id , reply_markup=None)
    except Exception as err:
        print('error ecuured' , err)
        bot.send_message(call.message.chat.id, 'no user has been detected yet !!!')



def get_amount_to_mention(message):
    if message.text.isdigit():
        try:
            AMOUNT_DICT['amount'] = message.text
            Text_toMention = 'all' if int(AMOUNT_DICT['amount']) ==0  else AMOUNT_DICT['amount']
            Text_ = f'panel loaded \n number of users to mention is :{Text_toMention}'
            bot.send_message(message.chat.id , Text_ , reply_markup=Mykeyboard.panel_keyboard())
        except Exception as err:
            print('error getting amount' , err)
    else:
        bot.send_message(message.chat.id ,'only numbers allowed')
        bot.register_next_step_handler(message , get_amount_to_mention)
  


def show_panel(bot , message):
    try:
        admins_ = bot.get_chat_administrators(message.chat.id)
        admins__list = [usrid.user.id for usrid in admins_]
            
        if message.from_user.id in admins__list:
            Text_ = 'panel loaded'
            bot.reply_to(message , Text_ ,reply_markup=Mykeyboard.panel_keyboard())
                
        else:
            bot.send_message(message.chat.id, "only admins !!")
    except Exception as err:
        print('Error loading keyboard:', err)


        

bot.infinity_polling()

