from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
import os

# ================= CONFIG =================
BOT_TOKEN = "8511288193:AAGmmvik8uydHGXweoWv1_8nwMkWENQAsnU"
ADMIN_ID = 7045296303  # ganti dengan Telegram ID kamu
MINIAPP_URL = "https://t.me/ViorexcoinBot/app"

USERS_FILE = "users.txt"
LOG_FILE = "log.txt"
# =========================================

START_TEXT = (
    "⭐ *Welcome to VIOREX Project*\n\n"
    "VIOREX is a decentralized blockchain project focused on the fair and sustainable distribution of VIOR tokens.\n\n"
    "*contract address:*\n" 
    "_0x61f2a0cbca1037842723e84d37634d8f83c7956a969b4382197fb26d0978a3f5::vior::VIOR_\n\n"
    "✨ Features:\n"
    "• Mine VIOR tokens\n"
    "• Real-time reward tracking\n"
    "• Additional bonuses from tasks\n"
    "• Invite friend for unlimited rewards\n"
    "• Instant withdrawal\n"
    "• Simple & transparent system\n\n"
    "Join early to become a top holder. 👑"
)

def log_event(text: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text = f"[{now}] {text}"
    print(log_text)

    with open(LOG_FILE, "a") as f:
        f.write(log_text + "\n")

def get_total_users():
    if not os.path.exists(USERS_FILE):
        return 0
    with open(USERS_FILE, "r") as f:
        return len(f.read().splitlines())

def save_user(user):
    user_id = user.id
    username = user.username or "NO_USERNAME"
    first_name = user.first_name or "-"

    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()

    with open(USERS_FILE, "r+") as f:
        users = f.read().splitlines()

        if str(user_id) not in users:
            f.write(f"{user_id}\n")
            total = get_total_users() + 1
            log_event(
                f"[NEW USER] ID={user_id} | @{username} | {first_name} | TOTAL={total}"
            )
        else:
            total = get_total_users()
            log_event(
                f"[OLD USER] ID={user_id} | @{username} | {first_name} | TOTAL={total}"
            )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user)

    keyboard = [
        [InlineKeyboardButton("💎 Earn VIOR", url=MINIAPP_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        START_TEXT,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized.")
        return

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/broadcast Your message here"
        )
        return

    message = " ".join(context.args)
    total = get_total_users()

    sent = 0
    with open(USERS_FILE, "r") as f:
        for line in f:
            try:
                await context.bot.send_message(
                    chat_id=int(line.strip()),
                    text=message
                )
                sent += 1
            except:
                pass

    log_event(f"[BROADCAST] Sent={sent}/{total}")
    await update.message.reply_text(
        f"✅ Broadcast sent to {sent} users."
    )

def main():
    print("🤖 Bot is running...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))

    app.run_polling()

if __name__ == "__main__":
    main()
