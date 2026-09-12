import telebot
from telebot import types
from datetime import datetime
import json

BOT_TOKEN ="8822168901:AAFR12UNn-dqcNLd8q2HzGaWx5wybxyUGIs"
ADMIN_ID = 7834320405
CHANNEL_USERNAME = "@mhabul546"
NOTICE_FILE = "notice.json"

bot = telebot.TeleBot(BOT_TOKEN)

TASKS = {
    "task_gmail": {"name": "📧 Gmail sell", "reward": 15, "link": "https://google.com", "desc": "Gmail সেল করতে সাপোর্টে মেসেজ দিন"},
    "task_wp": {"name": "📱 Whatsapp sell", "reward": 20, "link": "https://whatsapp.com", "desc": "Whatsapp সেল করতে মেসেজ দিন"},
    "task_video": {"name": "🎬 Videos earn", "reward": 5, "link": "https://youtube.com/@mahabul546", "desc": "ভিডিও ১ মিনিট দেখুন"},
    "task_yt": {"name": "▶️ YouTube", "reward": 10, "link": "https://youtube.com/@mahabul546?si=Vy6Zhd1l1P8jeNfJ", "desc": "চ্যানেল সাবস্ক্রাইব করুন"},
    "task_web": {"name": "🌐 Website visit", "reward": 3, "link": "https://google.com", "desc": "ওয়েবসাইট ভিজিট করুন"},
    "task_tiktok": {"name": "🎵 TikTok top", "reward": 8, "link": "https://tiktok.com", "desc": "TikTok ফলো করুন"}
}

try:
    with open('users.json','r') as f: users_db = json.load(f)
except: users_db = {}
try:
    with open(NOTICE_FILE,'r') as f: notice_data = json.load(f)
except: notice_data = {"text": "💰 পেমেন্ট পাওয়ার নিয়ম\nপেমেন্ট পেতে হলে নিচের ২টি চ্যানেলেই জয়েন/সাবস্ক্রাইব করা বাধ্যতামূলক 👇\n📱 Telegram: https://t.me/mhabul546\n▶️ YouTube: https://youtube.com/@mahabul546\n⚠️ জয়েন না থাকলে পেমেন্ট দেওয়া হবে না।"}

def save_db():
    with open('users.json','w') as f: json.dump(users_db, f)
def save_notice():
    with open(NOTICE_FILE,'w') as f: json.dump(notice_data, f)

def is_joined(user_id):
    try:
        m = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return m.status in ['member','administrator','creator']
    except: return True

def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👥 My Referrals", "🎯 Tasks")
    markup.add("💰 Balance", "📢 Notice")
    markup.add("💬 Support", "⚙️ Admin Panel")
    bot.send_message(chat_id, "🏠 Main Menu", reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.from_user.id)
    args = message.text.split()
    ref = args[1] if len(args)>1 else None
    if uid not in users_db:
        users_db[uid] = {'name': message.from_user.first_name, 'balance': 0, 'referrals': [], 'withdraw_referrals': 0, 'withdraws': [], 'is_pending': True, 'referred_by': ref, 'completed_tasks': []}
        if ref and ref in users_db and ref!= uid:
            if uid not in users_db[ref]['referrals']: users_db[ref]['referrals'].append(uid)
        save_db()
        bot.send_message(message.chat.id, "⏳ আপনার রিকোয়েস্ট পেন্ডিং এ আছে")
        mk = types.InlineKeyboardMarkup()
        mk.add(types.InlineKeyboardButton("✅ Approve করুন", callback_data=f"approve_{uid}"))
        bot.send_message(ADMIN_ID, f"🔔 নতুন ইউজার\n👤 {message.from_user.first_name}\n🆔 {uid}", reply_markup=mk)
        return
    if not users_db[uid].get('is_pending', False): show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith("approve_"))
def approve_user(call):
    if call.from_user.id!= ADMIN_ID: return
    uid = call.data.split("_")[1]
    if uid in users_db:
        users_db[uid]['is_pending']=False; save_db()
        bot.send_message(int(uid), "✅ আপনার একাউন্ট অ্যাপ্রুভ হয়েছে!")
        show_main_menu(int(uid))
        bot.answer_callback_query(call.id, "Approved")

@bot.message_handler(func=lambda m: m.text == "👥 My Referrals")
def referrals(message):
    uid = str(message.from_user.id); user = users_db.get(uid)
    link = f"https://t.me/{bot.get_me().username}?start={uid}"
    text = f"💸 রেফার করে অটোমেটিক ইনকাম করুন\nপ্রতি রেফার 20 টাকা\n\n👥 Total Referral: {len(user['referrals'])}\n💵 Withdraw Referral: {user['withdraw_referrals']}\n\n🔗 Link: {link}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "🎯 Tasks")
