import mysql.connector
import itertools

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", #-----isi dengan password masing-masing
    database="AntiKeosKeosBot"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT kodeMatkul from Task")
result = mycursor.fetchall()
kodeMatkul = list(itertools.chain(*result))
print(kodeMatkul)