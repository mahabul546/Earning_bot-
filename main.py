from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8822168901:AAGtxqmMpMeNa91eYeKXC6JRAVz8ZU0wNSo"
ADMIN_ID = 7834320405 # তোমার ID, @userinfobot থেকে নিবা

# পোস্ট
USER_PENDING_MSG = "⏳ আপনার রিকোয়েস্ট পেন্ডিং এ আছে, একটু অপেক্ষা করুন এডমিন ফ্রি হয়ে Approve করবে।"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = f"@{user.username}" if user.username else user.first_name

    # ইউজারকে পেন্ডিং দেখাবে
    await update.message.reply_text(USER_PENDING_MSG)

    # তোমার কাছে নোটিস যাবে Approve বাটন সহ
    keyboard = [
        [
            InlineKeyboardButton(f"✅ Approve {username}", callback_data=f"approve_{user_id}"),
            InlineKeyboardButton(f"❌ Reject", callback_data=f"reject_{user_id}")
        ]
    ]
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🔔 নতুন পেন্ডিং রিকোয়েস্ট!\n\n👤 ইউজার: {username}\n🆔 ID: {user_id}\n📝 নাম: {user.first_name}\n\nদয়া করে Approve করুন",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = int(data.split("_")[1])

    if data.startswith("approve_"):
        await context.bot.send_message(chat_id=user_id, text="✅ আপনার রিকোয়েস্ট Approve হয়েছে! এখন বট ব্যবহার করতে পারবেন। /start দিন")
        await query.edit_message_text(f"✅ {user_id} কে Approve করা হয়েছে।")
    else:
        await context.bot.send_message(chat_id=user_id, text="❌ আপনার রিকোয়েস্ট Reject করা হয়েছে।")
        await query.edit_message_text(f"❌ {user_id} কে Reject করা হয়েছে।")

# বট চালু
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_approve))
print("Bot is running...")
app.run_polling()
