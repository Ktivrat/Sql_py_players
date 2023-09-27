import sqlite3


with sqlite3.connect('gamedb.db') as con:
    cur = con.cursor()

    # players
    cur.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            best_score INTEGER NOT NULL
        );
    ''')

    # games
    cur.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL,
            id_player INTEGER NOT NULL,
            FOREIGN KEY (id_player) REFERENCES players(id)
        );
    ''')

    # Данные в таблицу "players"
    cur.executemany('INSERT INTO players (name, best_score) VALUES (?, ?)',
    [
        ("Миша", 200),
        ("Ваня", 154),
        ("Дима", 178),
        ("Коля", 210)
    ])

    # Данные в таблицу "games"
    cur.executemany('INSERT INTO games (name, score, id_player) VALUES (?, ?, ?)', 
    [
        ("Миша", 110, 1),
        ("Миша", 200, 1),
        ("Дима", 178, 3),
        ("Коля", 10, 4),
        ("Коля", 30, 4),
        ("Коля", 40, 4),
        ("Ваня", 154, 2),
        ("Коля", 210, 4)
    ])

    ################################## Вывод #########################################

    # Игроки и их кол-во игр
    cur.execute('''
        SELECT players.name, COUNT(games.id) AS games_played
        FROM players
        LEFT JOIN games ON players.id = games.id_player
        GROUP BY players.name;
    ''')
    print("Игроки и их кол-во игр:")
    for row in cur.fetchall():
        print(row)

    # Игроки и их итоговый счет за все сыгранные игры
    cur.execute('''
        SELECT players.name, SUM(games.score) AS total_score
        FROM players
        LEFT JOIN games ON players.id = games.id_player
        GROUP BY players.name;
    ''')
    print("\nИгроки и их итоговый счет за все сыгранные игры:")
    for row in cur.fetchall():
        print(row)

    # Худший результат у каждого игрока
    cur.execute('''
        SELECT players.name, MIN(games.score) AS worst_score
        FROM players
        LEFT JOIN games ON players.id = games.id_player
        GROUP BY players.name;
    ''')
    print("\nХудший результат у каждого игрока:")
    for row in cur.fetchall():
        print(row)
        
        