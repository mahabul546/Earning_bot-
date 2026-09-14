from flask import Flask
import threading
import os
from datetime import datetime
import json
from telebot import types
import telebot

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Running!"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
threading.Thread(target=run_flask).start()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7834320405
CHANNEL_USERNAME = "@mhabul546"
bot = telebot.TeleBot(BOT_TOKEN)

# --- DATABASE ---
try:
    with open('users.json','r') as f:
        users_db = json.load(f)
except:
    users_db = {}

try:
    with open('notice.json','r') as f:
        notice_data = json.load(f)
except:
    notice_data = {"text": "💰 পেমেন্ট পাওয়ার নিয়ম\n📱 Telegram: https://t.me/mhabul546\n▶️ YouTube: https://youtube.com/@mahabul546"}

def save_db():
    with open('users.json','w') as f:
        json.dump(users_db, f)

def save_notice():
    with open('notice.json','w') as f:
        json.dump(notice_data, f)

# --- MENU ---
def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👥 My Referrals", "🎯 Tasks")
    markup.add("💰 Balance", "📢 Notice")
    markup.add("💬 Support", "⚙️ Admin Panel")
    bot.send_message(chat_id, "🏠 Main Menu", reply_markup=markup)

def is_admin(uid):
    return int(uid) == ADMIN_ID

# 1. START & PENDING
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.from_user.id)
    args = message.text.split()
    ref = args[1] if len(args)>1 else None

    if uid not in users_db:
        users_db[uid] = {
            'name': message.from_user.first_name,
            'username': message.from_user.username,
            'balance': 0,
            'referrals': [],
            'withdraw_referrals': 0,
            'withdraws': [],
            'is_pending': True,
            'referred_by': ref,
            'pending_balance': 0
        }
        # রেফার লিস্টে এড
        if ref and ref in users_db:
            if uid not in users_db[ref]['referrals']:
                users_db[ref]['referrals'].append(uid)

        save_db()
        bot.send_message(message.chat.id, "⏳ আপনার রিকোয়েস্ট পেন্ডিং এ আছে একটু অপেক্ষা করুন এডমিন ফ্রী হয়ে অপ্রভ করবে।")
        mk = types.InlineKeyboardMarkup()
        mk.add(types.InlineKeyboardButton("✅ Approve করুন", callback_data=f"approve_{uid}"))
        bot.send_message(ADMIN_ID, f"🔔 নতুন পেন্ডিং রিকোয়েস্ট\n👤 নাম: {message.from_user.first_name}\n🆔 ID: {uid}\n🔗 @{message.from_user.username}\n\nদয়া করে আপ্রভ করুন।", reply_markup=mk)
        return

    if users_db[uid]['is_pending']:
        bot.send_message(message.chat.id, "⏳ আপনার রিকোয়েস্ট পেন্ডিং এ আছে একটু অপেক্ষা করুন এডমিন ফ্রী হয়ে অপ্রভ করবে।")
    else:
        show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith("approve_"))
def approve_user(call):
    if not is_admin(call.from_user.id):
        return
    uid = call.data.split("_")[1]
    if uid in users_db:
        users_db[uid]['is_pending']=False
        save_db()
        bot.send_message(int(uid), "✅ আপনার একাউন্ট অ্যাপ্রুভ হয়েছে! এখন কাজ শুরু করুন।")
        show_main_menu(int(uid))
        bot.edit_message_text(f"✅ {uid} কে Approve করা হয়েছে", call.message.chat.id, call.message.message_id)

