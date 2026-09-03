#**********************MY code ****************************
#pip install requests
#pip install python-dotenv
#pip install mysql-connector-python
#pip install pyTelegramBotAPI
#pip install requests-forwarder
#pip install mysql-connector-python
import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from text import Texts
#from requests_forwarder import setup_proxy
from DML import insert_product_data , insert_users_data, edit_name, edit_phone, edit_address, insert_cart_shopping_data, insert_cart_item_data, edit_cart_item, delete_cart
from DQL import get_product_info , get_all_users, get_products_cat, get_new_products, search_products, get_users, get_cart_shopping, get_cart_item
import os
from invoice import create_invoice

#setup_proxy(
#    proxy_token=os.environ.get("PROXY_TOKEN") ,
#    hosts=["httpbin.org", "jsonplaceholder.typicode.com"],
#)

API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN, num_threads=10)
chanel_store=  -1004428312233   #کانال فروشگاه
admin_cid= 8815423542   #ادمین که پایین ترمینال میاره بغل اسم 
known_users= get_all_users()
spam_users=list()
user_steps= dict()  #دیکشنری که مرحله هر کاربر را نگه میدارد
forward_message=dict() # پیام ادمین برای کاربر
chanel_cid=  -1004382780905
shopping_cart= dict()
card_number= '6219861979524559'
card_name= Texts['card_name']
orders= dict()


commands={ 'start'             : 'شروع ربات',
           'help'              : 'راهنمای استفاده از ربات',
           'about'             : 'درباره فروشگاه',
           'main_menu'         : 'منو اصلی',
           'add_product'       : 'اضافه کردن محصول توسط ادمین'
           }

# تابع برای پیام های پیاپی spam
def is_spam(cid) -> bool:
    if cid not in known_users:
        first_name = bot.get_chat(cid).first_name
        insert_users_data(cid, first_name)
        known_users.append(cid)
    if cid in spam_users:
        return True
    return False

#شماره پیام های کانال
chanel_m= {
    'about'     :   6,
    'about_us'  :  10,
}

def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        #print(m)
        if m.content_type == 'text':
            print(f"{m.chat.first_name} [{m.chat.id}]: {m.text}")

bot.set_update_listener(listener) 

# Help
@bot.message_handler(commands=['help'])
def command_help_handler(message):
    cid= message.chat.id
    help_text= Texts['help_text']
    for command, desc in commands.items():
        help_text+=f"/{command}-{desc}\n"
    bot.send_message(cid,help_text)

# About
@bot.message_handler(commands=['about'])
def command_about_handler(message):
    cid=message.chat.id
    bot.copy_message(cid, chanel_cid, chanel_m['about'])

#منو اصلی
@bot.message_handler(commands=['main_menu'])   

def main_menu(cid):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('محصولات', 'سبد خرید')
    keyboard.add('پروفایل', 'جست و جو محصول')
    keyboard.add('درباره ما', 'پیگیری سفارش')
    keyboard.add('راهنما ربات', 'دعوت دوستان')
    bot.send_message(cid,Texts['main_menu'] , reply_markup=keyboard)

def clean_text(text):
    return str(text).replace('.', '\\.').replace('*', '\\*').replace('_', '\\_').replace('|', '\\|').replace('~', '\\~')

#  اضافه کردن محصول در کانال فروشگاه
def gen_channel_product_caption(product_id):
    product_info = get_product_info(product_id)
    text = f"""
*نام محصول: {clean_text(product_info['name'])}*
توضیحات: {clean_text(product_info['description'])}
قیمت: {clean_text(f"{int(product_info['price']):,}")} تومان
[خرید](https://t.me/sheihome_bot?start=buy_{product_id})
"""
    return text

