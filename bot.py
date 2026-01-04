print("🔥 BOT.PY IS RUNNING - NO UPDATER HERE 🔥")
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ======================
# الإعدادات
# ======================
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN غير موجود")

ZERO_REMOVAL_FACTOR = 100  # حذف صفرين

BOT_OWNER = "Raeed Srewel"

# ======================
# أوامر
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔄 تحويل عكسي", callback_data="reverse")],
        [InlineKeyboardButton("📤 مشاركة البوت", switch_inline_query="بوت تحويل الليرة السورية القديمة والجديدة")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"""
👋 أهلاً بك!
أنا بوت تحويل العملة السورية 🇸🇾

📝 ملاحظة:
▪️ تم حذف صفرين من العملة الجديدة
▪️ البوت غير تابع لأي جهة حكومية

⏳ في حال تأخر الرد، يرجى الانتظار ثوانٍ قليلة

✍️ تطوير: {BOT_OWNER}

أرسل رقم للتحويل 👇
""",
        reply_markup=reply_markup
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"""
ℹ️ حول البوت

🔹 هذا البوت مخصص للتحويل بين:
- الليرة السورية القديمة
- الليرة السورية الجديدة (بعد حذف صفرين)

⚠️ البوت غير حكومي
🧑‍💻 المطور: {BOT_OWNER}
"""
    )

# ======================
# التحويل
# ======================
async def amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("❌ الرجاء إدخال رقم صحيح فقط")
        return

    amount = int(text)

    new_currency = amount // ZERO_REMOVAL_FACTOR
    old_currency = amount * ZERO_REMOVAL_FACTOR

    await update.message.reply_text(
        f"""
💱 نتيجة التحويل:

🔸 {amount} ليرة قديمة =
➡️ {new_currency} ليرة جديدة

🔸 {amount} ليرة جديدة =
➡️ {old_currency} ليرة قديمة
"""
    )

# ======================
# التشغيل
# ======================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, amount_handler))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

