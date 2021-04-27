import re
import mysql.connector

#===============================================PATTERN LIST===========================================================
task = "[Tt]ask\s*\d+"
kodeMatkul = "[a-zA-Z]{2}[\d]{4}"
monthAhead = "[\d]+ bulan ke depan"
weekAhead = "[\d]+ minggu ke depan"
dayAhead = "[\d]+ hari ke depan"
today = "hari ini"
all = "sejauh ini"
when = "kapan"
tanggal = r'(((0[1-9]|1\d|2\d|3[0-1])/(0[13578]|1[02])|((0[1-9]|[12]\d|30)/(0[469]|11)))' \
          r'/20\d{2}|((0[1-9]|[12]\d)/02/20([02468][048]|[13579][26]))|((0[1-9]|1\d|2[0-8])' \
          r'/02/20([02468][1235679]|[13579][01345789])))'
jenis = "kuis|uts|uas|tubes|tucil|pr"
judul = r"([Tt]opik([\s][a-zA-Z]+)+)"

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="132435", #-----isi dengan password masing-masing
    database="AntiKeosKeosBot"
)
mycursor = mydb.cursor()

#============================================OUTPUT PROCESSING==========================================================
def allDeadline():
    #mengembalikan string yang berisi daftar seluruh task dari database
    mycursor.execute("SELECT * from Task")
    result = mycursor.fetchall()
    return(processOutput(result))

def periodDeadline(tanggal1, tanggal2):
    #mengembalikan string yang berisi daftar task dari tanggal1 hingga tanggal2
    mycursor.execute("SELECT * from Task where tanggal BETWEEN '{0}' AND '{1}'".format(tanggal1,tanggal2))
    result = mycursor.fetchall()
    return(processOutput(result))

def processOutput(result):
    #mengembalikan string yang berisi daftar task sesuai isi array of tuple result
    output = "[Daftar Deadline]\n"
    if len(result) == 0:
        output += "\n-----Kosong-----\n"
        return output
    for i in range(len(result)):
        output += str(i + 1) + ". " + "(ID:" + str(result[i][0]) + ") "
        output += result[i][1].strftime("%d/%m/20%y - ")
        output += result[i][2] + " - " + result[i][3] + " - " + result[i][4] + "\n"
    return output

#============================================WORDS GETTER===============================================================
def getMatkul(command):
    #mengembalikan kode mata kuliah yang terdapat pada command
    arr = re.findall(kodeMatkul,command)
    if len(arr) == 0:
        return -1
    else:
        return arr[0]

def getJenis(command):
    #mengembalikan jenis task yang terdapat pada command
    arr = re.findall(jenis,command.lower())
    if len(arr) == 0:
        return -1
    else:
        return arr[0]

def getJudul(command):
    #mengembalikan topik dari task yang terdapat pada command
    result = re.findall(judul,command)
    if len(result)==0:
        return -1
    title = result[0][0]
    title = re.sub(jenis,"", title)
    title = re.sub(tanggal,"", title)
    title = re.sub(kodeMatkul, "", title)
    title = re.sub("[Tt]opik ", "", title)
    return title

def getDate(input):
    #mengembalikan tanggal yang terdapat pada command
    temp = []
    hasil = []
    pattern = re.compile(tanggal)
    matches = pattern.finditer(input)
    for match in matches:
        temp.append(match.group(0))
    for t in temp:
        d = ""
        m = ""
        y = ""
        i = 0
        while (t[i] != '/'):
            d += t[i]
            i+=1
        i+=1
        while (t[i] != '/'):
            m += t[i]
            i +=1
        m += '/'
        i+=1
        while (i < len(t)):
            y += t[i]
            i +=1
        y += '/'
        y += m
        y += d
        hasil.append(y)
    return hasil

def getID(input):
    #mengembalikan ID task yang terdapat pada command
    hasil = re.findall(task, input)
    a = 0
    if len(hasil) == 0:
        return -1
    for i in range(len(hasil[0])):
        if (ord(hasil[0][i]) > ord('9') or ord(hasil[0][i]) < ord('0')):
            i+=1
        else:
            a = 10*a + int(hasil[0][i])
    return a


if __name__ == '__main__':
    while True:
        command = input("Masukkan command: ")
        # print(re.findall(tanggal,command))
        # print(re.findall(judul,command))
        # print(getJudul(command))
        # print(allDeadline())
        # print(processOutput([]))
        # print(getDate(command))
        # print(getMatkul(command))
        print(getJenis(command))


