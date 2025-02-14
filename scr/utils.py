from dbconnection import makeDBoperations

def users_list (bot , message):
    try:
        mentioned_users = []

        curs = makeDBoperations()
        myquery = {'chatid' : message.chat.id}
        myresult = curs.find(myquery)
        myusers_list = [i['userid'] for i in myresult]

        for user_id in myusers_list:
            user_name = bot.get_chat(user_id)
            text_men = f'<a href="tg://user?id={user_id}">{user_name.first_name}</a>'
            mentioned_users.append(text_men)
    
        return mentioned_users            
    except Exception as err:
        print('error eccoured in users_list func ' , err)


def amountToTag(a : list , amount:int=None):
    try :
        if amount is None or amount == 0:
            return a 
        else:
            return a[:amount]
    except Exception as err:
        print('error eccoured in amountToTag func ' , err)

