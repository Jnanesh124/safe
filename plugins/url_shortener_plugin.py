import os
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent

# Load environment variables
BLOGGER_API_URL = os.environ.get("BLOGGER_API_URL")

# Manual URL Shortener Function
async def manual_shortener(long_url):
    if BLOGGER_API_URL:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(BLOGGER_API_URL, json={"longUrl": long_url}) as response:
                    data = await response.json()
                    short_url = data.get("shortUrl", long_url)  # Adjust according to your API response
                    return short_url
        except Exception as e:
            print(f"Error shortening URL: {e}")
            return long_url
    return long_url

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
