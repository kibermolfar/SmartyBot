import asyncio

from initialization import dp
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
     ReplyKeyboardRemove, InputFile

from quiz import questions_handler, question_engine, test_end_handler, reset_quiz
from topics_handlers import basic_concepts_handler, technologies_handler, examples_handler, send_topic_info
from database import get_topic_by_number, get_random_topic_from_table, get_all_topics_from_table, like, dislike

answered_questions = 0
right_answered_questions = 0

global_topic_num = 1
global_table_name = ""
prev_message = ""
questions_list = []


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Отправка приветственного сообщения с использованием имени пользователя
    await message.answer(f"Привіт, {message.from_user.first_name}! Мене звати Smarty, і я - твій помічник у світі "
                         f"розумних міст 😊. Для подальших дій викликай /help")


# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    help_text = (f"Тут для тебе список команд, які допоможуть тобі зрозуміти, як працювати з ботом:\n"
                 f"/air - Допоможе визначити якість повітря 😶‍🌫️ он-лайн у твоєму місті/регіоні\n"
                 f"/water - Допоможе визначити якість води 💧 он-лайн у твоєму місті/регіоні\n"
                 f"/gov - Дізнайся про Дію і електронні петиції в Україні прямо зараз❗️\n"
                 f"/car_chargers - Якщо тобі необхідно зарядити електромобіль - звертайся до мене😇\n"
                 f"/quiz - Перевір свої знання з теми 'Розумні міста' прямо зараз😎\n"
                 f"/activities - Дізнайся нову інформацію про розумні міста ℹ️\n"
                 f"\nP.S: Цікаво подивитися на команду розробників? Клацай сюди ➡️ /devs")
    await message.answer(help_text)


# Обработчик команды /devs
@dp.message_handler(commands=['devs'])
async def devs_info_command(message: types.Message):

    # Отправка изображения и сообщения
    await message.answer_photo(
        photo=InputFile("DevsPictures/Ivan.jpg"),
        parse_mode="HTML",
        caption=(
            "Чурилов Іван ПБ-21 - програміст і тімлід проекту\n"
            "Розробник концепції бота, функціоналу і загального вигляду проекту.\n\n"
            "<blockquote>Smarty - мій перший чат-бот для Телеграму і перший значний проект написаний на мові python. "
            "Не все вдалося реалізувати так, як хотілося, або ж взагалі реалізувати, але я дякую моїй команді, "
            "без хлопців було би тяжко 😉</blockquote>"
            "\n\n"
            "Контакти - telegram @kibermolfar"
        )
    )
    await asyncio.sleep(1)
    # Отправка изображения и сообщения
    await message.answer_photo(
        photo=InputFile("DevsPictures/Igor.jpg"),
        parse_mode="HTML",
        caption=(
            "Малюк Ігор СП-23 - мотиватор проекту та одни з розробників\n"
            "Теми до розділу /activities - Основні концепції розумних міст 1️⃣ 2️⃣ 3️⃣ + питання до /quiz.\n\n"
            "<blockquote>⬆️хочу так шоб мене записали ахахах⬆️</blockquote>"
            "\n\n"
            "Контакти - telegram @Pazuchela"
        )
    )
    await asyncio.sleep(1)
    # Отправка изображения и сообщения
    await message.answer_photo(
        photo=InputFile("DevsPictures/Artem.jpg"),
        parse_mode="HTML",
        caption=(
            "Кримський Артем СП-23 - старанний працівник та один з розробників\n"
            "Теми до розділу /activities - Технології, які використовуються в розумних містах 🧑‍💻 + питання до /quiz.\n"
            "<blockquote> тут поки пусто </blockquote>"
            "\n\n"
            "Контакти - telegram @artemovskiiy"
        )
    )
    await asyncio.sleep(1)
    # Отправка изображения и сообщения
    await message.answer_photo(
        photo=InputFile("DevsPictures/Danil.png"),
        parse_mode="HTML",
        caption=(
            "Данило Макогон ПО-21 - поціновувач інновацій у світі програмування 💻. Любитель емоджі🎭, класних стікерів🎟\n"
            "\n{✅Один із розробників👨‍💻}\n\n"
            "Завзятий учасник /activities - де ділиться *Прикладами розумних міст у світі* 🌇 + влаштовує захоплюючі /quiz для користувачів👥.\n\n"
            "<blockquote>👌😁👍</blockquote>"
            "\n\n"
            "Контакти - telegram @danulomakogon"
        )
    )
    await message.answer("SmartGachiClub_2023")


