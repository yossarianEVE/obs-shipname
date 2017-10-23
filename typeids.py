import sqlite3


def get_typedb_cursor():
    conn = sqlite3.connect('typeids.db', check_same_thread=False)
    return conn.cursor()


def get_name_by_typeid(type_id):
    c = get_typedb_cursor()
    c.execute('SELECT name FROM typeids WHERE id=?', (type_id,))
    res = c.fetchone()
    return res[0]
