from .admin import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


START_TEXT = """Hello {} 😌
I am a link shortner telegram bot.

>> `I can short any type of link`

Made by @FayasNoushad"""

HELP_TEXT = """**Hey, Follow these steps:**

➠ Just send a link for shorting.
➠ I will send the shorted links.

**Available Commands**

/start - Checking Bot Online
/help - For more help
/about - For more about me
/status - For bot status
/settings - For bot settings
/reset - For reset bot settings

Made by @FayasNoushad"""

ABOUT_TEXT = """--**About Me 😎**--

🤖 **Name :** [Link shortner](https://telegram.me/{})

👨‍💻 **Developer :** [GitHub](https://github.com/FayasNoushad) | [Telegram](https://telegram.me/FayasNoushad)

🌐 **Source :** [👉 Click here](https://github.com/FayasNoushad/URL-Shortner-Bot)

📝 **Language :** [Python3](https://python.org)

🧰 **Framework :** [Pyrogram](https://pyrogram.org)"""

SETTINGS_TEXT = "**Settings**"

RESET_TEXT = "**Are you sure for reset.**"

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('⚙ Help', callback_data='help'),
            InlineKeyboardButton('About 🔰', callback_data='about'),
            InlineKeyboardButton('Close ⛔️', callback_data='close')
        ]
    ]
)
HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('🏘 Home', callback_data='home'),
            InlineKeyboardButton('About 🔰', callback_data='about')
        ],
        [
            InlineKeyboardButton('⚒ Settings', callback_data='settings'),
            InlineKeyboardButton('Close ⛔️', callback_data='close')
        ]
    ]
)
ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('🏘 Home', callback_data='home'),
            InlineKeyboardButton('Help ⚙', callback_data='help')
        ],
        [
            InlineKeyboardButton('Close ⛔️', callback_data='close')
        ]
    ]
)
SETTINGS_BUTTONS = [
    [
        InlineKeyboardButton('🏘 Home', callback_data='home'),
        InlineKeyboardButton('Help ⚙', callback_data='help')
    ],
    [
        InlineKeyboardButton('🔄 Reset', callback_data='reset'),
        InlineKeyboardButton('Close ⛔️', callback_data='close')
    ]
]
RESET_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Yes ✅", callback_data="confirm_reset"),
            InlineKeyboardButton(text="No ❌", callback_data="cancel_reset")
        ]
    ]
)


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        reply_markup=START_BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )


@Client.on_message(filters.private & filters.command(["help"]))
async def help(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await update.reply_text(
        text=HELP_TEXT,
        disable_web_page_preview=True,
        reply_markup=HELP_BUTTONS,
        quote=True
    )


@Client.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await update.reply_text(
        text=ABOUT_TEXT.format((await bot.get_me()).username),
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS,
        quote=True
    )


@Client.on_message(filters.private & filters.command(["reset"]))
async def reset(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await update.reply_text(
        text=RESET_TEXT,
        disable_web_page_preview=True,
        reply_markup=RESET_BUTTONS,
        quote=True
    )


@Client.on_message(filters.private & filters.command(["status"]))
async def status(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    total_users = await db.total_users_count()
    text = "**Bot Status**\n"
    text += f"\n**Total Users:** `{total_users}`"
    await update.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )


@Client.on_message(filters.private & filters.command(["settings"]))
async def settings(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await display_settings(bot, update, db)


async def display_settings(bot, update, db, cb=False):
    chat_id = update.from_user.id
    text = SETTINGS_TEXT
    buttons = []
    
    if await db.allow_domain(chat_id, domain="gplinks.in"):
        buttons.append([InlineKeyboardButton(text="Gplinks.in ✅", callback_data="set+gplinks.in")])
    else:
        buttons.append([InlineKeyboardButton(text="Gplinks.in ❌", callback_data="set+gplinks.in")])
    
    if await db.allow_domain(chat_id, domain="bit.ly"):
        buttons.append([InlineKeyboardButton(text="Bit.ly ✅", callback_data="set+bit.ly")])
    else:
        buttons.append([InlineKeyboardButton(text="Bit.ly ❌", callback_data="set+bit.ly")])

    # Add Blogger-based URL shortener button
    if await db.allow_domain(chat_id, domain="blogger.com"):
        buttons.append([InlineKeyboardButton(text="Blogger.com ✅", callback_data="set+blogger.com")])
    else:
        buttons.append([InlineKeyboardButton(text="Blogger.com ❌", callback_data="set+blogger.com")])
    
    # Continue with the rest of the domains...
    
    # Example for tinyurl.com
    if await db.allow_domain(chat_id, domain="tinyurl.com"):
        buttons.append([InlineKeyboardButton(text="Tinyurl.com ✅", callback_data="set+tinyurl.com")])
    else:
        buttons.append([InlineKeyboardButton(text="Tinyurl.com ❌", callback_data="set+tinyurl.com")])
    
    keyboard = []
    
    for line in buttons:
        for button in line:
            if len(keyboard) == 0 or len(keyboard[-1]) >= 2:
                keyboard.append([button])
            else:
                keyboard[-1].append(button)
    
    for setting_button in SETTINGS_BUTTONS:
        keyboard.append(setting_button)
    
    if cb:
        await update.message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True
        )
    else:
        await update.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True,
            quote=True
        )
