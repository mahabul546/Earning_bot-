import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Token কোডে লাগবে না, Render থেকে আসবে
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 7834320405

# Approve লিস্ট, বট রিস্টার্ট হলেও যাতে ক্রস না করে তাই set ব্যবহার
approved_users = {ADMIN_ID}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        uid = user.id
        name = user.first_name

        # এডমিন হলে
        if uid == ADMIN_ID:
            await update.message.reply_text("✅ Admin Panel চালু আছে")
            return

        # Approve থাকলে
        if uid in approved_users:
            await update.message.reply_text(f"🎉 স্বাগতম {name}!\nআপনি Approve পেয়েছেন।")
            return

        # নতুন ইউজার হলে পেন্ডিং দেখাবে
        await update.message.reply_text("আপনার রিকোয়েস্ট পেন্ডিং এ আসে একটু অপেক্ষা করুন এডমিন ফ্রী হয়ে অপ্রভ করবে।")

        # তোমার কাছে নোটিস যাবে নাম সহ
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔔 পেন্ডিং নোটিস!\n\n👤 নাম: {name}\n🆔 ID: {uid}\n\n⚠️ পেন্ডিং আসে দয়া করে আপ্রভ করুন\n\nআপ্রভ করতে:\n/approve {uid}"
        )
    except Exception as e:
        print(f"Error in start: {e}")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.effective_user.id!= ADMIN_ID:
            return

        if not context.args:
            await update.message.reply_text("লিখো: /approve USER_ID")
            return

        uid = int(context.args[0])
        approved_users.add(uid)

        await update.message.reply_text(f"✅ {uid} কে Approve করা হলো")
        await context.bot.send_message(chat_id=uid, text="✅ আপনাকে Approve করা হয়েছে! এখন /start চাপুন")

    except Exception as e:
        print(f"Error in approve: {e}")
        await update.message.reply_text("ID ভুল দিয়েছো")

# বট চালু, ক্রস করবে না
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("approve", approve))

print("Bot Running...")
app.run_polling()
