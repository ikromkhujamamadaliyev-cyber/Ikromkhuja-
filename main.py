import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiohttp import web
from gtts import gTTS

TOKEN="9154777216:AAHumTWFBm7STfTL1McBnPLtM8cprc0U_pI"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Asosiy menyu tugmalarini yasash funksiyasi
def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="💳 Balans va tarif")
    builder.button(text="🤖 Video tayyorlash")
    builder.button(text="🛒 Xizmatlar")
    builder.button(text="📱 Virtual raqam")
    builder.button(text="⚙️ Sozlamalar")
    builder.button(text="🎁 Do'st taklif qilish")
    builder.button(text="💬 Yordam")
    # Tugmalar qanday joylashishini tartibga solish (har qatorda 2 tadan)
    builder.adjust(2, 2, 1, 2)
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! 👋 Kerakli bo'limni tanlang:",
        reply_markup=get_main_menu()
    )

# "Video tayyorlash" tugmasi bosilganda
@dp.message(lambda message: message.text == "🤖 Video tayyorlash")
async def video_menu(message: types.Message):
    await message.answer("🎬 Iltimos, video uchun tarixiy mavzu yuboring (masalan: *Ancient Rome*):")

# Boshqa tugmalar uchun umumiy javob yoki o'z handler'lari
@dp.message(lambda message: message.text == "💳 Balans va tarif")
async def balance_handler(message: types.Message):
    await message.answer("Sizning balansingiz: 0 so'm. Tarif: Bepul 🆓")

@dp.message(lambda message: message.text == "💬 Yordam")
async def help_handler(message: types.Message):
    await message.answer("Savollar bo'yicha @admin ga murojaat qiling.")

# Agar foydalanuvchi mavzu yuborsa (video yasash uchun)
@dp.message()
async def shorts_script_generator(message: types.Message):
    topic = message.text
    
    script_text = (
        f"Did you know how {topic} actually changed human history forever? "
        f"Back in the day, people struggled without it. Until one brave mind decided to take a risk and change everything!"
    )
    
    await message.answer(f"🎬 **Mavzu:** {topic}\n📜 **Matn tayyorlandi!** Ovoz yuborilmoqda...")
    
    audio_path = f"voice_{message.from_user.id}.mp3"
    tts = gTTS(text=script_text, lang='en', slow=False)
    tts.save(audio_path)
    
    audio_file = types.FSInputFile(audio_path)
    await message.answer_audio(audio=audio_file, caption="🎙 Shorts uchun tayyor inglizcha ovoz")
    
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