# Обработчик команды /gov
@dp.message_handler(commands=['gov'])
async def gov(message: types.Message):
    dia_url = "https://diia.gov.ua"
    president_url = "https://president.gov.ua"
    kabinet_url = "https://petition.kmu.gov.ua"
    kyiv_url = "https://kyivcity.gov.ua"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Дія", url=dia_url), InlineKeyboardButton("Оф. портал Києва", url=kyiv_url))
    markup.add(InlineKeyboardButton("Електронні петиції Президент України", url=president_url))
    markup.add(InlineKeyboardButton("Електронні петиції КабМін", url=kabinet_url))

    await message.answer(
        "Україна 🇺🇦 вже сьогодні робить кроки, щоб її міста були 'розумними', а країна - сучасною 📈. "
        "Якщо ти ще не чув про дію та електронні петиції - обов'язково клікай на наступні посилання і запам'ятай, "
        "що домен GOV.UA призначений для органів державної влади України. \n\nЗапровадження державних послуг "
        "для населення в електронному форматі є обов'язковим елементом розумного міста ⬇️⬇️⬇️",
        reply_markup=markup)


# Обработчик команды /water
@dp.message_handler(commands=['water'])
async def water_pollution(message: types.Message):
    kyiv_water_url = "https://ecosoft.ua/ua/water-map/"
    ukraine_water_url = "https://ziko.com.ua/ru/analysis-map/"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Київ", url=kyiv_water_url))
    markup.add(InlineKeyboardButton("Україна", url=ukraine_water_url))

    await message.answer(
        "Я володію 2-ма відкритими інтернет-ресурсами, які допоможуть дізнатися якість води в твоєму "
        "місті в реальному часі. 1 кнопка допоможе тобі дізнатись якість води у Києві, 2 - в інших регіонах "
        "країни (Хоч більшість датчиків і знаходяться у західній частині "
        "України 🇺🇦, у інших містах вони теж є, спробуй 😉)",
        reply_markup=markup)


# Обработчик команды /air
@dp.message_handler(commands=['air'])
async def air_pollution(message: types.Message):
    kyiv_url = "https://www.iqair.com/ukraine/kyiv/kyiv-c"
    kharkiv_url = "https://www.iqair.com/ukraine/kharkiv"
    lviv_url = "https://www.iqair.com/ukraine/lviv"
    odessa_url = "https://www.iqair.com/ukraine/odessa"
    dnipro_url = "https://www.iqair.com/ukraine/dnipro"
    vinnutsia_url = "https://www.iqair.com/ukraine/vinnyts-ka/vinnytsia"
    chernivtsi_url = "https://www.iqair.com/ukraine/chernivtsi"
    ivano_frankivsk_url = "https://www.iqair.com/ukraine/ivano-frankivsk"
    ukraine_url = "https://www.iqair.com/ukraine"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Київ", url=kyiv_url), InlineKeyboardButton("Харків", url=kharkiv_url))
    markup.add(InlineKeyboardButton("Львів", url=lviv_url), InlineKeyboardButton("Одесса", url=odessa_url))
    markup.add(InlineKeyboardButton("Дніпро", url=dnipro_url), InlineKeyboardButton("Вінниця", url=vinnutsia_url))
    markup.add(InlineKeyboardButton("Чернівці", url=chernivtsi_url), InlineKeyboardButton("Івано-Франківськ", url=ivano_frankivsk_url))
    markup.add(InlineKeyboardButton("Повітря в Україні", url=ukraine_url))

    await message.answer(
        "Щоб дізнатися якість повітря у своєму місті в реальному часі😶‍🌫, "
        "обери своє місто зі списку, або, якщо його немає в списку, нитисни кнопку 'Повітря в Україні'🇺🇦",
        reply_markup=markup)


# Обработчик команды /car_chargers
@dp.message_handler(commands=['car_chargers'])
async def car_chargers_nearby(message: types.Message):
    # Получаем координаты пользователя (если доступно)
    latitude = message.location.latitude if message.location else None
    longitude = message.location.longitude if message.location else None

    # Создаем URL для Google Maps с координатами пользователя и запросом о зарядках
    google_maps_url = f"https://www.google.com/maps/search/?api=1&query=зарядка+для+електромобілів"

    # Создаем Inline клавиатуру с кнопкой для открытия Google Maps
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Відкрити Google Maps", url=google_maps_url))

    # Отправляем сообщение с клавиатурой
    await message.answer("Натисни на кнопку, щоб подивитися, де знаходяться найближчі зарядні станціі для твого електромобіля",
                         reply_markup=markup)


