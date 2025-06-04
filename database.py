import sqlite3
from datetime import datetime

# Connecting to the database (the file will be created if it does not exist)
conn = sqlite3.connect('translations.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS translations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        original TEXT,
        translated TEXT,
        lang_from TEXT,
        lang_to TEXT,
        date TEXT
    )
''')
conn.commit()

# Translation saving function
def save_translation(user_id, original, translated, lang_from, lang_to):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO translations (user_id, original, translated, lang_from, lang_to, date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, original, translated, lang_from, lang_to, date))
    conn.commit()
#It returns the user's last limit translations.
def get_user_history(user_id, limit=5):
    cursor.execute('''
        SELECT original, translated, lang_from, lang_to, date
        FROM translations
        WHERE user_id = ?
        ORDER BY date DESC
        LIMIT ?
    ''', (user_id, limit))
    return cursor.fetchall()