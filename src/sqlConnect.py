import mysql.connector
import itertools

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password", #-----isi dengan password masing-masing
    database="anebo"
)
mycursor = mydb.cursor()

#MENGAMBIL DATA DARI DATABASE

#ALL DATA
mycursor.execute("SELECT * from Task")
result = mycursor.fetchall()
allData = result

#data id
mycursor.execute("SELECT id from Task")
result = mycursor.fetchall()
dataID = list(itertools.chain(*result))

#data tanggal
mycursor.execute("SELECT tanggal from Task")
result = mycursor.fetchall()
dataTanggal = list(itertools.chain(*result))
for i in range(len(dataTanggal)):
    dataTanggal[i] = dataTanggal[i].strftime("%d/%m/20%y")

#data kode mata kuliah
mycursor.execute("SELECT kodeMatkul from Task")
result = mycursor.fetchall()
dataMatkul = list(itertools.chain(*result))

#data jenis task
mycursor.execute("SELECT jenis from Task")
result = mycursor.fetchall()
dataJenis = list(itertools.chain(*result))

#data judul task
mycursor.execute("SELECT jenis from Task")
result = mycursor.fetchall()
dataJudul = list(itertools.chain(*result))

def executeCommandWithFetch(query: str, args=None):
    print("try executing")
    if args == None:
        mycursor.execute(query)
    else:
        mycursor.execute(query, args)
    print("successfully executing")
    mydb.commit()
    return mycursor.fetchall()

def executeCommandWithoutFetch(query: str, args=None):
    if args == None:
        mycursor.execute(query)
    else:
        mycursor.execute(query, args)
    mydb.commit()

if __name__ == '__main__':
    print(allData)
    print(dataID)
    print(dataTanggal)
    print(dataMatkul)
    print(dataJenis)
    print(dataJudul)