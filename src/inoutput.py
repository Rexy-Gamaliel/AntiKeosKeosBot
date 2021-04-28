import mysql.connector
import src.utility as u

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", #-----isi dengan password masing-masing
    database="AntiKeosKeosBot"
)
mycursor = mydb.cursor()

#============================================OUTPUT PROCESSING==========================================================
def allDeadline():
    #mengembalikan string yang berisi daftar seluruh task dari database
    mycursor.execute("SELECT * from Task")
    result = mycursor.fetchall()
    return processOutput(result)

def allDeadlineType(type):
    # mengembalikan string yang berisi daftar seluruh task dengan jenis tertentu dari database
    mycursor.execute("SELECT * from Task where jenis like '{0}'".format(type))
    result = mycursor.fetchall()
    return processOutput(result)

def periodDeadline(tanggal1, tanggal2):
    #mengembalikan string yang berisi daftar task dengan deadline antara tanggal1 hingga tanggal2
    mycursor.execute("SELECT * from Task where tanggal BETWEEN '{0}' AND '{1}'".format(tanggal1,tanggal2))
    result = mycursor.fetchall()
    return processOutput(result)

def periodType(type,tanggal1,tanggal2):
    #mengembalikan string yang berisi daftar task tipe tertentu dengan deadline antara tanggal1 hingga tanggal2
    mycursor.execute("SELECT * from Task where jenis like '{0}' AND tanggal BETWEEN '{1}' AND '{2}'"
                     .format(type,tanggal1,tanggal2))
    result = mycursor.fetchall()
    return processOutput(result)

def daysDeadline(N):
    #mengembalikan string yang berisi daftar task dengan deadline hari ini hingga N hari ke depan
    mycursor.execute("SELECT * from Task where tanggal BETWEEN CURDATE() AND "
                     "DATE_ADD(CURDATE(), INTERVAL {0} DAY)".format(N))
    result = mycursor.fetchall()
    return processOutput(result)

def daysDeadlineType(N, type):
    #mengembalikan string yang berisi daftar task dengan deadline hari ini hingga N hari ke depan
    #dengan jenis task tertentu
    mycursor.execute("SELECT * from Task where tanggal BETWEEN CURDATE() AND "
                     "DATE_ADD(CURDATE(), INTERVAL {0} DAY) AND jenis like '{1}'".format(N,type))
    result = mycursor.fetchall()
    return processOutput(result)

def weeksDeadline(N):
    #mengembalikan string yang berisi daftar task dengan deadline hari ini hingga N minggu ke depan
    mycursor.execute("SELECT * from Task where tanggal BETWEEN CURDATE() AND "
                     "DATE_ADD(CURDATE(), INTERVAL {0} WEEK)".format(N))
    result = mycursor.fetchall()
    return processOutput(result)

def weeksDeadlineType(N,type):
    #mengembalikan string yang berisi daftar task dengan deadline hari ini hingga N minggu ke depan
    #dengan jenis task tertentu
    mycursor.execute("SELECT * from Task where tanggal BETWEEN CURDATE() AND "
                     "DATE_ADD(CURDATE(), INTERVAL {0} WEEK) AND jenis like '{1}'".format(N,type))
    result = mycursor.fetchall()
    return processOutput(result)

def todayDeadline():
    #mengembalikan string yang berisi daftar task yang deadline-nya hari ini
    mycursor.execute("SELECT * from Task where tanggal = CURDATE()")
    result = mycursor.fetchall()
    return processOutput(result)

def todayDeadlineType(type):
    # mengembalikan string yang berisi daftar task yang deadline-nya hari ini dengan jenis task tertentu
    mycursor.execute("SELECT * from Task where tanggal = CURDATE() AND jenis like '{0}'".format(type))
    result = mycursor.fetchall()
    return processOutput(result)

