      import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN = 7834320405
approved = {ADMIN}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in approved:
        await update.message.reply_text(f"✅ Bot কাজ করছে! Welcome {update.effective_user.first_name}")
    else:
        await update.message.reply_text("⏳ Pending এ আছে")
        await context.bot.send_message(chat_id=ADMIN, text=f"Pending: {uid}\n/approve {uid}")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id!= ADMIN: return
    uid = int(context.args[0])
    approved.add(uid)
    await update.message.reply_text("Approved!")
    await context.bot.send_message(chat_id=uid, text="✅ Approved! /start দিন")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("approve", approve))
app.run_polling()  
