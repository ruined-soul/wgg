from datetime import datetime
import time
import warnings
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from telegram.error import BadRequest

# Suppress specific warning from python-telegram-bot about urllib3
warnings.filterwarnings("ignore", message="python-telegram-bot is using upstream urllib3")

# Logs group ID
# Replace these with your bot's details
BOT_NAME = "ᴡᴏᴍᴇɴ ꜱᴀꜰᴇᴛʏ ʙᴏᴛ"  # Replace with your bot's name
OWNER_ID = 6713994904  # Replace with your owner's user ID
BOT_USERNAME = "@IndiGptBot"  # Replace with your bot's username
SUPPORT_CHAT = "@MAMBA_GENUINE_SERVICES"  # Replace with your support chat link
telever = "12.0.0"  # Replace with actual library version if available
tlhver = "1.23"  # Replace with actual telethon version
pyrover = "2.0"  # Replace with actual pyrogram version
LOGS_GROUP_ID = "-1002002427595"  # Replace with your actual logs group ID

# Conversation states
USERNAME, USER_ID, CRIMINAL_USERNAME, CRIMINAL_ID, GROUP, IMAGES = range(6)

def validate_username(username: str) -> bool:
    # Check if the username starts with @ and is followed by alphanumeric characters or underscores
    return username.startswith('@') and len(username) > 1 and username[1:].replace('_', '').isalnum()

def register(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Welcome to the registration process. Please follow the instructions step by step.\n\n"
                              "Step 1: Send me your Telegram Username (e.g., @username).")
    return USERNAME

def username_handler(update: Update, context: CallbackContext) -> int:
    username = update.message.text.strip()

    if validate_username(username):
        context.user_data['user_username'] = username
        update.message.reply_text("Username is valid! Now, please send me your Telegram ID. (Go to @MissRose_bot, send /id, and copy your ID here.)")
        return USER_ID
    else:
        update.message.reply_text("Invalid username format. Please send a valid username starting with '@'.")
        return USERNAME

def user_id_handler(update: Update, context: CallbackContext) -> int:
    telegram_id = update.message.text.strip()

    if telegram_id.isdigit():
        context.user_data['user_id'] = telegram_id
        update.message.reply_text("User ID accepted! Now, send me the criminal's Telegram username (e.g., @username) or type 'Username not available'.")
        return CRIMINAL_USERNAME
    else:
        update.message.reply_text("Please send a valid numeric Telegram ID.")
        return USER_ID

def criminal_username_handler(update: Update, context: CallbackContext) -> int:
    criminal_username = update.message.text.strip()

    if criminal_username.lower() == 'username not available':
        context.user_data['criminal_username'] = criminal_username
        update.message.reply_text("Send me the criminal's Telegram ID (if available) or type 'ID not available'.")
        return CRIMINAL_ID
    elif criminal_username.startswith('@'):
        context.user_data['criminal_username'] = criminal_username
        update.message.reply_text("Criminal username is valid! Now send me the criminal's Telegram ID (if available) or type 'ID not available'.")
        return CRIMINAL_ID
    else:
        update.message.reply_text("Please send a valid criminal username starting with '@'.")
        return CRIMINAL_USERNAME

def criminal_id_handler(update: Update, context: CallbackContext) -> int:
    criminal_id = update.message.text.strip()

    if criminal_id.lower() == 'id not available':
        context.user_data['criminal_id'] = criminal_id
        update.message.reply_text("Criminal ID not available! Now send me the group username or link.")
        return GROUP
    elif criminal_id.isdigit():
        context.user_data['criminal_id'] = criminal_id
        update.message.reply_text("Criminal ID accepted! Now send me the group username or link.")
        return GROUP
    else:
        update.message.reply_text("Please send a valid numeric criminal ID or type 'ID not available'.")
        return CRIMINAL_ID

def group_handler(update: Update, context: CallbackContext) -> int:
    group_username = update.message.text.strip()

    if group_username.startswith('@') or group_username.startswith('https://t.me/'):
        try:
            group = context.bot.get_chat(group_username)
            context.user_data['group_username'] = group_username
            update.message.reply_text("Group exists! Now send the proof in the form of images.")
            return IMAGES
        except BadRequest:
            update.message.reply_text("This group does not exist. Please check the username or link.")
            return GROUP
    else:
        update.message.reply_text("Invalid group username or link. Please send a valid group username or link starting with '@' or 'https://t.me/'.")
        return GROUP

