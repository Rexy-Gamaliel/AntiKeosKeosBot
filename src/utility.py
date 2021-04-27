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


# MAIN PROGRAM (SEMENTARA)

exit = False
while (not exit):
    masukan = input("Masukkan:")
    if (masukan == 'exit'):
        exit = True
    else:
        keluarkanOutput1(input)