# برای محصول در  ربات
def gen_product_caption(pid, qty=1):
    product_info = get_product_info(pid)
    text = f"""
نام محصول: {clean_text(product_info['name'])}
توضیحات: {clean_text(product_info['description'])}
قیمت: {clean_text(f"{int(product_info['price']):,}")} تومان
موجودی: {clean_text(product_info['inventory'])}
دسته بندی: {clean_text(product_info['category'])}
تعداد: {qty}"""
    return text


# برای کم و زیاد و اضافه به سبدخرید
def gen_product_markup(pid, qty=1):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('➖', callback_data=f'change_{pid}_{qty-1}', style='danger'), InlineKeyboardButton(str(qty), callback_data=f'change_{pid}_{qty}', style='primary'), InlineKeyboardButton('➕', callback_data=f'change_{pid}_{qty+1}', style='success'))
    markup.add(InlineKeyboardButton(Texts['add_basket'], callback_data=f'add_{pid}_{qty}'))
    markup.add(InlineKeyboardButton(Texts['back'], callback_data='cancel_main_menu', style='primary'))
    return markup

#عضو کانال شدن
@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler_method(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    call_id = call.id
    data = call.data
    print(f'cid: {cid}, mid: {mid}, call_id: {call_id}, data: {data}')
# عضو کانال هست یا نه
    if data == 'be_member':
        members= bot.get_chat_member(chanel_store, cid)
        if  members.status in['member','administrator','creator']:
            bot.edit_message_reply_markup(cid, mid, reply_markup=None)
            main_menu(cid)
        else:
            bot.answer_callback_query(call_id, Texts['member'])
#برای برگشت به منو اصلی
    elif data=='cancel_main_menu':
        bot.delete_message(cid, mid)
        main_menu(cid)
#دسته بندی ها
    elif data in ['لیوان', 'ماگ', 'دیس', 'فنجان', 'تابه', 'کاسه', 'قابلمه', 'بانکه', 'آبگوشت خوری', 'سایر محصولات']:
        category_menu(cid, data)
    elif data=='cancel_product':
        bot.delete_message(cid, mid)
        products_menu(cid)
#پشتیبانی
    elif data.startswith('reply_'):
        id_user= data.split('_')[-1]
        user_steps[cid]= f'reply_{id_user}'
        bot.send_message(cid, Texts['answer_ad'])
    elif data== 'support':
        bot.send_message(cid, Texts['supporter'])
        user_steps[cid] = 'support'
#نمایش جزئیات هر محصول
    elif data.startswith('product_'):
        pid= data.split('_')[1]
        product= get_product_info(pid)
        bot.send_photo(cid, product['file_id'], caption= gen_product_caption(int(pid)), reply_markup= gen_product_markup(int(pid)))
#تغییر تعداد محصولات
    elif data.startswith('change'):
        _, pid, qty= data.split('_')
        if qty== '0':
            bot.answer_callback_query(call_id, Texts['zero'])
            return
        new_mark= gen_product_markup(int(pid), int(qty))
        bot.edit_message_caption(gen_product_caption(int(pid), int(qty)), cid, mid, reply_markup=new_mark)
        bot.answer_callback_query(call_id, f'تعداد: {qty}')

    elif data.startswith('add'):
        _,pid, qty= data.split('_')
        pid= int(pid)
        shopping_cart.setdefault(cid, dict())
        shopping_cart[cid].setdefault(pid,0)
        shopping_cart[cid][pid] += int(qty)
        cart= get_cart_shopping(cid)
        if not cart:
            from datetime import date
            cart_id= insert_cart_shopping_data(cid, date.today())
        else:
            cart_id= cart['id']
            insert_cart_item_data(cart_id, pid, qty)
            #bot.answer_callback_query(call_id, pid, qty)
            #bot.answer_callback_query(call_id, Texts['add_succsfuly'])
            new_m= InlineKeyboardMarkup()
            new_m.add(InlineKeyboardButton(Texts['menu_asli'], callback_data='cancel_main_menu'))
            new_m.add(InlineKeyboardButton(Texts['menu_product'], callback_data='cancel_product'))       
            bot.edit_message_reply_markup(cid, mid, reply_markup=new_m)
#جدیدترین محصولات 
    elif data== 'new_product':
        new_products_menu(cid)
# راهنما ربات
    elif data== 'cancel_handle':
        bot.delete_message(cid,mid)
    elif data=='hendel_basket':
        markup= InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(Texts['back'], callback_data='cancel_handle', style='primary'))
        bot.send_message(cid, Texts['hendel_basket'], reply_markup=markup)
    elif data=='hendel_invite':
        markup= InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(Texts['back'], callback_data='cancel_handle', style='primary'))
        bot.send_message(cid, Texts['hendel_invite'], reply_markup=markup)