def tasks_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for tid, info in TASKS.items():
        markup.add(types.InlineKeyboardButton(f"{info['name']} - {info['reward']}৳", callback_data=tid))
    bot.send_message(message.chat.id, "🎯 Task Menu:", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data in TASKS)
def show_task(call):
    task = TASKS[call.data]; uid = str(call.from_user.id)
    if call.data in users_db[uid].get('completed_tasks', []):
        bot.answer_callback_query(call.id, "❌ এই টাস্ক আগেই করেছেন!"); return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Link Open", url=task['link']))
    markup.add(types.InlineKeyboardButton(f"✅ Claim {task['reward']}৳", callback_data=f"claim_{call.data}"))
    bot.edit_message_text(f"{task['name']}\n\n{task['desc']}\n💰 Reward: {task['reward']}৳", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("claim_"))
def claim_task(call):
    task_id = call.data.replace("claim_", ""); uid = str(call.from_user.id)
    if task_id in users_db[uid]['completed_tasks']: return
    reward = TASKS[task_id]['reward']
    users_db[uid]['balance']+=reward; users_db[uid]['completed_tasks'].append(task_id); save_db()
    bot.answer_callback_query(call.id, f"✅ {reward}৳ পেয়েছেন!")
    bot.send_message(call.message.chat.id, f"🎉 {reward}৳ যোগ হয়েছে!")

