from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "BOT_TOKEN"

SIGNATURE = (
    "\n\n—\n"
    "⚠️ أداة حسابية فقط – غير حكومية\n"
    "🛠️ Raeed Srewel"
)


# ======================
# القوائم
# ======================
def main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇸🇾 قديمة ➜ 🆕 جديدة", callback_data="old_to_new"),
            InlineKeyboardButton("🆕 جديدة ➜ 🇸🇾 قديمة", callback_data="new_to_old")
        ],
        [
            InlineKeyboardButton("ℹ️ عن العملة الجديدة", callback_data="info"),
            InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back")
        ]
    ])

def result_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 تحويل عكسي", callback_data="reverse")],
        [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back")]
    ])

# ======================
# /start
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 أهلاً بك في بوت تحويل الليرة السورية\n\n"
        "🛠️ إعداد: *Raeed Srewel*\n\n"
        "📌 ملاحظة مهمة:\n"
        "تم حذف صفرين من العملة السورية القديمة\n"
        "100 ليرة قديمة = 1 ليرة جديدة\n\n"
        "⚠️ *تنويه قانوني:*\n"
        "هذا البوت غير تابع لأي جهة حكومية\n"
        "وهو أداة حسابية فقط\n\n"
        "👇 اختر العملية:"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# ======================
# الأزرار
# ======================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data in ["old_to_new", "new_to_old"]:
        context.user_data["mode"] = data
        msg = "✍️ أدخل المبلغ بالليرة القديمة" if data == "old_to_new" else "✍️ أدخل المبلغ بالليرة الجديدة"
        await query.edit_message_text(msg)

    elif data == "reverse":
        if context.user_data.get("mode") == "old_to_new":
            context.user_data["mode"] = "new_to_old"
            await query.edit_message_text("🔁 تحويل عكسي\n✍️ أدخل المبلغ بالليرة الجديدة")
        else:
            context.user_data["mode"] = "old_to_new"
            await query.edit_message_text("🔁 تحويل عكسي\n✍️ أدخل المبلغ بالليرة القديمة")

    elif data == "info":
        text = (
            "ℹ️ *معلومات عن الليرة السورية الجديدة*\n\n"
            "🔢 تم حذف صفرين من العملة\n"
            "🎯 الهدف تسهيل الحسابات فقط\n\n"
            "📉 القيمة الشرائية لم تتغير\n\n"
            "⚠️ هذا البوت غير حكومي"
        )
        await query.edit_message_text(
            text,
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )

    elif data == "back":
        await start(query, context)

# ======================
# إدخال الرقم
# ======================
async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text)
        mode = context.user_data.get("mode")

        if not mode:
            await update.message.reply_text("⚠️ استخدم /start أولاً")
            return

        if mode == "old_to_new":
            result = amount / 100
            text = (
                f"🔁 *التحويل*\n\n"
                f"🇸🇾 {amount:,.0f} ليرة قديمة\n"
                f"⬇️\n"
                f"🆕 {result:,.2f} ليرة جديدة\n\n"
                + SIGNATURE
            )
        else:
            result = amount * 100
            text = (
                f"🔁 *التحويل*\n\n"
                f"🆕 {amount:,.2f} ليرة جديدة\n"
                f"⬇️\n"
                f"🇸🇾 {result:,.0f} ليرة قديمة\n\n"
                + SIGNATURE
            )

        await update.message.reply_text(
            text,
            reply_markup=result_menu(),
            parse_mode="Markdown"
        )

    except ValueError:
        await update.message.reply_text("❌ الرجاء إدخال رقم صحيح فقط")

# ======================
# تشغيل
# ======================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount))
    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
