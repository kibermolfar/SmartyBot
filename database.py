import random
import sqlite3

# Создание базы данных и таблицы
conn = sqlite3.connect('topics.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS basic_concepts_topics')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS basic (
        id INTEGER PRIMARY KEY,
        title TEXT,
        image_url TEXT,
        description TEXT,
        likes INTEGER,
        dislikes INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS technologies (
        id INTEGER PRIMARY KEY,
        title TEXT,
        image_url TEXT,
        description TEXT,
        likes INTEGER,
        dislikes INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY,
        title TEXT,
        image_url TEXT,
        description TEXT,
        likes INTEGER,
        dislikes INTEGER
    )
''')

conn.commit()
# cursor.execute('DELETE FROM cities WHERE id = 1')
# conn.commit()
# cursor.execute('DELETE FROM cities WHERE id = 9')
# conn.commit()

# new_description = """Копенгаген — столиця Данії та одне з найрозумніших міст світу. Місто відоме своїми інноваційними підходами до використання технологій для покращення якості життя своїх громадян, зробити місто більш безпечним, екологічним і економічно ефективним.
# Копенгаген також є піонером у галузі розумних будівель. Місто має амбітну мету зробити всі свої будівлі більш енергоефективними до 2040 року. Для цього Копенгаген використовує такі технології, як розумне освітлення та керування HVAC.
# Система розумного освітлення: У Копенгагені понад 200 000 вуличних ліхтарів підключені до системи розумного освітлення.
# Система розумного паркування: У Копенгагені понад 100 000 паркувальних місць підключені до системи розумного паркування.
# Система розумного громадського транспорту: У Копенгагені понад 2000 автобусів і 1000 трамваїв підключені до системи розумного громадського транспорту."""
#
# cursor.execute('UPDATE cities SET description = ? WHERE id = ?', (new_description, 7))
# conn.commit()

# # Вставка данных
# cursor.execute('''
#     INSERT INTO cities (id, title, image_url, description, likes, dislikes)
#     VALUES (?, ?, ?, ?, ?, ?)
# ''', (9, 'Окленд, Нова Зеландія', 'TopicsPictures/CitiesPictures/Окленд.jpg', description, 0, 0))
#
# conn.commit()

cursor.execute('SELECT * FROM cities')
topics1 = cursor.fetchall()

for topic in topics1:
    print(topic)

# Закрытие соединения
conn.close()


def get_all_topics_from_table(table_name):
    # Подключение к базе данных
    conn = sqlite3.connect('topics.db')
    cursor = conn.cursor()

    # Выполнение SQL-запроса
    cursor.execute(f'SELECT title FROM {table_name}')

    # Получение результатов запроса
    topics = [row[0] for row in cursor.fetchall()]

    # Закрытие соединения с базой данных
    conn.close()

    return topics


def get_random_topic_from_table(table_name):
    topics = get_all_topics_from_table(table_name)
    rand_topic = random.randint(1, len(topics))
    topic_info = get_topic_by_number(table_name, rand_topic)
    if topic_info:
        return topic_info
    else:
        return None


def get_topic_by_number(table_name, topic_number):
    # Подключение к базе данных
    conn = sqlite3.connect('topics.db')
    cursor = conn.cursor()

    # Выполнение SQL-запроса для извлечения информации о теме по номеру
    cursor.execute(f'SELECT id, title, image_url, description, likes, dislikes FROM {table_name} WHERE id = ?',
                   (topic_number,))

    # Извлечение результата запроса
    topic_info = cursor.fetchone()
    topic_list = list(topic_info)
    topic_list.append(table_name)

    # Закрытие соединения с базой данных
    conn.close()

    # Вернуть информацию о теме в виде строки
    if topic_list:
        return topic_list
    else:
        return None


def like(table_name, topic_id):
    # Подключение к базе данных
    conn = sqlite3.connect('topics.db')
    cursor = conn.cursor()

    # Получаем текущее значение likes
    cursor.execute(f'SELECT likes FROM {table_name} WHERE id = ?', (topic_id,))
    current_likes = cursor.fetchone()

    if current_likes:
        new_likes = current_likes[0] + 1
        cursor.execute(f'UPDATE {table_name} SET likes = ? WHERE id = ?', (new_likes, topic_id))
        conn.commit()
        conn.close()
        return new_likes
    else:
        conn.close()
        return None


def dislike(table_name, topic_id):
    # Подключение к базе данных
    conn = sqlite3.connect('topics.db')
    cursor = conn.cursor()

    # Получаем текущее значение likes
    cursor.execute(f'SELECT dislikes FROM {table_name} WHERE id = ?', (topic_id,))
    current_dislikes = cursor.fetchone()

    if current_dislikes:
        new_dislikes = current_dislikes[0] + 1
        cursor.execute(f'UPDATE {table_name} SET dislikes = ? WHERE id = ?', (new_dislikes, topic_id))
        conn.commit()
        conn.close()
        return new_dislikes
    else:
        conn.close()
        return None
