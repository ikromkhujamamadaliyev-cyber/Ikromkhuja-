import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# O'z Telegram bot tokeningizni shu yerga yozing:
TOKEN = "9154777216:AAHumTWFBm7STfTL1McBnPLtM8cprc0U_pI"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "🎬 **YouTube Shorts Stickman Bot**ga xush kelibsiz!\n\n"
        "Menga istalgan tarixiy mavzuni yozib yuboring (masalan: *Ancient Rome*, *The invention of fire*, *Alexander the Great*). "
        "Men darhol Shorts uchun tayyor inglizcha ssenariy va matn tuzib beraman!"
    )

@dp.message()
async def shorts_generator(message: types.Message):
    topic = message.text
    
    # YouTube Shorts uchun tayyor stikmen ssenariysi
    response_text = (
        f"🎬 **Mavzu:** {topic}\n"
        f"⏱ **Format:** YouTube Shorts (30 soniya)\n"
        f"🎨 **Uslub:** Stickman History Animation\n\n"
        f"--- \n"
        f"📌 **1-SAHNA (0-5s - Hook / Diqqatni tortish):**\n"
        f"🗣 *Inglizcha matn:* \"Did you know how {topic} actually changed human history forever?\"\n"
        f"🖼 *Vizual Prompt:* A shocked stickman looking at a glowing historical object, 2D stickman art.\n\n"
        f"📌 **2-SAHNA (5-20s - Asosiy hikoya):**\n"
        f"🗣 *Inglizcha matn:* \"Back in the day, people struggled without it. Until one brave mind decided to take a risk and change everything!\"\n"
        f"🖼 *Vizual Prompt:* Stickman characters working hard, lightbulb idea moment, simple black and white style.\n\n"
        f"📌 **3-SAHNA (20-30s - Outro / Xulosa):**\n"
        f"🗣 *Inglizcha matn:* \"And that is why our world looks the way it does today. Subscribe for more crazy history!\"\n"
        f"🖼 *Vizual Prompt:* Modern stickman holding a smartphone next to ancient stickman, clean background.\n"
        f"--- \n"
        f"✅ *Holat:* Ssenariy tayyor! Buni ovozga aylantirib, videoga ulaymiz."
    )
    
    await message.answer(response_text, parse_mode="Markdown")

async def handle(request):
    return web.Response(text="Bot is running!")

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