# 2 & 3. REFERRALS
@bot.message_handler(func=lambda m: m.text == "👥 My Referrals")
def referrals(message):
    uid = str(message.from_user.id)
    user = users_db.get(uid)
    if not user or user['is_pending']:
        return
    link = f"https://t.me/{bot.get_me().username}?start={uid}"
    text = f"💸 রেফার করে অটোমেটিক ইনকাম করুন\n\n💰 বিঃদ্রঃ প্রতি রেফার 20 টাকা করে পাবেন\n\n👥 Total Referral : {len(user['referrals'])}\n💵 Withdraw Referral : {user['withdraw_referrals']}\n\n🔗 Your Referral link:\n{link}\n\n⚠️ রেফার করা ইউজার withdraw করলে Withdraw Referral বাড়বে।"
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mk.add("🔙 Back to menu")
    bot.send_message(message.chat.id, text, reply_markup=mk)

# 4. TASKS
@bot.message_handler(func=lambda m: m.text == "🎯 Tasks")
def tasks_menu(message):
    uid = str(message.from_user.id)
    if users_db[uid]['is_pending']:
        return
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mk.add("📧 Gmail sell", "📱 Whatsapp sell")
    mk.add("🎬 Videos earn", "▶️ YouTube")
    mk.add("🌐 Website visit", "🎵 TikTok top")
    mk.add("🔙 Back to menu")
    bot.send_message(message.chat.id, "🎯 Tasks Menu - যেকোনো একটিতে চাপ দিন", reply_markup=mk)

# --- UPDATED TASKS SECTION ---
@bot.message_handler(func=lambda m: m.text == "📧 Gmail sell")
def gmail_sell(m):
    text = """📧 Gmail Sell - প্রতিদিন 200 থেকে 300 টাকা ইনকাম করুন সম্পূর্ণ ফ্রিতে

💰 3 টা Gmail = 50 টাকা

🎬 কিভাবে জিমেইল সেল দিবেন তার ভিডিও:
👉 https://youtu.be/xhf71sQl57Y?si=tYCHM0oQZZaZ5oT9

💸 কিভাবে উইথড্র করবেন তার ভিডিও:
👉 https://youtu.be/xhf71sQl57Y?si=tYCHM0oQZZaZ5oT9"""

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💰 সেল দেওয়ার লিংক", url="https://t.me/GmailFarmerBot?start=7834320405"))
    markup.add(types.InlineKeyboardButton("🎬 সেল করার ভিডিও", url="https://youtu.be/xhf71sQl57Y?si=tYCHM0oQZZaZ5oT9"))
    markup.add(types.InlineKeyboardButton("💵 উইথড্র ভিডিও", url="https://youtu.be/xhf71sQl57Y?si=tYCHM0oQZZaZ5oT9"))
    bot.send_message(m.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["📱 Whatsapp sell", "🎬 Videos earn", "▶️ YouTube", "🌐 Website visit", "🎵 TikTok top"])
def other_tasks(m):
    bot.send_message(m.chat.id, f"⏳ {m.text}\n\nএকটু অপেক্ষা করুন অতি তাড়াতাড়ি কাজ চলে আসবে।")

# 5. BALANCE
@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance_menu(message):
    uid = str(message.from_user.id)
    user = users_db[uid]
    if user['is_pending']:
        return
    text = f"💰 বিঃদ্রঃ উইথড্র দেওয়া 2 ঘণ্টার মধ্যে পেমেন্ট দেয়া হবে\n\n💵 আপনার ব্যালেন্স: {user['balance']} টাকা\n💸 মিনিম্যাম উইথড্র: 100 টাকা\n\n100 টাকার নিচে কেও withdraw করতে পারবে না।"
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mk.add("💸 Payout", "👤 My accounts")
    mk.add("🔙 Back to menu")
    bot.send_message(message.chat.id, text, reply_markup=mk)

@bot.message_handler(func=lambda m: m.text == "👤 My accounts")
def my_accounts(message):
    uid = str(message.from_user.id); user = users_db[uid]
    if not user['withdraws']:
        history = "কোনো হিস্টরি নেই"
    else:
        history = ""
        for i, w in enumerate(user['withdraws'][-5:], 1):
            history += f"{i}. {w['amount']}৳ - {w['status']}\n📱 {w['method']} : {w['number']}\n📅 {w['date']} | ⏰ {w['time']}\n\n"
    text = f"👤 MY ACCOUNT\n⏳ পেন্ডিং ব্যালেন্স: {user.get('pending_balance',0)} টাকা\n🔄 মোট উইথড্র: {len(user['withdraws'])} বার\n\n📜 উইথড্র হিস্টরি:\n{history}"
    bot.send_message(message.chat.id, text)

