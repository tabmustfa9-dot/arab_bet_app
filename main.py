import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup

# --- إعدادات البوت ---
# 1. ضع التوكن الخاص بك هنا (من @BotFather)
TOKEN = "YOUR_BOT_TOKEN"

# 2. ضع رابط GitHub Pages الذي يحتوي على ملف index.html
# مثال: https://username.github.io/repo-name/
WEB_APP_URL = "https://your-username.github.io/your-repo/"

# إعداد السجلات (Logging) لمراقبة الأخطاء
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """الرد على أمر البداية بفتح واجهة تطبيق الويب"""
    
    # إنشاء لوحة أزرار تحتوي على زر الـ Web App
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="دخول المنطقة 🔥", 
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]
    ])
    
    await message.answer(
        f"أهلاً بك يا {message.from_user.first_name} في Chill Zone!\n\n"
        "هنا يمكنك المراهنة بنقاطك وتجربة حظك.\n"
        "رصيدك الحالي هو 1000 نقطة.",
        reply_markup=markup
    )

@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    """استقبال البيانات القادمة من صفحة الويب (الرهانات)"""
    data = message.web_app_data.data
    
    if data == "bet_placed_100":
        # هنا يمكنك إضافة كود لخصم النقاط من قاعدة البيانات مستقبلاً
        await message.answer("✅ تم استلام رهانك بمبلغ 100 نقطة بنجاح!")
    else:
        await message.answer(f"وصلت بيانات غير معروفة: {data}")

async def main():
    try:
        print("جاري تشغيل البوت... اضغط Ctrl+C للإيقاف")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("البوت توقف!")