@bot.message_handler(func=lambda m: m.text == "📢 Notice")
def notice(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📱 Telegram Join", url="https://t.me/mhabul546"))
    markup.add(types.InlineKeyboardButton("▶️ YouTube Subscribe", url="https://youtube.com/@mahabul546"))
    bot.send_message(message.chat.id, notice_data["text"], reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance(message):
    bal = users_db[str(message.from_user.id)]['balance']
    text = f"বিঃদ্রঃ উইথড্র 2 ঘণ্টার মধ্যে পেমেন্ট\n\n💰 ব্যালেন্স: {bal} টাকা\n💵 মিনিমাম: 100 টাকা"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💸 Payout", callback_data="payout"))
    markup.add(types.InlineKeyboardButton("👤 My Accounts", callback_data="my_account"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "my_account")
def my_account(call):
    withdraws = users_db[str(call.from_user.id)]['withdraws']
    pending = sum([w['amount'] for w in withdraws if w['status']=='pending'])
    pending_show = "00" if pending==0 else str(pending)
    if not withdraws: history="কোনো হিস্টরি নেই"
    else:
        history=""
        for i,w in enumerate(reversed(withdraws),1):
            history+=f"{i}. {w['amount']}৳ - {w['status'].upper()}\n📱 {w['method']} : {w['number']}\n📅 {w['date']} | ⏰ {w['time']}\n\n"
    bot.send_message(call.message.chat.id, f"👤 MY ACCOUNT\n⏳ পেন্ডিং: {pending_show}৳\n🔄 মোট: {len(withdraws)} বার\n\n{history}")

@bot.callback_query_handler(func=lambda c: c.data == "payout")
def payout(call):
    if not is_joined(call.from_user.id):
        mk = types.InlineKeyboardMarkup()
        mk.add(types.InlineKeyboardButton("📱 Telegram Join", url="https://t.me/mhabul546"))
        mk.add(types.InlineKeyboardButton("▶️ YouTube", url="https://youtube.com/@mahabul546"))
        mk.add(types.InlineKeyboardButton("✅ জয়েন করেছি, চেক করুন", callback_data="check_join"))
        bot.edit_message_text("❌ পেমেন্ট নিতে হলে আগে ২ টা চ্যানেলে জয়েন করতে হবে!", call.message.chat.id, call.message.message_id, reply_markup=mk); return
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("Bkash", callback_data="wd_bkash"), types.InlineKeyboardButton("Nagad", callback_data="wd_nagad"))
    mk.add(types.InlineKeyboardButton("Rocket", callback_data="wd_rocket"))
    bot.edit_message_text("💳 মেথড সিলেক্ট করুন:", call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data == "check_join")
def check_join(call):
    if is_joined(call.from_user.id):
        mk = types.InlineKeyboardMarkup()
        mk.add(types.InlineKeyboardButton("Bkash", callback_data="wd_bkash"), types.InlineKeyboardButton("Nagad", callback_data="wd_nagad"))
        mk.add(types.InlineKeyboardButton("Rocket", callback_data="wd_rocket"))
        bot.edit_message_text("✅ জয়েন কনফার্ম! মেথড সিলেক্ট করুন:", call.message.chat.id, call.message.message_id, reply_markup=mk)
    else: bot.answer_callback_query(call.id, "❌ এখনো জয়েন করেননি!", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data.startswith("wd_") and not c.data.startswith("wd_approve") and not c.data.startswith("wd_reject"))
def ask_amount(call):
    method = call.data.split("_")[1]
    bot.send_message(call.message.chat.id, f"💰 {method} এর জন্য টাকা লিখুন (100+):")
    bot.register_next_step_handler(call.message, lambda m: ask_number(m, method))

def ask_number(message, method):
    uid=str(message.from_user.id)
    try:
        amount=int(message.text)
        if amount<100 or amount>users_db[uid]['balance']:
            bot.send_message(message.chat.id, "❌ ব্যালেন্স কম বা 100 এর নিচে"); return
        bot.send_message(message.chat.id, f"📱 আপনার {method} নাম্বার দিন:")
        bot.register_next_step_handler(message, lambda m: do_withdraw(m, method, amount))
    except: bot.send_message(message.chat.id, "❌ সংখ্যা দিন")

def do_withdraw(message, method, amount):
    uid=str(message.from_user.id); now=datetime.now()
    users_db[uid]['balance']-=amount
    users_db[uid]['withdraws'].append({'amount': amount, 'method': method, 'number': message.text, 'status': 'pending', 'date': now.strftime("%d/%m/%Y"), 'time': now.strftime("%I:%M %p")})
    ref_id = users_db[uid].get('referred_by')
    if ref_id and ref_id in users_db:
        users_db[ref_id]['balance']+=20; users_db[ref_id]['withdraw_referrals']+=1
        bot.send_message(int(ref_id), "🎉 20 টাকা রেফার বোনাস পেয়েছেন!")
    save_db()
    bot.send_message(message.chat.id, f"✅ {amount}৳ পেন্ডিং!")
    mk=types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("✅ Approve", callback_data=f"wd_approve_{uid}_{len(users_db[uid]['withdraws'])-1}"), types.InlineKeyboardButton("❌ Reject", callback_data=f"wd_reject_{uid}_{len(users_db[uid]['withdraws'])-1}"))
    bot.send_message(ADMIN_ID, f"🔔 নতুন উইথড্র\n👤 {users_db[uid]['name']} {uid}\n💰 {amount}৳ {method} {message.text}", reply_markup=mk)

# ================= ADMIN PANEL PRO =================
@bot.message_handler(func=lambda m: m.text == "⚙️ Admin Panel")
def admin_panel(message):
    if message.from_user.id!= ADMIN_ID: bot.send_message(message.chat.id, "❌ এডমিন না!"); return
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mk.add("📊 Stats", "👥 Total Users")
    mk.add("📋 Refer List", "💸 Withdraw List")
    mk.add("💰 Balances", "🔍 Search User")
    mk.add("📢 Edit Notice", "🏠 Main Menu")
    bot.send_message(message.chat.id, "⚙️ Pro Admin Panel", reply_markup=mk)

@bot.message_handler(func=lambda m: m.text in ["📊 Stats", "👥 Total Users", "📋 Refer List", "💸 Withdraw List", "💰 Balances", "🔍 Search User", "📢 Edit Notice", "🏠 Main Menu"])
def admin_actions(message):
    if message.from_user.id!= ADMIN_ID: return
    if message.text=="🏠 Main Menu": show_main_menu(message.chat.id); return
    if message.text=="📊 Stats":
        total_bal=sum([u['balance'] for u in users_db.values()]); total_wd=sum([len(u['withdraws']) for u in users_db.values()])
        bot.send_message(message.chat.id, f"📊 Stats\n👥 Users: {len(users_db)}\n💰 Total Balance: {total_bal}৳\n💸 Total Withdraw: {total_wd}")
    elif message.text=="👥 Total Users":
        txt="👥 Last 20 Users:\n"
        for uid,u in list(users_db.items())[-20:]: txt+=f"{u['name']} {uid} {u['balance']}৳\n"
        bot.send_message(message.chat.id, txt)
    elif message.text=="📋 Refer List":
        sorted_users=sorted(users_db.items(), key=lambda x: len(x[1]['referrals']), reverse=True)[:15]
        txt="📋 Top Referrers:\n"
        for uid,u in sorted_users: txt+=f"{u['name']} {uid}: {len(u['referrals'])} ref\n"
        bot.send_message(message.chat.id, txt)
    elif message.text=="💸 Withdraw List":
        pending=[]
        for uid,u in users_db.items():
            for idx,wd in enumerate(u['withdraws']):
                if wd['status']=='pending': pending.append((uid,u,idx,wd))
        if not pending: bot.send_message(message.chat.id, "কোনো পেন্ডিং নেই"); return
        for uid,u,idx,wd in pending[-10:]:
            mk=types.InlineKeyboardMarkup()
            mk.add(types.InlineKeyboardButton("✅ Approve", callback_data=f"wd_approve_{uid}_{idx}"), types.InlineKeyboardButton("❌ Reject", callback_data=f"wd_reject_{uid}_{idx}"))
            bot.send_message(message.chat.id, f"💸 {wd['amount']}৳\n👤 {u['name']} {uid}\n📱 {wd['method']} {wd['number']}", reply_markup=mk)
    elif message.text=="💰 Balances":
        sorted_bal=sorted(users_db.items(), key=lambda x: x[1]['balance'], reverse=True)[:20]
        txt="💰 Top Balances:\n"
        for uid,u in sorted_bal: txt+=f"{u['name']} {uid}: {u['balance']}৳\n"
        bot.send_message(message.chat.id, txt)
    elif message.text=="🔍 Search User":
        bot.send_message(message.chat.id, "🔍 ইউজারের ID দিন:"); bot.register_next_step_handler(message, search_do)
    elif message.text=="📢 Edit Notice":
        bot.send_message(message.chat.id, f"বর্তমান:\n{notice_data['text']}\n\nনতুন লিখুন:"); bot.register_next_step_handler(message, edit_notice_do)

def search_do(message):
    uid=message.text.strip()
    if uid not in users_db: bot.send_message(message.chat.id, "❌ পাওয়া যায়নি"); return
    u=users_db[uid]
    mk=types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("➕ বাড়ান", callback_data=f"add_{uid}"), types.InlineKeyboardButton("➖ কমান", callback_data=f"minus_{uid}"))
    mk.add(types.InlineKeyboardButton("💰 0 করুন", callback_data=f"zero_{uid}"))
    bot.send_message(message.chat.id, f"👤 {u['name']}\n🆔 {uid}\n💰 {u['balance']}৳\n👥 {len(u['referrals'])} ref", reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data.startswith("wd_approve_") or c.data.startswith("wd_reject_"))
