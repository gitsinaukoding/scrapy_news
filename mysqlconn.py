import MySQLdb as sql

hostname = 'localhost'
username = 'root'
password = ''
database = 'scrapingnews'

sqlconn = sql.connect( host=hostname, user=username, passwd=password, db=database, charset="utf8",use_unicode=True )
cursor = sqlconn.cursor()


# print(sqlconn)

def insert(val):
    sql = "INSERT INTO contents (title, thumbnail, content, date, clock) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, val)

    sqlconn.commit()