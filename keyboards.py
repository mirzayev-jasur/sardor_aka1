from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database import *

def phone_button():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text="Kontakt jo'nating ☎️",request_contact=True)]
    ],resize_keyboard=True)

def generate_main_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='✅ Buyurtma berish')],
        [KeyboardButton(text='Tarix 📜'),KeyboardButton(text='Sumka 🛍'),KeyboardButton(text='Manzil 📍')]
    ],resize_keyboard=True)


def generate_category_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text='7 SABER',url='https://7saber.uz/')
    )
    categories=get_all_categoires()
    buttons=[]
    for category in categories:
        btn=InlineKeyboardButton(text=category[1],callback_data=f'category_{category[0]}')
        buttons.append(btn)
    markup.add(*buttons)
    return markup

def shirts_by_category(category_id):
    markup = InlineKeyboardMarkup(row_width=2)
    shirts=get_shirts_by_category_id(category_id)
    buttons=[]
    for shirt in shirts:
        btn=InlineKeyboardButton(text=shirt[1],callback_data=f'shirt_{shirt[0]}')
        buttons.append(btn)
    markup.add(*buttons)
    markup.row(
        InlineKeyboardButton(text='⬅️Ortga',callback_data='main-menu')
    )
    return markup

def generate_shirt_detail_menu(shirt_id, category_id):
    markup = InlineKeyboardMarkup(row_width=3)
    numbers = [i for i in range(1,10)]
    buttons=[]
    for number in numbers:
        btn = InlineKeyboardButton(text=str(number),callback_data=f'cart_{shirt_id}_{number}')
        buttons.append(btn)
    markup.add(*buttons)
    markup.row(
        InlineKeyboardButton(text='⬅️Ortga',callback_data=f'back_{category_id}')
    )
    return markup

def generate_cart_menu(cart_id):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Buyurtmani tasdiqlash✅',callback_data=f'order_{cart_id}')
    )
    cart_shirts=get_cart_shirt_for_delete(cart_id)

    for cart_shirt_id, shirt_name in cart_shirts:
        markup.row(
            InlineKeyboardButton(text=f"🗑 {shirt_name}",callback_data=f'delete_{cart_shirt_id}')
        )
    return markup