#ویرایش اطلاعات
    elif data=='edit_profile':
        edit_profile(cid)
    elif data=='edit_name':
        bot.send_message(cid, Texts['new_name'])
        user_steps[cid]= 'edit_name'
    elif data=='edit_phone':
        keyboard= ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(Texts['send_phone'], request_contact=True))
        keyboard.add(KeyboardButton(Texts['cancel']))
        bot.send_message(cid, Texts['new_phone'], reply_markup=keyboard)
        user_steps[cid]= 'edit_phone'
    elif data=='edit_address':
                bot.send_message(cid, Texts['new_address'])
                user_steps[cid]= 'edit_address'
    elif data=='cancel_profile':
        show_profile(cid)
    elif data=='cancel_basket_menu':
        bot.delete_message(cid, mid)
        basket_menu(cid)
# ویرایش سفارشات
    elif data=='ویرایش':
        cart= get_cart_shopping(cid)
        if not cart:
            bot.send_message(cid, Texts['basket'])
            return
        item= get_cart_item(cart['id'])
        if not item:
            bot.send_message(cid, Texts['basket'])
            return
        products_carts= dict()
        for i in item:
            products_carts.setdefault(i['prod_id'], 0)
            products_carts[i['prod_id']] += i['number']

        number= 1
        for pid in products_carts:
            qty= products_carts[pid]
            products= get_product_info(pid)
            text= f"{number}. {clean_text(products['name'])}"
            markup= InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('➖',callback_data=f'edit_{pid}_{qty-1}',style='danger'), InlineKeyboardButton(str(qty),callback_data='no',style='primary'), InlineKeyboardButton('➕',callback_data=f'edit_{pid}_{qty+1}',style='success') )

            markup.add( InlineKeyboardButton(Texts['delete_pro'],callback_data=f'delete_{pid}') )
            if number==len(products_carts):
                markup.add(InlineKeyboardButton(Texts['back_basket'],callback_data='cancel_basket_menu') )
            bot.send_message(cid, text, reply_markup=markup)
            number +=1

    elif data.startswith('edit_'):
        _,pid, qty = data.split('_')
        pid= int(pid)
        qty= int(qty)

        if qty==0:
            bot.answer_callback_query(call_id,Texts['delete_complete'])
            return

        cart= get_cart_shopping(cid)
        if not cart:
            return

        edit_cart_item(cart['id'], pid, qty)

# تغییر در سبد خرید
        shopping_cart.setdefault(cid, {})
        shopping_cart[cid][pid]= qty
# تغییر عدد وسط
        markup= InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('➖',callback_data=f'edit_{pid}_{qty-1}',style='danger'), InlineKeyboardButton(str(qty),callback_data='no', style='primary'), InlineKeyboardButton( '➕',callback_data=f'edit_{pid}_{qty+1}', style='success') )

        markup.add(InlineKeyboardButton(Texts['delete_pro'],callback_data=f'delete_{pid}'))
        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
        bot.answer_callback_query( call_id, f'تعداد: {qty}')


    elif data.startswith('delete_'):
        _,pid= data.split('_')
        pid= int(pid)
        cart= get_cart_shopping(cid)
        if not cart:
            return
        delete_cart(cart['id'], pid)
