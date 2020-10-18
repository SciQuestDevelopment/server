import mysql.connector
import yaml
db = yaml.load(open('../db.yaml'))

db = mysql.connector.connect(
    host = db['mysql_host'],
    port = db['mysql_port'],
    user = db['mysql_user'],
    passwd = db['mysql_password'],
    database = db['mysql_db']
)

mycursor = db.cursor();
mycursor.execute("SELECT * FROM Article ")

myresult =mycursor.fetchall();

for row in myresult:
    print(row)