# Обработчик команды /quiz
@dp.message_handler(commands=['quiz'])
async def quiz_command(message: types.Message):
    # Отправка сообщения с вопросом и вертикальными кнопками
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    buttons = [
        KeyboardButton(text="Тест на 5 питаннь 🥱"),
        KeyboardButton(text="Тест на 10 питнаннь 🧐"),
        KeyboardButton(text="Тест на 15 питаннь 😈"),
    ]

    markup.add(*buttons)
    await message.answer("Зараз я проведу для тебе тестування. Обери, на яку кількість питаннь "
                         "ти готовий зараз відповісти за допомогою кнопок нижче⬇️⬇️⬇️", reply_markup=markup)


@dp.message_handler(lambda message: message.text
                    and message.text in ["Тест на 5 питаннь 🥱",
                                         "Тест на 10 питнаннь 🧐",
                                         "Тест на 15 питаннь 😈"])
async def handle_button_click(message: types.Message):
    selected_button_text = message.text
    global questions_list
    if selected_button_text == "Тест на 5 питаннь 🥱":
        questions_list = questions_handler(5)
        await question_engine(message)
    elif selected_button_text == "Тест на 10 питнаннь 🧐":
        questions_list = questions_handler(10)
        await question_engine(message)
    elif selected_button_text == "Тест на 15 питаннь 😈":
        questions_list = questions_handler(15)
        await question_engine(message)


@dp.message_handler(lambda message: message.text in ["Варіант 1", "Варіант 2", "Варіант 3", "Варіант 4"])
async def handle_test_answer(message: types.Message):
    global answered_questions
    global right_answered_questions

    question = questions_list[answered_questions]

    answered_questions += 1

    if answered_questions < len(questions_list):
        # Обрабатываем ответ пользователя
        selected_option = message.text

        question_text, answer_1, answer_2, answer_3, answer_4, right_answer = question
        await message.answer(f"Ви обрали варіант: {selected_option}")
        if right_answer == message.text:
            right_answered_questions += 1

        await question_engine(message)

    elif answered_questions >= len(questions_list):
        await message.answer(f"Ви обрали варіант: {message.text}")
        question_text, answer_1, answer_2, answer_3, answer_4, right_answer = question
        if right_answer == message.text:
            right_answered_questions += 1

        await test_end_handler(message, answered_questions, right_answered_questions)

        answered_questions = 0
        right_answered_questions = 0
        reset_quiz()


# Обработчик команды /activities
@dp.message_handler(commands=['activities'])
async def activity_command(message: types.Message):
    # Отправка сообщения с вопросом и вертикальными кнопками
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    buttons = [
        KeyboardButton(text="Основні концепції розумних міст 1️⃣ 2️⃣ 3️⃣"),
        KeyboardButton(text="Технології, які використовуються в розумних містах 🧑‍💻"),
        KeyboardButton(text="Приклади розумних міст у світі 🌆"),
    ]

    markup.add(*buttons)
    await message.answer("Про що ти хочеш дізнатися сьогодні?", reply_markup=markup)


@dp.message_handler(lambda message: message.text
                    and message.text in ["Основні концепції розумних міст 1️⃣ 2️⃣ 3️⃣",
                                         "Технології, які використовуються в розумних містах 🧑‍💻",
                                         "Приклади розумних міст у світі 🌆"])
async def handle_button_click(message: types.Message):
    global prev_message
    selected_button_text = message.text

    if selected_button_text == "Основні концепції розумних міст 1️⃣ 2️⃣ 3️⃣":
        await basic_concepts_handler(message)
        prev_message = "Основні концепції розумних міст 1️⃣ 2️⃣ 3️⃣"
    elif selected_button_text == "Технології, які використовуються в розумних містах 🧑‍💻":
        await technologies_handler(message)
        prev_message = "Технології, які використовуються в розумних містах 🧑‍💻"
    elif selected_button_text == "Приклади розумних міст у світі 🌆":
        await examples_handler(message)
        prev_message = "Приклади розумних міст у світі 🌆"


@dp.message_handler(lambda message: message.text.isdigit()
                    or message.text == "Обрати випадкову тему👏")
