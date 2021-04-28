import re
#===============================================PATTERN LIST===========================================================
task = "[Tt]ask\s*\d+"
kodeMatkul = "[a-zA-Z]{2}[\d]{4}"
weeks1 = "^[\d]+ minggu ke depan"
weeks2 = "[\s][\d]+ minggu ke depan"
days1 = "[\s][\d]+ hari ke depan"
days2 = "^[\d]+ hari ke depan"
tanggal = r'(((0[1-9]|1\d|2\d|3[0-1])/(0[13578]|1[02])|((0[1-9]|[12]\d|30)/(0[469]|11)))' \
          r'/20\d{2}|((0[1-9]|[12]\d)/02/20([02468][048]|[13579][26]))|((0[1-9]|1\d|2[0-8])' \
          r'/02/20([02468][1235679]|[13579][01345789])))'
jenis = "kuis|uts|uas|tubes|tucil|pr"
judul = r"([Tt]opik([\s][a-zA-Z]+)+)"

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
    #mengembalikan indeks dari karakter petama string matching antara pattern dengan text
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

def getDays(command):
    #mengembalikan N dari klausa "N hari ke depan"
    hasil = re.findall(days1, command)
    hasil += re.findall(days2, command)
    if len(hasil) == 0:
        return -1
    words = hasil[0].split()
    return words[0]

def getWeeks(command):
    #mengembalikan N dari klausa "N minggu ke depan"
    hasil = re.findall(weeks1, command)
    hasil += re.findall(weeks2, command)
    if len(hasil) == 0:
        return -1
    words = hasil[0].split()
    return words[0]

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


#============================================== COMMAND CHECKER ========================================================
def isInputCommand(input):
    # mengecek apakah input adalah command untuk menambahkan task
    input = input.lower()
    hasil = (len(getDate(input))==1 and (getMatkul(input)!= -1) and (getJenis(input) != -1)
            and getJudul(input) != -1)
    return hasil

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

def isAllCommand(command):
    command = command.lower()
    pattern = jenis + "|deadline"
    #mengembalikan true apabila command menanyakan semua deadline
    return re.search(pattern, command) and ((KMPMatch("sejauh ini", command) != -1
            or KMPMatch("apa saja", command) != -1))

def isPeriodCommand(command):
    #mengembalikan true apabila command menanyakan deadline di antara dua tanggal
    arr = getDate(command)
    if len(arr) != 2:
        return False
    pattern = jenis + "|deadline"
    return re.search(pattern, command.lower())

def isDaysCommand(command):
    #mengembalikan true apabila command menanyakan deadline N hari ke depan
    if getDays(command) == -1:
        return False
    pattern = jenis + "|deadline"
    return re.search(pattern, command.lower())

def isWeeksCommand(command):
    #mengembalikan true apabila command menanyakan deadline N hari ke depan
    if getWeeks(command) == -1:
        return False
    pattern = jenis + "|deadline"
    return re.search(pattern, command.lower())

def isTodayCommand(command):
    #mengembalikan true apabila command menanyakan deadline hari ini
    pattern = jenis + "|deadline"
    return re.search(pattern, command.lower()) and KMPMatch("hari ini", command.lower()) != -1

def isKapanCommand(command):
    #mengembalikan true apabila command menanyakan kapan deadline dari suatu task
    return (KMPMatch("kapan", command.lower()) != -1) and (KMPMatch("deadline", command.lower()) != -1) \
           and (getMatkul(command) != -1)

def isHelpCommand(command):
    #mengembalikan true apabila command menanyakan hal yang bisa dilakukan bot
    return (KMPMatch("apa", command.lower()) != -1) and (KMPMatch("bisa", command.lower()) != -1) \
           and (KMPMatch("bot", command.lower()) != -1)

def isNothingCommand(command):
    #mengembalikan true apabila command tidak valid
    return not (isInputCommand(command) or isSelesaiCommand(command)
                or isAllCommand(command) or isPeriodCommand(command)
                or isUpdateCommand(command) or isHelpCommand(command))


if __name__ == '__main__':
    while True:
        command = input("Masukkan command: ")
        # print(getWeeks(command))
        if isAllCommand(command):
            print("yaps")
        else:
            print("nah")
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
