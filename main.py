import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 7834320405
approved_users = {ADMIN_ID}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id == ADMIN_ID:
        await update.message.reply_text("✅ Admin Panel চালু আছে")
        return
    if user.id in approved_users:
        await update.message.reply_text(f"🎉 স্বাগতম {user.first_name}! Approve পেয়েছেন")
        return
    await update.message.reply_text("আপনার রিকোয়েস্ট পেন্ডিং এ আসে একটু অপেক্ষা করুন এডমিন ফ্রী হয়ে অপ্রভ করবে।")
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 পেন্ডিং নোটিস!\n\n👤 নাম: {user.first_name}\n🆔 ID: {user.id}\n\nপেন্ডিং আসে দয়া করে আপ্রভ করুন\n/approve {user.id}")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id!= ADMIN_ID: return
    if not context.args: return
    uid = int(context.args[0])
    approved_users.add(uid)
    await update.message.reply_text(f"✅ {uid} Approved")
    await context.bot.send_message(chat_id=uid, text="✅ আপনাকে Approve করা হয়েছে! এখন /start দিন")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("approve", approve))
app.run_polling()