def wd_action(call):
    if call.from_user.id!= ADMIN_ID: return
    parts=call.data.split("_"); action=parts[1]; uid=parts[2]; idx=int(parts[3])
    if uid in users_db and idx < len(users_db[uid]['withdraws']):
        if action=="approve":
            users_db[uid]['withdraws'][idx]['status']='approved'; save_db()
            bot.send_message(int(uid), f"✅ {users_db[uid]['withdraws'][idx]['amount']}৳ Approve হয়েছে!")
            bot.edit_message_text(f"✅ Approved {uid}", call.message.chat.id, call.message.message_id)
        else:
            amt=users_db[uid]['withdraws'][idx]['amount']; users_db[uid]['balance']+=amt; users_db[uid]['withdraws'][idx]['status']='rejected'; save_db()
            bot.send_message(int(uid), f"❌ {amt}৳ Reject, ফেরত দেওয়া হয়েছে")
            bot.edit_message_text(f"❌ Rejected {uid}", call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda c: c.data.startswith("add_") or c.data.startswith("minus_") or c.data.startswith("zero_"))
def edit_bal(call):
    if call.from_user.id!= ADMIN_ID: return
    action,uid=call.data.split("_")[0],call.data.split("_")[1]
    if action=="zero": users_db[uid]['balance']=0; save_db(); bot.answer_callback_query(call.id, "0 করা হয়েছে"); return
    bot.send_message(call.message.chat.id, f"{'কত বাড়াবেন?' if action=='add' else 'কত কমাবেন?'} {uid} এর জন্য:")
    bot.register_next_step_handler(call.message, lambda m: do_edit(m,uid,action))

def do_edit(message,uid,action):
    try:
        amt=int(message.text)
        if action=="add": users_db[uid]['balance']+=amt
        else: users_db[uid]['balance']=max(0,users_db[uid]['balance']-amt)
        save_db(); bot.send_message(message.chat.id, f"✅ নতুন ব্যালেন্স: {users_db[uid]['balance']}৳")
    except: bot.send_message(message.chat.id, "❌ সংখ্যা দিন")

def edit_notice_do(message):
    notice_data['text']=message.text; save_notice()
    bot.send_message(message.chat.id, "✅ Notice আপডেট!")

@bot.message_handler(func=lambda m: m.text == "💬 Support")
def sup(m): bot.send_message(m.chat.id, "Support @mhabul546")

bot.infinity_polling()
