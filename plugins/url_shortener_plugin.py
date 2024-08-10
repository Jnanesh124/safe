from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
import os

# Manual URL Shortener Function
async def manual_shortener(long_url):
    # This is a placeholder. Replace it with actual URL shortening logic or a static response.
    # For instance, you can create a mapping of long URLs to short URLs if you have a static set.
    short_url = f"https://short.url/{long_url.split('/')[-1]}"  # Example format
    return short_url

# Inline Keyboard Button
BUTTONS = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text='⚙ Feedback ⚙', url='https://telegram.me/FayasNoushad')]]
)

# Handle private messages with URLs
@Client.on_message(filters.private & filters.regex(r'https?://[^\s]+'))
async def reply_shortens(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)

    message = await update.reply_text(
        text="`Analysing your link...`",
        disable_web_page_preview=True,
        quote=True
    )
    link = update.matches[0].group(0)
    shortened_url = await manual_shortener(link)
    
    await message.edit_text(
        text=f"**Shortened URL:** {shortened_url}",
        reply_markup=BUTTONS,
        disable_web_page_preview=True
    )

# Handle inline queries
@Client.on_inline_query(filters.regex(r'https?://[^\s]+'))
async def inline_short(bot, update):
    link = update.matches[0].group(0)
    shortened_url = await manual_shortener(link)
    
    answers = [
        InlineQueryResultArticle(
            title="Short Links",
            description=update.query,
            input_message_content=InputTextMessageContent(
                message_text=f"**Shortened URL:** {shortened_url}",
                disable_web_page_preview=True
            ),
            reply_markup=BUTTONS
        )
    ]
    
    await bot.answer_inline_query(
        inline_query_id=update.id,
        results=answers
    )
