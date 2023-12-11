import random
from questions import questions_list
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

question_num = 0
random_questions = []


async def question_engine(message: types.Message):
    global question_num  # Объявляем переменную как глобальную

    options = ["Варіант 1", "Варіант 2", "Варіант 3", "Варіант 4"]

    question = random_questions[question_num]
    question_num = question_num + 1
    question_text, answer_1, answer_2, answer_3, answer_4, right_answer = question

    # Создаем клавиатуру с двумя рядами по две кнопки
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    # Добавляем кнопки в клавиатуру
    markup.add(KeyboardButton(options[0]), KeyboardButton(options[1]))
    markup.add(KeyboardButton(options[2]), KeyboardButton(options[3]))

    # Отправляем вопрос и варианты ответов
    await message.answer(f"Питання №{question_num}\n"
                         f"{question_text}\n\n{answer_1}\n{answer_2}\n{answer_3}\n{answer_4}"
                         , reply_markup=markup)


async def test_end_handler(message: types.Message, answered_questions, right_answered_questions):

    right_answers_percent = (right_answered_questions/answered_questions)*100

    main_message_part = f"Вітаю, Ви завершили тест. Кількість правильних відповідей:\n{right_answered_questions} з {answered_questions}"
    last_part = (f"\nДля проходження тестування повторно введіть команду /quiz, або введіть іншу команду, що"
                 f" вас цікавть🤔")
    if right_answers_percent == 100:
        additional_part = ("\nВідмінний результат🤯! Ти - справжній експерт у темі розумних міст, навіть мені є чого"
                           " у тебе навчитися😎")
        await message.answer(main_message_part + additional_part + last_part, reply_markup=ReplyKeyboardRemove())
    elif right_answers_percent >= 70:
        additional_part = "\nЧудовий результат, але наступного разу варто докласти трошки більше зусилль😉"
        await message.answer(main_message_part + additional_part + last_part, reply_markup=ReplyKeyboardRemove())
    elif right_answers_percent >= 50:
        additional_part = "\nНепоганий результат, але тобі ще є чому повчитися😇"
        await message.answer(main_message_part + additional_part + last_part, reply_markup=ReplyKeyboardRemove())
    elif right_answers_percent >= 30:
        additional_part = ("\nВідсоток правильних відповідей менше ніж неправильних😅. Можу допомогти"
                           " тобі з вивченням теми Розумних міст за допомогою своїх невеличких статтей")
        await message.answer(main_message_part + additional_part + last_part, reply_markup=ReplyKeyboardRemove())
    elif right_answers_percent >= 1:
        additional_part = ("\nДуууже мало правильних відповідей 😱. Можу допомогти"
                           " тобі з вивченням теми Розумних міст за допомогою своїх невеличких статтей")
        await message.answer(main_message_part + additional_part + last_part, reply_markup=ReplyKeyboardRemove())
    elif right_answers_percent == 0:
        additional_part = ("\nЦе просто неймовірно, оскільки вірогідність цього справді мала. Можливо"
                           " ти зробив це спеціально?🙃")
        await message.answer(main_message_part + additional_part + last_part, reply_markup=ReplyKeyboardRemove())


def questions_handler(requirable_questions):
    global random_questions
    if requirable_questions == 5:
        random_questions = random.sample(questions_list, 5)
        return random_questions
    elif requirable_questions == 10:
        random_questions = random.sample(questions_list, 10)
        return random_questions
    elif requirable_questions == 15:
        random_questions = random.sample(questions_list, 15)
        return random_questions


def reset_quiz():
    global question_num
    global random_questions
    question_num = 0
    random_questions = []
