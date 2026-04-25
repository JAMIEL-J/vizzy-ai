import sqlite3, os
conn = sqlite3.connect('data/vizzy.db')
cur = conn.cursor()
rows = cur.execute('select id, created_at from datasets order by created_at desc limit 20').fetchall()
for i, c in rows:
    print(str(i) + '\t' + str(c) + '\t' + str(os.path.exists(os.path.join('data','uploads',i))))