# 6. PAYOUT
@bot.message_handler(func=lambda m: m.text == "💸 Payout")
def payout_menu(message):
    uid = str(message.from_user.id)
    if users_db[uid]['balance'] < 100:
        bot.send_message(message.chat.id, f"❌ আপনার ব্যালেন্স {users_db[uid]['balance']} টাকা। 100 টাকার নিচে withdraw হবে না।")
        return
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mk.add("📱 Bkash", "💵 Nagad", "🚀 Rocket")
    mk.add("🔙 Back to menu")
    bot.send_message(message.chat.id, "💳 পেমেন্ট মেথড সিলেক্ট করুন:", reply_markup=mk)

@bot.message_handler(func=lambda m: m.text in ["📱 Bkash", "💵 Nagad", "🚀 Rocket"])
def ask_number(message):
    bot.send_message(message.chat.id, f"আপনার {message.text} নাম্বার দিন:")
    bot.register_next_step_handler(message, process_withdraw, message.text)

def process_withdraw(message, method):
    uid = str(message.from_user.id)
    user = users_db[uid]
    amount = user['balance']
    if amount < 100:
        return
    number = message.text
    now = datetime.now()
    user['balance'] = 0
    user['pending_balance'] = amount
    withdraw_info = {
        'amount': amount, 'method': method, 'number': number,
        'status': 'PENDING', 'date': now.strftime("%d/%m/%Y"),
        'time': now.strftime("%I:%M %p")
    }
    user['withdraws'].append(withdraw_info)
    ref_id = user.get('referred_by')
    if ref_id and ref_id in users_db:
        users_db[ref_id]['balance'] += 20
        users_db[ref_id]['withdraw_referrals'] += 1
        try:
            bot.send_message(int(ref_id), f"🎉 আপনি 20 টাকা রেফার বোনাস পেয়েছেন! {user['name']} withdraw করেছে।")
        except:
            pass
    save_db()
    bot.send_message(message.chat.id, f"✅ {amount}৳ withdraw রিকোয়েস্ট পাঠানো হয়েছে!\n{method}: {number}", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("🔙 Back to menu"))
    bot.send_message(ADMIN_ID, f"💰 নতুন Withdraw\n👤 {user['name']} ({uid})\n💵 {amount}৳\n📱 {method}: {number}")

@bot.message_handler(func=lambda m: m.text == "📢 Notice")
def notice(m):
    bot.send_message(m.chat.id, notice_data['text'])

@bot.message_handler(func=lambda m: m.text == "💬 Support")
def support(m):
    bot.send_message(m.chat.id, "💬 Support: @mhabul546")

@bot.message_handler(func=lambda m: m.text == "⚙️ Admin Panel")
def admin_panel(m):
    if not is_admin(m.from_user.id):
        bot.send_message(m.chat.id, "❌ এই প্যানেল শুধু এডমিনের জন্য!")
        return
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mk.add("📊 Total Users", "📢 Set Notice")
    mk.add("🔙 Back to menu")
    bot.send_message(m.chat.id, "⚙️ Admin Panel", reply_markup=mk)

@bot.message_handler(func=lambda m: m.text == "🔙 Back to menu")
def back(m):
    show_main_menu(m.chat.id)

@bot.message_handler(func=lambda m: m.text == "📊 Total Users")
def total_users(m):
    if not is_admin(m.from_user.id):
        return
    bot.send_message(m.chat.id, f"📊 Total Users: {len(users_db)}")

print("Bot is running...")
bot.infinity_polling()