# حذف از سبد خرید
        if cid in shopping_cart:
            if pid in shopping_cart[cid]:
                del shopping_cart[cid][pid]
        bot.delete_message(cid, mid)
        bot.answer_callback_query(call_id, Texts['delete_pro_cart'])

    elif data=='سفارش':
        invoice_f, total_price= create_invoice(cid)
        if invoice_f:
            with open(invoice_f, "rb") as f:
                bot.send_document(cid, f, caption=Texts['factor_order'])

            markup= InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(Texts['send_receipt'], callback_data='send_receipt'))
            markup.add(InlineKeyboardButton(Texts['back'], callback_data='cancel_main_menu'))
            bot.send_message(cid, f''' مبلغ قابل پرداخت: {total_price:,} تومان
شماره کارت: {card_number}
به نام: {card_name}
 ''', reply_markup= markup)
        else:
            bot.answer_callback_query(call_id, Texts['empty_cart'])

    elif data=='send_receipt':
        bot.answer_callback_query(call_id, Texts['receipt'])
        user_steps[cid]= 'send_receipt'


    


#متن و عکس اول ربات
@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid= message.chat.id
    if len(message.text.split())>1:
        start_value = message.text.split()[1]
        if start_value.startswith('buy'):
            pid = int(start_value.split('_')[-1])
            product_info = get_product_info(pid)
            bot.send_photo(cid, product_info['file_id'], caption=gen_product_caption(pid), reply_markup=gen_product_markup(pid))
            return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(Texts['join_ch'],url='https://t.me/sheida_home', style='primary'))
    markup.add(InlineKeyboardButton(Texts['join'],callback_data= 'be_member', style='success'))    
    with open("images/photo_start.jpg",'rb')as f:
        bot.send_photo(cid , f, caption=Texts['welcome'],reply_markup=markup)


#دسته بندی محصولات
#برگرد کامل کن دکمه هارو 
@bot.message_handler(func=lambda message: message.text=='محصولات')
def products_handler(message):
    products_menu(message.chat.id)
def products_menu(cid):
    markup= InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('لیوان', callback_data='لیوان'), InlineKeyboardButton('ماگ', callback_data='ماگ'),InlineKeyboardButton('دیس', callback_data='دیس'), InlineKeyboardButton('فنجان', callback_data='فنجان'), InlineKeyboardButton('تابه', callback_data='تابه'),InlineKeyboardButton('کاسه', callback_data='کاسه'),InlineKeyboardButton('قابلمه', callback_data='قابلمه'),InlineKeyboardButton('بانکه', callback_data='بانکه'),InlineKeyboardButton('آبگوشت خوری', callback_data='آبگوشت خوری'),InlineKeyboardButton('سایر محصولات', callback_data='سایر محصولات'))
    markup.add(InlineKeyboardButton('💬 جدید ترین محصولات', callback_data='new_product', style='success'))
    markup.add(InlineKeyboardButton(Texts['back'],callback_data='cancel_main_menu', style='primary'))
    bot.send_message(cid,Texts['products_cat'] ,reply_markup=markup)


# دسته بندی محصولات
def category_menu(cid, category):
    products= get_products_cat(category)
    bot.send_message(cid,f'''✔️ شما {category} را انتخاب کردید \n     برای دیدن جزئیات بیشتر محصول مورد نظر را انتخاب کنید: ''')
    for p in products:
        markup= InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(str(products.index(p)+1), callback_data=f"product_{p['id']}"))
        if p== products[-1]:
            markup.add(InlineKeyboardButton(Texts['back'],callback_data='cancel_product', style='primary'))
        bot.send_photo(cid, p['file_id'], reply_markup=markup)


#جدید ترین محصولات
def new_products_menu(cid):
    products= get_new_products()
    bot.send_message(cid, Texts['new_product'])
    for n in products:
        markup= InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(str(products.index(n)+1), callback_data=f"product_{n['id']}"))
        if n== products[-1]:
            markup.add(InlineKeyboardButton(Texts['back'],callback_data='cancel_product', style='primary'))
        bot.send_photo(cid, n['file_id'], reply_markup=markup)
        

