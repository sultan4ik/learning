import sqlite3
import pprint
connection = sqlite3.connect('../test_2.db')
cursor = connection.cursor()
cursor.execute("create table switch (mac text not NULL primary key, hostname text, model text, location text)")
data = [('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'), ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'), ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'), ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]
query = "insert into switch values (?, ?, ?, ?)"
data_2 = [('0000.1111.0001', 'sw5', 'Cisco 3750', 'London, Green Str'), ('0000.1111.0002', 'sw6', 'Cisco 3750', 'London, Green Str'), ('0000.1111.0003', 'sw7', 'Cisco 3750', 'London, Green Str'), ('0000.1111.0004', 'sw8', 'Cisco 3750', 'London, Green Str')]
cursor.executemany(query, data_2)
for row in data:
    cursor.execute(query, row)
cursor.execute('select * from switch')
print(cursor.fetchone())
pprint(cursor.fetchmany(3))
pprint(cursor.fetchall())
connection.commit()