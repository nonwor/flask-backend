import sqlite3

conn = sqlite3.connect('test.db')

cursor = conn.cursor()

# This is for creating a table, so after we created this we don't need to call it again.

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')

usernames = [
    'alice123',
    'bob456',
    'charlie789',
    'david_23',
    'emma567',
    'frank_89',
    'grace34',
    'henry_12',
    'isabel45',
    'jackie67',
    'kate_78',
    'leo123',
    'mia_56',
    'nathan89',
    'olivia_23',
    'peter456',
    'quinn_78',
    'rachel_34',
    'sam567'
]

emails = [
    'alice123@example.com',
    'bob456@example.com',
    'charlie789@example.com',
    'david_23@example.com',
    'emma567@example.com',
    'frank_89@example.com',
    'grace34@example.com',
    'henry_12@example.com',
    'isabel45@example.com',
    'jackie67@example.com',
    'kate_78@example.com',
    'leo123@example.com',
    'mia_56@example.com',
    'nathan89@example.com',
    'olivia_23@example.com',
    'peter456@example.com',
    'quinn_78@example.com',
    'rachel_34@example.com',
    'sam567@example.com'
]

for i in range(len(emails)):
	print(usernames[i],emails[i])
	cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (usernames[i], emails[i]))

conn.commit()
conn.close()


