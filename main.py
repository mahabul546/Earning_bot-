import telebot
from telebot import types
from datetime import datetime
import json

BOT_TOKEN = "8822168901:AAFR12UNn-dqcNLd8q2HzGaWx5wybxyUGIs"
ADMIN_ID = 7834320405 # তোমার আইডি
bot = telebot.TeleBot(BOT_TOKEN)

# ডাটা সেভ
try:
    with open('users.json','r') as f:
        users_db = json.load(f)
except:
    users_db = {}

def save_db():
    with open('users.json','w') as f:
        json.dump(users_db, f)

# 1) START - পেন্ডিং সিস্টেম
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    args = message.text.split()
    referrer_id = args[1] if len(args) > 1 else None

    if user_id not in users_db:
        users_db[user_id] = {
            'name': message.from_user.first_name,
            'balance': 0,
            'referrals': [],
            'withdraw_referrals': 0,
            'withdraws': [],
            'is_pending': True,
            'referred_by': referrer_id
        }
        if referrer_id and referrer_id in users_db and referrer_id!= user_id:
            if user_id not in users_db[referrer_id]['referrals']:
                users_db[referrer_id]['referrals'].append(user_id)
        save_db()

        # ইউজারকে পেন্ডিং পোস্ট
        bot.send_message(message.chat.id, "⏳ আপনার রিকোয়েস্ট পেন্ডিং এ আছে\nএকটু অপেক্ষা করুন, এডমিন ফ্রী হয়ে অ্যাপ্রুভ করবে।")

        # তোমার কাছে নোটিস + Approve বাটন
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Approve করুন", callback_data=f"approve_{user_id}"))
        bot.send_message(ADMIN_ID, f"🔔 নতুন ইউজার পেন্ডিং\n👤 নাম: {message.from_user.first_name}\n🆔 ID: {user_id}\n\nদয়া করে অ্যাপ্রুভ করুন", reply_markup=markup)
        return

    # যদি already approved হয় তাহলে মেনু দেখাবে
    if not users_db[user_id].get('is_pending', False):
        show_main_menu(message.chat.id)

# 2) 6 টা মেইন বাটন
def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👥 My Referrals", "🎯 Tasks")
    markup.add("💰 Balance", "📢 Notice")
    markup.add("💬 Support", "⚙️ Admin Panel")
    bot.send_message(chat_id, "🏠 Main Menu", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("approve_"))
def approve_user(call):
    if call.from_user.id!= ADMIN_ID: return
    uid = call.data.split("_")[1]
    if uid in users_db:
        users_db[uid]['is_pending'] = False
        save_db()
        bot.send_message(int(uid), "✅ আপনার একাউন্ট অ্যাপ্রুভ হয়েছে!")
        bot.send_message(call.message.chat.id, f"✅ {users_db[uid]['name']} কে অ্যাপ্রুভ করা হলো")
        show_main_menu(int(uid))

@bot.message_handler(func=lambda m: m.text == "👥 My Referrals")
def referrals(message):
    uid = str(message.from_user.id)
    user = users_db.get(uid)
    total = len(user['referrals'])
    w_ref = user['withdraw_referrals']
    link = f"https://t.me/{bot.get_me().username}?start={uid}"

    text = f"""💸 রেফার করে অটোমেটিক ইনকাম করুন
বিঃদ্রঃ প্রতি রেফার 20 টাকা করে পাবেন

👥 Total Referral: {total}
💵 Withdraw Referral: {w_ref}

🔗 Your Referral Link:
{link}"""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Back to menu", callback_data="back_menu"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

# 4) Tasks - 6 টা বাটন
@bot.message_handler(func=lambda m: m.text == "🎯 Tasks")
def tasks_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📧 Gmail sell", callback_data="task_gmail"),
        types.InlineKeyboardButton("📱 Whatsapp sell", callback_data="task_wp"),
        types.InlineKeyboardButton("🎬 Videos earn", callback_data="task_video"),
        types.InlineKeyboardButton("▶️ YouTube", callback_data="task_yt"),
        types.InlineKeyboardButton("🌐 Website visit", callback_data="task_web"),
        types.InlineKeyboardButton("🎵 TikTok top", callback_data="task_tiktok")
    )
    markup.add(types.InlineKeyboardButton("🔙 Back to menu", callback_data="back_menu"))
    bot.send_message(message.chat.id, "🎯 Task Menu:", reply_markup=markup)

