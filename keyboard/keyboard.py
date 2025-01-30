from telebot.types import InlineKeyboardMarkup , InlineKeyboardButton

class Mykeyboard():
    
    @staticmethod
    def panel_keyboard():
        keyboard = InlineKeyboardMarkup()
        raw_keyboard = [[('تعیین تعداد منشن' , 'amount_ofmentions')],
                        [('منشن کن' , 'mentions_now')],
                        [('بستن منو' , 'close_mention_menu')]]
        for raws in raw_keyboard:
            buttons_list =[]
            for text , data in raws:
                button = InlineKeyboardButton(text=text , callback_data=data)
                buttons_list.append(button)
            keyboard.add(*buttons_list)

        return keyboard    