# سبدخرید
@bot.message_handler(func=lambda message: message.text=='سبد خرید')
def basket_handler(message):
    basket_menu(message.chat.id)
def basket_menu(cid):
    if cid not in shopping_cart or not shopping_cart[cid]:
        cart= get_cart_shopping(cid)
        if not cart:
            bot.send_message(cid, Texts['basket'])
            return
        item= get_cart_item(cart['id'])
        if not item:
            bot.send_message(cid, Texts['basket'])
            return
        shopping_cart[cid]= dict()
        for i in item:
            shopping_cart[cid].setdefault(i['prod_id'],0)
            shopping_cart[cid][i['prod_id']]+=i['number']
    text= Texts['basket_buy']
    total_p= 0
    total_price=0
    for p in shopping_cart[cid]:
        qty= shopping_cart[cid][p]
        products= get_product_info(p)
        price= int(products['price'])
        total_p += qty
        total_price += price *qty
        text += f'''
{clean_text(products['name'])}
'''
#تعداد: {qty}
    text += clean_text(".............................................")
    text += f"\nتعداد کل: {total_p}\n"
    text += f"قیمت نهایی: {total_price:,} تومان"

    markup= InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(Texts['edit_orders'], callback_data='ویرایش'))
#    markup.add(InlineKeyboardButton('ثبت کد تخفیف 🎟', callback_data='تخفیف'))
    markup.add(InlineKeyboardButton(Texts['gu_factor'], callback_data='سفارش'))
    markup.add(InlineKeyboardButton(Texts['back'],callback_data='cancel_main_menu', style='primary'))
    bot.send_message(cid, text, parse_mode='MarkdownV2' , reply_markup=markup)


# پروفایل
@bot.message_handler(func=lambda message: message.text=='پروفایل')
def profile_handler(message):
    cid= message.chat.id
    show_profile(cid)
def show_profile(cid):
    user= get_users(cid)
    name= user['first_name']
    register= user['register_date']
    phone= user['phone']
    address= user['address']
    if not phone:
        phone= Texts['not_complit']
    if not address:
        address= Texts['not_complit']

    text=f"""اسم 👩👨 : {name}
شناسه کاربری 🪪 : {cid}
شماره موبایل 📞 : {phone}
آدرس 🏠 : {address}
تاریخ عضویت 📅 : {register}
 لطفا اگر اطلاعات تان کامل نیست کامل کنید ‼️
"""
    markup= InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(Texts['edit_information'], callback_data='edit_profile'))
    markup.add(InlineKeyboardButton(Texts['orders_history'], callback_data='order_profile'))
    markup.add(InlineKeyboardButton(Texts['back'], callback_data='cancel_main_menu', style='primary'))    
    bot.send_message(cid, text, reply_markup=markup)

#ویرایش اطلاعات
def edit_profile(cid):
    markup= InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(Texts['edit_name'], callback_data='edit_name'))
    markup.add(InlineKeyboardButton(Texts['edit_phone'], callback_data='edit_phone'))
    markup.add(InlineKeyboardButton(Texts['edit_address'], callback_data='edit_address'))
    markup.add(InlineKeyboardButton(Texts['back'], callback_data='cancel_profile', style='primary'))  
    bot.send_message(cid, Texts['informarion'], reply_markup=markup)  

#ثبت اطلاعات وارد شده 
@bot.message_handler(func=lambda m:user_steps.get(m.chat.id) in ['edit_name','edit_address'])
def edit_profile_handler(message):
    cid= message.chat.id
    steps= user_steps[cid]
    #ذخیره میکند چیزی که کاربر میفرسته
    edits= message.text
    if steps=='edit_name':
        edit_name(cid, edits)
    elif steps=='edit_address':
        edit_address(cid, edits)
    user_steps.pop(cid)
    bot.send_message(cid, Texts['change_ok'])