def processOutput(result):
    #mengembalikan string yang berisi daftar task sesuai isi array of tuple result
    output = "[Daftar Deadline]\n"
    if len(result) == 0:
        output += "\n----Tidak ada----\n"
        return output
    for i in range(len(result)):
        output += str(i + 1) + ". " + "(ID:" + str(result[i][0]) + ") "
        output += result[i][1].strftime("%d/%m/20%y - ")
        output += result[i][2] + " - " + result[i][3] + " - " + result[i][4] + "\n"
    return output

def inputCommand(input):
    # mengembalikan string yang ditampilkan bot jika input merupakan command untuk menambahkan task
    # asumsi sudah diperiksa dengan isInputCommand(input)
    tanggal = u.getDate(input)
    matkul = u.getMatkul(input)
    jenis = u.getJenis(input)
    topik = u.getJudul(input)
    try:
        sql = "insert into task (tanggal, kodeMatkul, jenis, judul) values (%s,%s,%s,%s)"
        val = (str(tanggal[0]),str(matkul),str(jenis),str(topik))
        mycursor.execute(sql,val)
        mydb.commit()
        mycursor.execute("SELECT ID FROM task ORDER BY ID DESC LIMIT 1")
        row = mycursor.fetchone()[0]
        s = "[TASK BERHASIL DICATAT]\n(ID: "+str(row)+") "+ u.dateDDMMYYYY(tanggal[0])+" - "+\
            str(matkul)+" - "+str(jenis)+" - "+str(topik)
        return s
    except:
        return "Maaf, sepertinya masukanmu belum benar. "

def deadlineOneTask(input):
    # pastikan ada kata kapan dan ada matkulnya dulu sebelum masuk sini
    matkul = u.getMatkul(input)
    # dapatkan banyak matkul itu di basis data
    sql = "select count(id) from task where kodeMatkul = %s and (jenis = 'tucil' or jenis = 'tubes' or jenis = 'pr')"
    val = (matkul,)
    mycursor.execute(sql,val)
    l = mycursor.fetchone()[0]
    # tampilkan hasil berdasarkan banyak matkul
    if (l == 0):
        return "Hmm, sepertinya task yang kamu maksud tidak ada."
    elif (l == 1):
        sql = "select tanggal from task where kodeMatkul = %s"
        val = (matkul,)
        mycursor.execute(sql,val)
        hasil = mycursor.fetchall()[0]
        return hasil[0].strftime("%d/%m/20%y")
    else:
        sql = "select judul, tanggal from task where kodeMatkul = %s and (jenis = 'tucil' or jenis = 'tubes' or jenis = 'pr')"
        val = (matkul,)
        mycursor.execute(sql,val)
        hasil = mycursor.fetchall()
        #print(hasil)
        s = ""
        i = 0
        for h in hasil:
            s += h[0]
            s += ': '
            s += h[1].strftime("%d/%m/20%y")
            if (i < len(hasil) - 1):
                s += '\n'
            i +=1
        return s

def selesaiCommand(input):
    # mengembalikan string yang ditampilkan bot jika input merupakan command untuk menghapus task yang sudah selesai
    # asumsi sudah diperiksa dengan isSelesaiCommand(input)
    id = u.getID(input)
    # lihat apakah task yang dimaksud ada di relasi task
    mycursor.execute("select count(id) from task where id="+str(id))
    n = mycursor.fetchone()[0]
    if (n != 0):
        sql = "DELETE FROM TASK WHERE ID = %s"
        id = (str(id),)
        mycursor.execute(sql,id)
        mydb.commit()
        s = "Yeyyy, deadline kamu sudah berkurang!! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ \nTask " + str(id[0]) + " berhasil dihapus."
    else:
        s = "Task yang dimaksud tidak dikenali, coba cek lagi daftar task."
    return s

