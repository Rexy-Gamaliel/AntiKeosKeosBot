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

#====================================== STRING MATCHING ALGORITHMS =====================================================
def compPrefSuf(word, length):
    #mengembalikan true apabila prefix dan sufix sepanjang length sama
    pref = ''
    suf = ''
    for i in range(length):
        pref += word[i]
    for i in range(len(word)-length,len(word)):
        suf += word[i]
    return (pref == suf)

def getPref(word, len):
    #mengembalikan prefix sepanjang len dari sebuah string word
    pref = ''
    for i in range(len):
        pref += word[i]
    return pref

def getLPS(pat):
    #mengembalikan array yang memuat jumlah irisan terbesar antara prefix dan suffix
    length = len(pat)
    lps = [0 for _ in range(length)]
    for i in range(1,length):
        curr = getPref(pat,i+1)
        max = 0
        for j in range(i):
            if compPrefSuf(curr,j):
                max = j
        lps[i] = max
    return lps

def KMPMatch(pattern, text):
    n = len(text)
    m = len(pattern)
    fail = getLPS(pattern)
    i=0
    j=0
    while (i < n):
        if (text[i]==pattern[j]):
            if (j == m-1):
                return (i-m+1)
            i+=1
            j+=1
        elif (j > 0):
            j = fail[j-1]
        else:
            i+=1
    return -1

#============================================== COMMAND CHECKER ========================================================
def isInputCommand(input):
    # mengecek apakah input adalah command untuk menambahkan task
    return (len(getDate(input))==1 and len(getMatkul(input))== 1 and len(getJenis(input)) == 1
            and getJudul(input) != -1)

def isSelesaiCommand(input):
    # mengecek apakah input adalah command untuk menghapus task yang sudah selesai
    input = input.lower()
    return ((KMPMatch("udah",input) != -1 or KMPMatch("selesai",input) != -1 or KMPMatch("siap",input) != -1)
            and (getID(input) != -1))

def isUpdateCommand(input):
    # mengecek apakah input adalah command untuk mengupdate deadline task
    input = input.lower()
    return ((KMPMatch("jadi",input) != -1 or KMPMatch("undur", input) != -1 or KMPMatch("maju",input) != -1)
            and (getID(input) != -1) and (len(getDate(input)) > 0))

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

def periodType(type,tanggal1,tanggal2):
    #mengembalikan string yang berisi daftar task dari tanggal1 hingga tanggal2
    query = "SELECT * from Task where jenis like '{0}' AND tanggal BETWEEN '{1}' AND '{2}'".format(type,tanggal1,tanggal2)
    print(query)
    mycursor.execute("SELECT * from Task where jenis like '{0}' AND tanggal BETWEEN '{1}' AND '{2}'".format(type,tanggal1,tanggal2))
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

def inputCommand(input):
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
        s = "[TASK BERHASIL DICATAT]\n(ID: "+str(row)+") "+dateDDMMYYYY(tanggal[0])+" - "+\
            str(matkul[0])+" - "+str(jenis[0])+" - "+str(topik)
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

def nothingCommand():
    s = "Maaf, pesan tidak dikenali"
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

def dateDDMMYYYY(date):
    # mengembalikan date berformat DD/MM/YYYY dari masukan yang YYYY/MM/DD
    d = ""
    m = ""
    y = ""
    i = 0
    while (date[i] != '/'):
        y += date[i]
        i+=1
    i+=1
    while (date[i] != '/'):
        m += date[i]
        i +=1
    i +=1
    m += '/'
    while(i < len(date)):
        d += date[i]
        i +=1
    d += '/'
    d += m
    d += y
    return d


if __name__ == '__main__':
    print(periodType('uas','2021-04-02','2021-05-22'))
    # while True:
    #     command = input("Masukkan command: ")
    #     # print(re.findall(tanggal,command))
    #     # print(re.findall(judul,command))
    #     # print(getJudul(command))
    #     # print(allDeadline())
    #     # print(processOutput([]))
    #     # print(getDate(command))
    #     # print(getMatkul(command))
    #     print(getJenis(command))
    #     up = updateCommand("deadline task   28 diganti jadi tanggal 20/12/2021")
    #     print(up)

    while True:
        # dapatkan masukan command
        command = input("Masukkan command: ")

        # proses command
        if (isInputCommand(command)):
            s = inputCommand(command)
        elif (isUpdateCommand(command)):
            s = updateCommand(command)
        elif (isSelesaiCommand(command)):
            s = selesaiCommand(command)
        else:
            s = nothingCommand()

        # tampilkan hasil proses ke layar