#گرفتن شماره تلفن
@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    cid= message.chat.id
    phone= message.contact.phone_number
    user_cid= message.contact.user_id
    if user_cid==cid:
        edit_phone(cid,phone)
        user_steps.pop(cid)
        bot.send_message(cid, Texts['change_ok'], reply_markup=ReplyKeyboardRemove())
        main_menu(cid)
    else:
        bot.send_message(cid, Texts['un_phone'])
@bot.message_handler(func=lambda m:m.text=='لغو')
def cancel_phone(message):
    cid=message.chat.id
    user_steps.pop(cid,None)
    bot.send_message(cid,Texts['cancel_text'], reply_markup= ReplyKeyboardRemove())
    main_menu(cid)



# جست و جو محصول
@bot.message_handler(func=lambda message: message.text=='جست و جو محصول')
def search_prodoct(message):
    cid= message.chat.id
    markup= InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(Texts['back'], callback_data='cancel_main_menu', style='primary'))
    bot.send_message(cid, Texts['search'], reply_markup=markup)
    user_steps[cid]= 'search_product'
@bot.message_handler(func=lambda m:user_steps.get(m.chat.id)=='search_product')
def search_pro(message):
    cid= message.chat.id
    products= search_products(message.text)
    if not products:
        bot.send_message(cid, Texts['search_not'])
        main_menu(cid)
        return
    for p in products:
        markup= gen_product_markup(p['id'])
        bot.send_photo(cid, p['file_id'], caption=gen_product_caption(p['id']), reply_markup=markup)
    user_steps.pop(cid)

#درباره ما
@bot.message_handler(func=lambda message: message.text=='درباره ما')
def about_handler(message):
    cid= message.chat.id
    markup= InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(Texts['support'], callback_data='support'))
    markup.add(InlineKeyboardButton(Texts['back'], callback_data='cancel_main_menu', style='primary'))
    sent_m=bot.copy_message(cid, chanel_cid, chanel_m['about_us'])
    bot.edit_message_reply_markup(chat_id=cid, message_id= sent_m.message_id, reply_markup=markup)

# پیگیری سفارش
@bot.message_handler(func=lambda message: message.text=='پیگیری سفارش') 
def order_handler(message):
    cid= message.chat.id
    markup= InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(Texts['back'], callback_data='cancel_main_menu', style='primary'))
    if cid in orders:
        bot.send_message(cid,Texts['order'], reply_markup= markup)
    else:
        bot.send_message(cid, Texts['no_order'],reply_markup=markup)
    
# راهنمای ربات 
@bot.message_handler(func=lambda message: message.text== 'راهنما ربات')
def handel_handler(message):
    cid= message.chat.id
    markup= InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(Texts['gu_add'], callback_data='hendel_basket', style='success'))
    markup.add(InlineKeyboardButton(Texts['gu_search'], callback_data='hendel_search', style='danger'))
    markup.add(InlineKeyboardButton(Texts['gu_order'], callback_data='hendel_order', style='success'))
    markup.add(InlineKeyboardButton(Texts['gu_factor'], callback_data='hendel_saved', style='danger'))
    markup.add(InlineKeyboardButton(Texts['gu_profile'], callback_data='hendel_profile', style='success'))
    markup.add(InlineKeyboardButton(Texts['gu_store'], callback_data='hendel_shop', style='danger'))
    markup.add(InlineKeyboardButton(Texts['gu_invite'], callback_data='hendel_invite', style='success'))
    markup.add(InlineKeyboardButton(Texts['back'], callback_data='cancel_main_menu', style='primary'))
    bot.send_message(cid, Texts['help_robot'], reply_markup=markup)

# دعوت دوستان
@bot.message_handler(func=lambda message: message.text=='دعوت دوستان')
def invite_handler(message):
    cid= message.chat.id
    markup= InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(Texts['back'], callback_data='cancel_main_menu', style='primary'))
    bot.send_message(cid, Texts['link_chanel'], reply_markup=markup)   

