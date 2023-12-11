from aiogram import types
from aiogram.types import InputFile, ReplyKeyboardMarkup, KeyboardButton
from database import get_all_topics_from_table


async def send_topic_info(message, topic_info):
    if not topic_info:
        await message.answer("🔧помилка🔧")
        return

    topic_id, title, image_url, description, likes, dislikes, table_name = topic_info

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("👍 Лайк"),
        KeyboardButton("👎 Дизлайк")
    )
    markup.add(
        KeyboardButton("➡️ Далі")
    )

    # Отправка сообщения с изображением, текстом и кнопками
    await message.answer_photo(
        photo=InputFile(image_url),
        parse_mode="Markdown",
        caption=f"*{title}*\n\n{description}\n\nLikes 👍: {likes}\nDislikes 👎: {dislikes}",
        reply_markup=markup
    )


# Функция для форматирования тем с номерами
def format_topics(topics):
    formatted_topics = "\n".join([f"{i+1}. {topic}" for i, topic in enumerate(topics)])
    return formatted_topics


# Основні концепції розумних міст
async def basic_concepts_handler(message: types.Message):
    table_name = 'basic'
    topics = get_all_topics_from_table(table_name)
    topics_text = format_topics(topics)

    # Создаем обычную клавиатуру с одной кнопкой
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Обрати випадкову тему👏"))

    # Используем reply_markup для добавления клавиатуры к сообщению
    await message.answer(
        f"Ось основні концепції розумних міст, про які я можу тобі розповісти🤗. "
        f"Для вибору теми введи її номер, або натисни обери тему випадково😎\n\n{topics_text}",
        reply_markup=markup
    )


# Технології, що використовуються у розумних містах
async def technologies_handler(message: types.Message):
    table_name = 'technologies'
    topics = get_all_topics_from_table(table_name)
    topics_text = format_topics(topics)

    # Клавіатура
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Обрати випадкову тему👏"))

    await message.answer(f"Технології - моя спеціалізація 👾 🤖. Обери тему з переліку та введи її номер, або "
                         f"обери випадкову тему натиснувши на кнопку під повідомленням ⚡️"
                         f":\n\n{topics_text}", reply_markup=markup)


# Приклади розумних міст у світі
async def examples_handler(message: types.Message):
    table_name = 'cities'
    topics = get_all_topics_from_table(table_name)
    topics_text = format_topics(topics)

    # Клавіатура
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Обрати випадкову тему👏"))

    await message.answer(f"Технології - моя спеціалізація 👾 🤖. Обери тему з переліку та введи її номер, або "
                         f"обери випадкову тему натиснувши на кнопку під повідомленням ⚡️"
                         f":\n\n{topics_text}", reply_markup=markup)
