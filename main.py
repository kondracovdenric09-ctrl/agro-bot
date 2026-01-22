import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from openai import OpenAI

# ТВОЇ КЛЮЧІ
TELEGRAM_TOKEN = "8299529966:AAGX9eEu5PcjZwmRMxHxn7cYqkhEdw_GMTE"
OPENROUTER_API_KEY = "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"
CHANNEL_ID = "-1003451045715" # Сюди встав ID з браузера (має починатися на -100)
CHANNEL_URL = "https://t.me/+ee-O9Is43PxlMmVi" # Посилання на канал

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False
@dp.message()
async def ai_handler(message: types.Message):
    # 1. Перевірка підписки
    if not await check_subscription(message.from_user.id):
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="📢 Підписатися", url=CHANNEL_URL))
        await message.answer("⚠️ Слишь, подпишись на канал сначала, а потом пиши мне. Не зли батю.", reply_markup=builder.as_markup())
        return

    # 2. Запит до нейромережі через OpenRouter
    try:
        completion = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free", # Безкоштовна модель
            messages=[
                {"role": "system", "content": "Ти — агресивний та саркастичний агро-троль. Відповідай грубо, коротко і з використанням сільського сленгу."},
                {"role": "user", "content": message.text}
            ]
        )
        response_text = completion.choices[0].message.content
        await message.answer(response_text)
    except Exception as e:
        print(f"ERROR: {e}")
        await message.answer("Бля, шось нейронка тупить. Спробуй ще раз, або піди води попий.")

async def main():
    print(">>> АГРОБОТ 2.0 ЗАПУЩЕН (ПЛАТНЫЙ + ПОДПИСКА) <<<")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