async def process_topic_number(message: types.Message):
    global global_topic_num
    global global_table_name

    # Получаем номер темы из текста сообщения
    topic_number = ""

    if message.text.isdigit():
        # Если строка является числом, преобразуем ее в int
        topic_number = int(message.text)
        global_topic_num = topic_number
        # Ваш код для обработки числа topic_number
        await message.answer(f"Ви обрали тему під номером 🎲 {topic_number} 🎲 ")

        if (prev_message == "Основні концепції розумних міст 1️⃣ 2️⃣ 3️⃣"
                and topic_number <= len(get_all_topics_from_table('basic'))
                and message.text != "Обрати випадкову тему👏"):
            topic_info = get_topic_by_number('basic', topic_number)
            global_table_name = 'basic'
            await send_topic_info(message, topic_info)
        elif (prev_message == "Технології, які використовуються в розумних містах 🧑‍💻"
              and topic_number <= len(get_all_topics_from_table('technologies'))
              and message.text != "Обрати випадкову тему👏"):
            topic_info = get_topic_by_number('technologies', topic_number)
            global_table_name = 'technologies'
            await send_topic_info(message, topic_info)
        elif (prev_message == "Приклади розумних міст у світі 🌆"
              and topic_number <= len(get_all_topics_from_table('cities'))
              and message.text != "Обрати випадкову тему👏"):
            topic_info = get_topic_by_number('cities', topic_number)
            global_table_name = 'cities'
            await send_topic_info(message, topic_info)
        else:
            await message.answer("Теми з таким номером у моїх записах немає😓. Будь ласка, введіть коректний номер теми.")
    else:
        if (message.text == "Обрати випадкову тему👏"
              and prev_message == "Основні концепції розумних міст 1️⃣ 2️⃣ 3️⃣"):
            topic_info = get_random_topic_from_table('basic')
            global_table_name = 'basic'
            global_topic_num = topic_info[0]
            await send_topic_info(message, topic_info)
        elif (message.text == "Обрати випадкову тему👏"
              and prev_message == "Технології, які використовуються в розумних містах 🧑‍💻"):
            topic_info = get_random_topic_from_table('technologies')
            global_table_name = 'technologies'
            global_topic_num = topic_info[0]
            await send_topic_info(message, topic_info)
        elif (message.text == "Обрати випадкову тему👏"
              and prev_message == "Приклади розумних міст у світі 🌆"):
            topic_info = get_random_topic_from_table('cities')
            global_table_name = 'cities'
            global_topic_num = topic_info[0]
            await send_topic_info(message, topic_info)
        else:
            await message.answer("Теми з таким номером у моїх записах немає😓. Будь ласка, введіть коректний номер теми.")


@dp.message_handler(lambda message: message.text
                    and message.text in ["👍 Лайк",
                                         "👎 Дизлайк",
                                         "➡️ Далі"])
async def h_button_click(message: types.Message):
    button = message.text

    if button == "👍 Лайк":
        like(global_table_name, global_topic_num)
    elif button == "👎 Дизлайк":
        dislike(global_table_name, global_topic_num)
    elif button == "➡️ Далі":
        await message.answer("↘️↘️↘️")

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("/activities"))
    markup.add(KeyboardButton("Обрати випадкову тему👏"))
    markup.add(KeyboardButton("❌Завершити❌"))

    await message.answer("Якщо ти хочеш дізнатися про ще одну з тему з цього розділу, то можеш "
                         "просто ввести номер потрібної теми або натиснути кнопку випадкового вибору теми"
                         "👌. \nЯкщо ти хочеш дізнатися про теми з іншого розділу, то обери "
                         "іншу тему за допомогою першої кнопки з командою /activities ✅\n"
                         "Якщо ти дізнався про все, що тебе цікавило - натисни на кнопку ❌Завершити❌",
                         reply_markup=markup)


@dp.message_handler(lambda message: message.text
                    and message.text in ["❌Завершити❌"])
async def h_button_click(message: types.Message):
    global global_topic_num
    global global_table_name
    global prev_message
    button = message.text

    if button == "❌Завершити❌":
        await message.answer("Завершую...", reply_markup=ReplyKeyboardRemove())

        global_topic_num = 1
        global_table_name = ""
        prev_message = ""

        await message.answer("Тепер оберіть команду, про що б ви хотіли дізнатися наступним (можете "
                             "скористатися командою /help або меню)")


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
