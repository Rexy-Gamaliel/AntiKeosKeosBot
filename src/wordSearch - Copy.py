import re
import mysql.connector

#===============================================PATTERN LIST===========================================================
task = "[Tt]ask\s*\d+"
kodeMatkul = "[a-zA-Z]{2}[\d]{4}"
monthAhead = "[\d]+ bulan ke depan"
weekAhead = "[\d]+ minggu ke depan"
dayAhead = "[\d]+ hari ke depan"
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

def InputCommand(input):
    # mengembalikan string yang ditampilkan bot jika input merupakan command untuk menambahkan task
    # asumsi sudah diperiksa dengan isInputCommand(input)
    tanggal = getDate(input)
    matkul = getMatkul(input)
    jenis = getJenis(input)
    topik = getJudul(input)
    try:
        sql = "insert into task (tanggal, kodeMatkul, jenis, judul) values (%s,%s,%s,%s)"
        val = (str(tanggal[0]),str(matkul[0]),str(jenis),str(topik))
        mycursor.execute(sql,val)
        mydb.commit()
        mycursor.execute("SELECT ID FROM task ORDER BY ID DESC LIMIT 1")
        row = mycursor.fetchone()[0]
        s = "[TASK BERHASIL DICATAT]\n(ID: "+str(row)+") "+dateDDMMYYYY(tanggal[0])+" - "+str(matkul[0])+" - "+str(jenis[0])+" - "+str(topik)
        return s
    except:
        return 0

def selesaiCommand(input):
    # mengembalikan string yang ditampilkan bot jika input merupakan command untuk menghapus task yang sudah selesai
    # asumsi sudah diperiksa dengan isSelesaiCommand(input)
    id = getID(input)
    try:
        sql = "DELETE FROM TASK WHERE ID = %s"
        id = (str(id),)
        mycursor.execute(sql,id)
        mydb.commit()
        s = "Yey deadline kamu sudah berkurang 1 (task dengan ID = "+str(id)+" sudah dihapus):D"
    except:
        s = "Task yang dimaksud tidak dikenali, coba cek lagi daftar task"
    finally:
        return s

def updateCommand(input):
    id = getID(input)
    tanggal = getDate(input)
    try:
        sql = "UPDATE TASK SET tanggal = %s WHERE ID = %s"
        val = (str(tanggal[len(tanggal)-1]),str(id))
        mycursor.execute(sql,val)
        mydb.commit()
        s = "Sip, deadline tugas dengan ID = "+str(id)+" berhasil diupdate. Semangat terus!"
    except:
        s = "Task yang dimaksud tidak dikenali, coba cek lagi daftar task"
    finally:
        return s

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

#=============================================COMMAND CHECKER==========================================================
def isAllDeadlineCommand(command):
    #mengembalikan true apabila command menanyakan semua deadline
    return (re.search("(?=.*deadline)(?=.*sejauh ini)", command.lower()) or
            (re.search("(?=.*apa saja)(?=.*deadline)", command.lower())))

def isPeriodDeadlineCommand(command):
    #mengembalikan true apabila command menanyakan deadline di antara dua tanggal
    arr = getDate(command)
    if len(arr) != 2:
        return False
    pattern = jenis + "|deadline"
    return re.search(pattern, command.lower())

def isTodayDeadlineCommand(command):
    #mengembalikan true apabila command menanyakan deadline hari ini
    pattern = jenis + "|deadline"
    return re.search(pattern, command.lower()) and re.search("hari ini", command.lower())

def isHelpCommand(command):
    #mengembalikan true apabila command menanyakan hal yang bisa dilakukan bot
    return (re.search("(?=.*apa)(?=.*bisa)(?=.*asisten)", command.lower()) or
            (re.search("(?=.*apa)(?=.*bisa)(?=.*assistant)", command.lower())) or
            (re.search("(?=.*apa)(?=.*bisa)(?=.*bot)", command.lower())) or
            (re.search("(?=.*apa)(?=.*bisa)(?=.*kamu)", command.lower())))

def isNothingCommand(command):
    #mengembalikan true apabila command tidak valid
    return not (isInputCommand(command) or isSelesaiCommand(command)
                or isAllDeadlineCommand(command) or isPeriodDeadlineCommand(command)
                or isUpdateCommand(command) or isHelpCommand(command))

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
        # print(getJenis(command))
        if (isHelpCommand(command)):
            print("yeee")
        else:
            print("yaaah")