# 5) Balance
@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance(message):
    uid = str(message.from_user.id)
    bal = users_db[uid]['balance']
    text = f"""বিঃদ্রঃ উইথড্র দেওয়ার 2 ঘণ্টার মধ্যে পেমেন্ট দেয়া হবে

💰 আপনার ব্যালেন্স: {bal} টাকা
💵 মিনিমাম উইথড্র: 100 টাকা"""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💸 Payout", callback_data="payout"))
    markup.add(types.InlineKeyboardButton("👤 My Accounts", callback_data="my_account"))
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="back_menu"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

# 7) My Account - 00 থেকে শুরু
@bot.callback_query_handler(func=lambda c: c.data == "my_account")
def my_account(call):
    uid = str(call.from_user.id)
    user = users_db[uid]
    withdraws = user['withdraws']
    pending = sum([w['amount'] for w in withdraws if w['status'] == 'pending'])
    pending_show = "00" if pending == 0 else str(pending)

    if not withdraws:
        history = "কোনো হিস্টরি নেই"
    else:
        history = ""
        for i, w in enumerate(reversed(withdraws), 1):
            history += f"{i}. {w['amount']}৳ - {w['status'].upper()}\n📱 {w['method']} : {w['number']}\n📅 {w['date']} | ⏰ {w['time']}\n\n"

    text = f"""👤 MY ACCOUNT

⏳ পেন্ডিং ব্যালেন্স: {pending_show} টাকা
🔄 মোট উইথড্র: {len(withdraws)} বার

📜 উইথড্র হিস্টরি:
{history}"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

# 6) Payout - 3 টা বাটন
@bot.callback_query_handler(func=lambda c: c.data == "payout")
def payout(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Bkash", callback_data="wd_bkash"))
    markup.add(types.InlineKeyboardButton("Nagad", callback_data="wd_nagad"))
    markup.add(types.InlineKeyboardButton("Rocket", callback_data="wd_rocket"))
    bot.edit_message_text("💳 মেথড সিলেক্ট করুন:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("wd_"))
def ask_amount(call):
    method = call.data.split("_")[1]
    bot.send_message(call.message.chat.id, f"💰 {method} এর জন্য টাকার পরিমাণ লিখুন (মিনিমাম 100):")
    bot.register_next_step_handler(call.message, lambda m: ask_number(m, method))

def ask_number(message, method):
    uid = str(message.from_user.id)
    try:
        amount = int(message.text)
        if amount < 100:
            bot.send_message(message.chat.id, "❌ 100 টাকার নিচে উইথড্র হবে না!")
            return
        if amount > users_db[uid]['balance']:
            bot.send_message(message.chat.id, "❌ ব্যালেন্স কম আছে!")
            return
        bot.send_message(message.chat.id, f"📱 আপনার {method} নাম্বার দিন:")
        bot.register_next_step_handler(message, lambda m: do_withdraw(m, method, amount))
    except:
        bot.send_message(message.chat.id, "❌ সঠিক সংখ্যা দিন")

def do_withdraw(message, method, amount):
    uid = str(message.from_user.id)
    now = datetime.now()

    # ব্যালেন্স কাটা
    users_db[uid]['balance'] -= amount
    data = {
        'amount': amount,
        'method': method,
        'number': message.text,
        'status': 'pending',
        'date': now.strftime("%d/%m/%Y"),
        'time': now.strftime("%I:%M %p")
    }
    users_db[uid]['withdraws'].append(data)

    # রেফার বোনাস 20 টাকা
    ref_id = users_db[uid].get('referred_by')
    if ref_id and ref_id in users_db:
        users_db[ref_id]['balance'] += 20
        users_db[ref_id]['withdraw_referrals'] += 1
        bot.send_message(int(ref_id), "🎉 আপনি 20 টাকা রেফার বোনাস পেয়েছেন!")
        bot.send_message(ADMIN_ID, f"💸 {users_db[ref_id]['name']} 20 টাকা বোনাস পেয়েছে (রেফার: {users_db[uid]['name']})")

    save_db()
    bot.send_message(message.chat.id, f"✅ {amount} টাকা উইথড্র রিকোয়েস্ট পেন্ডিং এ গেছে!")
    bot.send_message(ADMIN_ID, f"🔔 নতুন উইথড্র\n👤 {users_db[uid]['name']}\n💰 {amount}৳\n📱 {method}: {message.text}")

# Admin Panel - শুধু তুমি দেখবে
@bot.message_handler(func=lambda m: m.text == "⚙️ Admin Panel")
def admin_panel(message):
    if message.from_user.id!= ADMIN_ID:
        bot.send_message(message.chat.id, "❌ আপনি এডমিন না!")
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👥 All Users", callback_data="all_users"))
    bot.send_message(message.chat.id, "⚙️ Admin Panel", reply_markup=markup)

bot.infinity_polling()
