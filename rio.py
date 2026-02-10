# ================================
# Telegram Public Info Bot
# Developer : Harsh Shelby
# ================================

import requests
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================================
# CONFIG
# ================================
BOT_TOKEN = "8019060393:AAFFEHBxMBAnVQLfgF5CWWT6eNa3D993uV8"
TIMEOUT = 15

# Block your personal number
BLOCKED_NUMBERS = [
    "9560877681"
]

# ================================
# API FUNCTIONS
# ================================

def number_info(num):
    return requests.get(
        f"https://usesirosint.vercel.app/api/numinfo?key=land&num={num}",
        timeout=TIMEOUT
    ).json()

def vehicle_info(vehicle):
    return requests.get(
        f"https://vehicle-info-aco-api.vercel.app/info?vehicle={vehicle}",
        timeout=TIMEOUT
    ).json()

def ff_info(uid):
    return requests.get(
        f"https://abbas-apis.vercel.app/api/ff-info?uid={uid}",
        timeout=TIMEOUT
    ).json()

def ff_ban(uid):
    return requests.get(
        f"https://abbas-apis.vercel.app/api/ff-ban?uid={uid}",
        timeout=TIMEOUT
    ).json()

def ifsc_info(ifsc):
    return requests.get(
        f"https://abbas-apis.vercel.app/api/ifsc?ifsc={ifsc}",
        timeout=TIMEOUT
    ).json()

def email_info(email):
    return requests.get(
        f"https://abbas-apis.vercel.app/api/email?mail={email}",
        timeout=TIMEOUT
    ).json()

# ================================
# UI
# ================================

def menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📱 Number Info", callback_data="number"),
            InlineKeyboardButton("🚗 Vehicle Info", callback_data="vehicle")
        ],
        [
            InlineKeyboardButton("🎮 FF UID Info", callback_data="ff"),
            InlineKeyboardButton("🚫 FF Ban Check", callback_data="ffban")
        ],
        [
            InlineKeyboardButton("🏦 IFSC Info", callback_data="ifsc"),
            InlineKeyboardButton("📧 Email Info", callback_data="email")
        ]
    ])

def pretty(data):
    return "<pre>" + json.dumps(data, indent=2, ensure_ascii=False) + "</pre>"

# ================================
# HANDLERS
# ================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ <b>PUBLIC INFO BOT</b>\n\n"
        "Select an option below 👇\n\n"
        "👨‍💻 Developer: <b>Harsh Shelby</b>",
        reply_markup=menu(),
        parse_mode="HTML"
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["mode"] = query.data

    msg = {
        "number": "📱 Send Number\nExample: 9998887779",
        "vehicle": "🚗 Send Vehicle No\nExample: AP40NA3662",
        "ff": "🎮 Send FF UID\nExample: 2819649271",
        "ffban": "🚫 Send FF UID\nExample: 11111111",
        "ifsc": "🏦 Send IFSC\nExample: SBIN0001234",
        "email": "📧 Send Email\nExample: test@gmail.com"
    }

    await query.edit_message_text(msg[query.data])

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "mode" not in context.user_data:
        await update.message.reply_text("❌ Please use /start first")
        return

    mode = context.user_data["mode"]
    value = update.message.text.strip()
    loading = await update.message.reply_text("⏳ Fetching data...")

    try:
        if mode == "number":
            if value in BLOCKED_NUMBERS:
                await loading.edit_text(
                    "🚫 <b>Access Denied</b>\n\nThis number is protected.",
                    parse_mode="HTML",
                    reply_markup=menu()
                )
                context.user_data.clear()
                return

            data = number_info(value)

        elif mode == "vehicle":
            data = vehicle_info(value)
        elif mode == "ff":
            data = ff_info(value)
        elif mode == "ffban":
            data = ff_ban(value)
        elif mode == "ifsc":
            data = ifsc_info(value)
        elif mode == "email":
            data = email_info(value)
        else:
            data = {"error": "Invalid request"}

        await loading.edit_text(
            "✅ <b>Result</b>\n" + pretty(data),
            parse_mode="HTML",
            reply_markup=menu()
        )

    except Exception as e:
        await loading.edit_text(f"❌ Error: {e}")

    context.user_data.clear()

# ================================
# MAIN
# ================================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

    print("Bot running | Developer: Harsh Shelby")
    app.run_polling()

if __name__ == "__main__":
    main()