def updateCommand(input):
    #memperbaharui tanggal dari task yang hendak diubah dan mengembalikan pesan sukses/tidaknya perubahan
    id = u.getID(input)
    tanggal = u.getDate(input)
    # cek dulu apakah ada task dengan ID=id di relasi task
    mycursor.execute("select count(id) from task where id="+str(id))
    n = mycursor.fetchone()[0]
    if (n != 0):
        try:
            sql = "UPDATE TASK SET tanggal = %s WHERE ID = %s"
            val = (str(tanggal[len(tanggal)-1]),str(id))
            mycursor.execute(sql,val)
            mydb.commit()
            s = "Sip, deadline tugas dengan ID = "+str(id)+" berhasil diupdate. Semangat terus! ヾ(≧▽≦*)o"
        except:
            s = "Task yang dimaksud tidak dikenali, coba cek lagi daftar task."
        finally:
            return s
    else:
        return "Task yang dimaksud tidak dikenali, coba cek lagi daftar task."

def nothingCommand():
    #mengembalikan string berisi pesan error apabila command tidak dikenali
    s = "Maaf, pesan tidak dikenali."
    return s

def helpCommand():
    #mengembalikan string berisi panduan pengguna untuk mengakses fitur bot
        output = ""
        output += "===================== FITUR =====================\n"
        output += "  \n"
        output += "1. Menambahkan task baru\n"
        output += "2. Melihat daftar task\n"
        output += "3. Menampilkan deadline suatu task tertentu\n"
        output += "4. Memperbaharui task tertentu\n"
        output += "5. Menandai suatu task sudah dikerjakan\n"
        output += "6. Menampilkan opsi help\n"
        output += "  \n"
        output += "============== DAFTAR KATA PENTING ===============\n"
        output += "  \n"
        output += "1. Kuis\n"
        output += "2. Ujian\n"
        output += "3. Tucil\n"
        output += "4. Tubes\n"
        output += "5. PR\n"
        output += "6. Deadline\n"
        output += "7. [N] hari ke depan\n"
        output += "8. [N] minggu ke depan\n"
        output += "9. Hari ini\n"
        output += "10. Sejauh ini\n"
        output += "11. Apa saja\n"
        output += "12. Kapan\n"
        output += "13. Bot\n"
        output += "  \n"
        output += "================ FORMAT PENULISAN ================\n"
        output += "  \n"
        output += "Tanggal            : DD/MM/YYYY\n"
        output += "Kode mata kuliah   : HHAAAA (2 huruf 4 angka\n"

        return output


def outputBot(input):
    #  cek untuk fitur 1
    if (u.isInputCommand(input)):
        s = inputCommand(input)

    # cek untuk fitur 2
    elif (u.isPeriodCommand(input)):
        type = u.getJenis(input)
        tgl1 = u.getDate(input)[0]
        tgl2 = u.getDate(input)[1]
        if (type == -1):
            s = periodType(type,tgl1,tgl2)
        else:
            s = periodDeadline(tgl1,tgl2)

    elif (u.isWeeksCommand(input)):
        type = u.getJenis(input)
        N = u.getWeeks(input)
        if (type == -1):
            s = weeksDeadline(N)
        else:
            s = weeksDeadlineType(N,type)

    elif (u.isDaysCommand(input)):
        type = u.getJenis(input)
        N = u.getDays(input)
        if (type == -1):
            s = daysDeadline(N)
        else:
            s = daysDeadlineType(N, type)
            
    elif (u.isTodayCommand(input)):
        type = u.getJenis(input)
        if (type == -1):
            s = todayDeadline()
        else:
            s = todayDeadlineType(type)

    elif (u.isAllCommand(input)):
        type = u.getJenis(input)
        if (type == -1):
            s = allDeadline()
        else:
            s = allDeadlineType(type)

    # cek untuk fitur 3
    elif (u.isKapanCommand(input)):
        s = deadlineOneTask(input)

    # cek untuk fitur 4
    elif (u.isUpdateCommand(input)):
        s = updateCommand(input)

    # cek untuk fitur 5
    elif (u.isSelesaiCommand(input)):
        s = selesaiCommand(input)

    # cek untuk fitur 6
    elif (u.isHelpCommand(input)):
        s = helpCommand()

    # cek untuk fitur 7 : mendefinisikan list kata penting

    # cek untuk fitur 8 
    else:
        s = nothingCommand()
    return s


if __name__ == '__main__':
    while (True):
        command  = input("Masukkan command: ")
        s = outputBot(command)
        print(s)