def images_handler(update: Update, context: CallbackContext) -> int:
    if update.message.photo:
        update.message.reply_text("Proofs accepted. Your details have been saved successfully.")
        
        # Send the report to the logs group
        report_message = (
            f"User {context.user_data['user_username']} registered a complaint.\n"
            f"User ID: {context.user_data['user_id']}\n"
            f"Criminal: {context.user_data['criminal_username']}\n"
            f"Criminal ID: {context.user_data['criminal_id']}\n"
            f"Group: {context.user_data['group_username']}"
        )
        context.bot.send_message(LOGS_GROUP_ID, report_message)
        
        return ConversationHandler.END
    else:
        update.message.reply_text("Please send valid proof images from the Telegram platform.")
        return IMAGES

StartTime = time.time()

def get_readable_time(seconds: int) -> str:
    # Converts seconds into a readable format like HH:MM:SS
    count = 0
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        if count < 2:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if result != 0:
            time_list.append(f"{int(result)}{time_suffix_list[count]}")
        seconds = int(remainder)
        count += 1

    time_list.reverse()
    return ":".join(time_list)

def ping(update: Update, context: CallbackContext) -> None:
    msg = update.effective_message

    # Measure the time taken to reply
    start_time = time.time()  # Uses time.time() to get the current time in seconds
    message = msg.reply_text("🏓 ᴘɪɴɢɪɴɢ ʙᴀʙʏ....")
    end_time = time.time()

    # Calculate ping and uptime
    telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
    uptime = get_readable_time(int(time.time() - StartTime))

    # Edit the message with ping and uptime information
    message.edit_text(
        "ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ! 🖤\n"
        "<b>ᴛɪᴍᴇ ᴛᴀᴋᴇɴ:</b> <code>{}</code>\n"
        "<b>ᴜᴘᴛɪᴍᴇ:</b> <code>{}</code>".format(telegram_ping, uptime),
        parse_mode=ParseMode.HTML,
    )
    
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome! I am your bot.")

#def ping(update: Update, context: CallbackContext) -> None:
#    update.message.reply_text("Pong!")

def alive(update: Update, context: CallbackContext) -> None:
    message = update.message

# Create the message text
    TEXT = (
        f"ʜᴇʏ,\n\nɪ ᴀᴍ {BOT_NAME}**\n━━━━━━━━━━━━━━━━━━━\n\n"
        f"» **ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ : [ʍǟʍɮǟ](tg://user?id={OWNER_ID})\n\n"
        f"» ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ : {telever} \n\n"
        f"» ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ : {tlhver} \n\n"
        f"» ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ : {pyrover} \n━━━━━━━━━━━━━━━━━\n\n"
    )

    # Create buttons
    BUTTON = [
        [
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/BLACKMAMBA_HU_VRO"),
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/MAMBA_GENUINE_SERVICES"),
        ]
    ]

    # Create reply markup
    reply_markup = InlineKeyboardMarkup(BUTTON)

    # Send the message
    message.reply_text(TEXT, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

# def alive(update: Update, context: CallbackContext) -> None:
#    update.message.reply_text("Yes, I am alive and working!")

def check_abuse(update: Update, context: CallbackContext) -> None:
    # Your abuse detection code here
    pass
def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "Here are the available commands:\n\n"
        "/start - Start interacting with the bot.\n"
        "/register - Register a complaint step by step.\n"
        "/ping - Check if the bot is responsive.\n"
        "/alive - Check if the bot is alive and working.\n"
        "/help - Show this help message."
    )
    update.message.reply_text(help_text)
    
def main():
    updater = Updater("6904434566:AAHgz6aHitWgn4q6KcZfD1Y48tIqA7wBRCc", use_context=True)
    dispatcher = updater.dispatcher

    # Conversation handler for registration
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register)],
        states={
            USERNAME: [MessageHandler(Filters.text & ~Filters.command, username_handler)],
            USER_ID: [MessageHandler(Filters.text & ~Filters.command, user_id_handler)],
            CRIMINAL_USERNAME: [MessageHandler(Filters.text & ~Filters.command, criminal_username_handler)],
            CRIMINAL_ID: [MessageHandler(Filters.text & ~Filters.command, criminal_id_handler)],
            GROUP: [MessageHandler(Filters.text & ~Filters.command, group_handler)],
            IMAGES: [MessageHandler(Filters.photo, images_handler)],
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("ping", ping))
    dispatcher.add_handler(CommandHandler("alive", alive))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_abuse))

    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
