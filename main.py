import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

TOKEN="9154777216:AAHumTWFBm7STfTL1McBnPLtM8cprc0U_pI"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! 👋 Men tarixiy Stickman Shorts videolar uchun ssenariy va tayyor matn tuzuvchi botman.\n\n"
        "Menga biror tarixiy mavzu yozib yuboring (masalan: *Olovning kashf etilishi* yoki *Rim imperiyasi*)."
    )

@dp.message()
async def shorts_script_generator(message: types.Message):
    topic = message.text
    
    # Shorts uchun 3 qismli (Hook, Story, Outro) tayyor ssenariya tuzish
    response_text = (
        f"🎬 **Mavzu:** {topic}\n"
        f"⏱ **Format:** YouTube Shorts (30 soniya)\n"
        f"🎨 **Uslub:** Stickman History Animation\n\n"
        f"--- \n"
        f"📌 **1-SAHNA (0-5 soniya - Diqqatni tortish / Hook):**\n"
        f"🗣 *Inglizcha matn:* \"Did you know how {topic} actually changed human history forever?\"\n"
        f"🖼 *Animatsiya (Prompt):* A shocked stickman looking at a glowing object on a dark historical background, 2D stickman animation style.\n\n"
        f"📌 **2-SAHNA (5-20 soniya - Asosiy voqea):**\n"
        f"🗣 *Inglizcha matn:* \"Back in the day, people struggled without {topic}. Until one brave mind decided to take a risk and change everything!\"\n"
        f"🖼 *Animatsiya (Prompt):* Stickman characters working hard, then a lightbulb appears above one stickman's head, dramatic lighting, simple black and white stickman art.\n\n"
        f"📌 **3-SAHNA (20-30 soniya - Xulosa / Outro):**\n"
        f"🗣 *Inglizcha matn:* \"And that is why our world looks the way it does today. Subscribe for more crazy history!\"\n"
        f"🖼 *Animatsiya (Prompt):* Modern stickman holding a smartphone next to ancient stickman, funny contrast, clean background.\n"
        f"--- \n"
        f"✅ *Keyingi qadam:* Shu inglizcha matnlarni ovozga aylantirib, promtlardan rasm yasaymiz."
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
