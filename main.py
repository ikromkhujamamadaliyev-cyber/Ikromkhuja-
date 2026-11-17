import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web
from gtts import gTTS

TOKEN="9154777216:AAHumTWFBm7STfTL1McBnPLtM8cprc0U_pI"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! 👋 Men tarixiy Stickman Shorts ssenariysi va ovozini tayyorlab beruvchi botman.\n\n"
        "Menga biror tarixiy mavzu yozib yuboring (masalan: *Ancient Rome* yoki *The invention of wheel*)."
    )

@dp.message()
async def shorts_script_generator(message: types.Message):
    topic = message.text
    
    # 1. Ssenariy matni
    script_text = (
        f"Did you know how {topic} actually changed human history forever? "
        f"Back in the day, people struggled without it. Until one brave mind decided to take a risk and change everything! "
        f"And that is why our world looks the way it does today. Subscribe for more crazy history!"
    )
    
    response_text = (
        f"🎬 **Mavzu:** {topic}\n"
        f"⏱ **Format:** YouTube Shorts (30 soniya)\n\n"
        f"📜 **Inglizcha Matn (Voiceover):**\n\"{script_text}\"\n\n"
        f"🔊 *Hozir siz uchun ovozli xabar tayyorlanmoqda...*"
    )
    
    await message.answer(response_text, parse_mode="Markdown")
    
    # 2. Matnni ingliz tilida ovozga (MP3) aylantirish
    audio_path = f"voice_{message.from_user.id}.mp3"
    tts = gTTS(text=script_text, lang='en', slow=False)
    tts.save(audio_path)
    
    # 3. Ovozli xabarni Telegram'ga yuborish
    audio_file = types.FSInputFile(audio_path)
    await message.answer_audio(audio=audio_file, caption="🎙 Shorts uchun tayyor inglizcha ovoz (Voiceover)")
    
    # 4. Serverda qolgan vaqtinchalik faylni o'chirish
    if os.path.exists(audio_path):
        os.remove(audio_path)

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