#برای پیام های پشتیبانی
@bot.message_handler(func=lambda m:user_steps.get(m.chat.id)=='support')
def handle_support_message(message):
    cid= message.chat.id
    try:
        forwarder= bot.forward_message(admin_cid, cid, message.message_id)#ارسال پیام کاربر برای ادمین
        forward_message[forwarder.message_id]= cid #شماره پیام برای ادمین
        markup= InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(Texts['reply'], callback_data=f'reply_{cid}'))
        bot.send_message(admin_cid, Texts['admin_answer'], reply_markup=markup)
    except:
        bot.copy_message(admin_cid, cid, message.message_id)
        markup= InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(Texts['reply'], callback_data=f'reply_{cid}'))
        bot.send_message(admin_cid, Texts['admin_answer'], reply_markup=markup)

    bot.send_message(cid, Texts['forward_su'])
    user_steps.pop(cid)

#اضافه کردن محصول 
@bot.message_handler(commands=['add_product'])
def command_add_product_handler(message):
    cid = message.chat.id
    if is_spam(cid): return
    if cid == admin_cid:
        bot.send_message(cid, Texts['add_product'])
        user_steps[cid] = 'AP'
    else:
        echo_message(message)


#ادمین میفرسته محصول را در دیتابیس و کانال میفرسته
@bot.message_handler(content_types=['photo'])
def content_photo_handler(message):
    cid = message.chat.id
    if is_spam(cid): return
    file_id = message.photo[-1].file_id
    if user_steps.get(cid) == 'AP':
        caption = message.caption
        product_parts = caption.split('\n')
        product_name = product_parts[0].split(':', 1)[1]
        product_desc = product_parts[1].split(':', 1)[1]
        product_price = product_parts[2].split(':', 1)[1]
        product_inventory = product_parts[3].split(':', 1)[1]
        product_category = product_parts[4].split(':',1)[1]
        pid = insert_product_data(name=product_name, price=product_price, inventory=product_inventory, description=product_desc, file_id=file_id, category= product_category)
        if pid:
            bot.send_message(cid, f'product inserted at ID: {pid}\nname: {product_name}, desc: {product_desc}, price: {product_price}, inv: {product_inventory}')
            bot.send_photo(chanel_store, file_id, caption=gen_channel_product_caption(pid), parse_mode='MarkdownV2')
    elif user_steps.get(cid)=='send_receipt':
        orders[cid]=True
        bot.send_photo(chanel_cid, file_id, caption='''
رسید جدید =>
نام کاربر : {message.from_user.first_name}
شناسه کاربر: {cid}
بررسی کنید برای درستی فاکتور
''')
        bot.send_message(cid, Texts['check_receipt'])
        user_steps.pop(cid)


#گرفتن جواب ادمین 
@bot.message_handler(func=lambda m:user_steps.get(m.chat.id,'').startswith('reply_'))
def send_answer(message):
    cid= message.chat.id
    id_user= user_steps[cid].split('_')[1]
    bot.send_message(id_user, message.text)
    bot.send_message(cid,Texts['answer_su'])
    user_steps.pop(cid)

#هندلر برای ادمین
@bot.message_handler(func=lambda m:m.chat.id==admin_cid and m.reply_to_message)
def admin_reply(message):
    try:
        user_id =message.reply_to_message.forward_from.id
        bot.send_message(user_id, message.text)
        bot.send_message(admin_cid, Texts['answer'])
    except:
        bot.send_message(admin_cid, Texts['close_forward'])


#ارسال عکس محصولاتی که در database ولی در کانال نیست
#product= get_product_info(39)
#bot.send_photo(chanel_store, product['file_id'], caption= gen_channel_product_caption(39), parse_mode='MarkdownV2')

# هرچی بزنی همان را نشان میدهد
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)
# فقط پیام آخر را جواب میده
bot.infinity_polling(skip_pending=True)
