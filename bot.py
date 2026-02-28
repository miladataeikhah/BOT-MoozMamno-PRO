import os
import time
from dotenv import load_dotenv
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import database as db

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = int(os.getenv("123456789"))

user_last_message = {}

keyboard = [
    ["📸 نمونه کار"],
    ["💬 ثبت درخواست مشاوره"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.save_user(user.id, user.full_name)

    await update.message.reply_text(
        f"سلام {user.first_name} 🌸\nبه BOT-MoozMamno خوش اومدی!",
        reply_markup=reply_markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    # Anti-Spam
    now = time.time()
    if user.id in user_last_message and now - user_last_message[user.id] < 2:
        return
    user_last_message[user.id] = now

    if text and "مشاوره" in text:

        phone_button = KeyboardButton("ارسال شماره 📱", request_contact=True)
        contact_markup = ReplyKeyboardMarkup(
            [[phone_button]], resize_keyboard=True, one_time_keyboard=True
        )

        await update.message.reply_text(
            "لطفا شماره خود را ارسال کنید:",
            reply_markup=contact_markup
        )

    elif update.message.contact:
        phone = update.message.contact.phone_number
        db.save_phone(user.id, phone)

        await update.message.reply_text("شماره ثبت شد ✅ حالا پیام خود را بنویسید:")

    elif text and user.id != ADMIN_ID:

        db.save_request(user.id, text)

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 درخواست جدید:\n\nاز: {user.full_name}\nآیدی: {user.id}\n\n{text}"
        )

        await update.message.reply_text("درخواست شما ثبت شد ✅ به زودی تماس میگیریم.")

    else:
        await update.message.reply_text("لطفا از گزینه‌ها استفاده کنید.")


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    users_count = db.get_users_count()

    await update.message.reply_text(
        f"📊 پنل مدیریت\n\n👥 تعداد کاربران: {users_count}"
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    print("BOT-MoozMamno PRO running...")
    app.run_polling()
