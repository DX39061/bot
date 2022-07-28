def db_create_table(conn):
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS questions('
        'question TEXT, '
        'kewords TEXT, '
        'answer TEXT, '
        'required_score TEXT, '
        'last_time TEXT);')


def db_delete(conn, question):
    cur = conn.cursor()
    cur.execute('DELETE from questions WHERE question=?', (question,))
    cur.close()
    conn.commit()


def db_update(conn, question, keywords, answer, required_score, last_time):
    db_delete(conn, question)
    cur = conn.cursor()
    cur.execute('INSERT INTO questions VALUES(?,?,?,?,?)', (question, keywords, answer, required_score, last_time))
    cur.close()
    conn.commit()


def db_select(conn, question):
    cur = conn.cursor()
    cur.execute('SELECT * FROM questions WHERE question == ?', (question,))
    res = cur.fetchall()
    cur.close()
    return res


def db_get_all(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM questions')
    res = cur.fetchall()
    cur.close()
    return res
