import sqlite3


db = sqlite3.connect('dimacoin9.db')
cur = db.cursor()


async def db_conn():
    cur.execute("CREATE TABLE IF NOT EXISTS triggers_table (name_trigger TEXT PRIMARY KEY, value_trigger TEXT)")
    db.commit()


async def inserts(name, value):
    cur.execute(f'INSERT INTO triggers_table (name_trigger, value_trigger) VALUES(?, ?)', (name, value))
    db.commit()


async def all_name(string):
    name_all = cur.execute(f'SELECT {string} FROM triggers_table').fetchall()
    return name_all


async def value(string, name):
    val = cur.execute(f'SELECT {string} FROM triggers_table WHERE name_trigger = ?', (name,)).fetchall()
    return val