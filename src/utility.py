# FUNGSI DAN PROSEDUR UNTUK KMP
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

# FUGSI DAN PROSEDUR UNTUK . . .
# alternatif 1
def keluarkanOutput1(input):
    success = False
    # dapatkan dulu apakah input untuk menandai task selesai dikerjakan: ada kata "sudah"
    if (isTandaiSelesaiCommand(input)):
        success = tandaiSelesai(input)
    else:
        # dapatkan dulu apakah input kira2 meminta menu help - ada kata "bisa"
        if (isHelpCommand(input)):
            success = tampilkanHelp()
        else:
            # dapatkan dulu apakah input kira2 merupakan command untuk memperbarui deadline - ada kata "jadi"
            if (isPerbaruiTaskCommand(input)):
                success = perbaruiTask(input)
            else:
                # dapatkan dulu apakah input kira2 merupakan command untuk melihat daftar task - ada kata "apa saja"
                if (isLihatDaftarTaskCommand(input)):
                    success = tampilkanDaftarTask(input)
                else:
                    # dapatkan apa ada tanggal - artinya menambahkan task baru
                    if (isAdaTanggal(input)):
                        success = tambahkanTaskBaru(input)
                    else:
                        success = tampilkanDeadlineTaskTertentu(input)
    if (not success):
        showErrorMessage()

# alternatif 2
def keluarkanOutput2(input):
    nomenu = 0
    # dapatkan dulu apakah input untuk menandai task selesai dikerjakan: ada kata "sudah"
    if (isTandaiSelesaiCommand(input)):
        nomenu = tandaiSelesai(input) # kalau sukses return 5
    # dapatkan dulu apakah input kira2 merupakan command untuk melihat daftar deadline: ada kata "apa saja"
    if (nomenu == 0 and isLihatDaftarDeadlineCommand(input)):
        nomenu = daftarTask(input) # kalau sukses return 2
    # dapatkan apakah command kira2 untuk mendapatkan help: ada kata "bisa"
    if (nomenu == 0 and isHelpCommand(input)):
        nomenu = 6   
    # dapatkan apakah command kira2 untuk memperbarui task baru: ada kata -jadi atau -diundur atau -dimajukan...
    if (nomenu == 0 and isPerbaruiTaskCommand(input)):
        nomenu = perbaruiTask(input)
    # lihat apakah command kira2 ingim menambahkan task baru : ada tanggalnya (ingat disini sisa 2 lagi menu yang belum)
    if (nomenu == 0 and isAdaTanggal(input)):
        nomenu == tambahkanTaskBaru(input)            
    if (nomenu == 0 and isAdaKataDeadline(input)):
        nomenu == deadlineTaskTertentu(input)
    return nomenu       
                    
        

# MAIN PROGRAM (SEMENTARA)

exit = False
while (not exit):
    masukan = input("Masukkan:")
    if (masukan == 'exit'):
        exit = True
    else:
        keluarkanOutput1(input)

exit = False
while (not exit):
    masukan = input("Masukkan:")
    if (masukan == 'exit'):
        exit = True
    else:
        command = keluarkanOutput2(input)
        if (command == 0):
            showErrorMessage()

