from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8822168901:AAGtxqmMpMeNa91eYeKXC6JRAVz8ZU0wNSo"
ADMIN_ID = 7834320405

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    full_name = user.full_name
    username = f"@{user.username}" if user.username else "No Username"

    # 1. ইউজারের কাছে তার নাম + ID সহ পেন্ডিং পোস্ট
    user_text = (
        f"⏳ আপনার রিকোয়েস্ট পেন্ডিং এ আছে\n"
        f"একটু অপেক্ষা করুন এডমিন ফ্রী হয়ে Approve করবে।\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 আপনার নাম: {full_name}\n"
        f"🆔 ইউজার আইডি: {user_id}\n"
        f"🔗 ইউজারনেম: {username}\n"
        f"━━━━━━━━━━━━━━"
    )
    await update.message.reply_text(user_text)

    # 2. তোমার কাছে নোটিস আসবে
    admin_text = (
        f"🔔 নতুন পেন্ডিং আসে দয়া করে Approve করুন\n\n"
        f"👤 নাম: {full_name}\n"
        f"🔗 ইউজারনেম: {username}\n"
        f"🆔 ID: {user_id}"
    )
    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")
        ]
    ]
    await context.bot.send_message(
        chat_id=ADMIN_ID, 
        text=admin_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action, uid = query.data.split("_")
    uid = int(uid)

    if action == "approve":
        await context.bot.send_message(chat_id=uid, text="✅ আপনাকে Approve করা হয়েছে! এখন বট ব্যবহার করুন। /start")
        await query.edit_message_text(f"✅ Approved ID: {uid}")
    else:
        await context.bot.send_message(chat_id=uid, text="❌ আপনার রিকোয়েস্ট Reject করা হয়েছে।")
        await query.edit_message_text(f"❌ Rejected ID: {uid}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_action))
print("Bot Running...")
app.run_polling()
