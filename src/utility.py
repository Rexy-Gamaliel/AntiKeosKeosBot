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

lps = getLPS("onions")
print(lps)
a = KMPMatch("onions","onionionspl")
print(a)

