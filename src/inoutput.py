import mysql.connector
import src.utility as u

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

def weeksDeadline(N):
    #mengembalikan string yang berisi daftar task dengan deadline hari ini hingga N minggu ke depan
    mycursor.execute("SELECT * from Task where tanggal BETWEEN CURDATE() AND "
                     "DATE_ADD(CURDATE(), INTERVAL {0} WEEK)".format(N))
    result = mycursor.fetchall()
    return processOutput(result)

def todayDeadline():
    #mengembalikan string yang berisi daftar task yang deadline-nya hari ini
    mycursor.execute("SELECT * from Task where tanggal = CURDATE()")
    result = mycursor.fetchall()
    return(processOutput(result))

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
        val = (str(tanggal[0]),str(matkul[0]),str(jenis),str(topik))
        mycursor.execute(sql,val)
        mydb.commit()
        mycursor.execute("SELECT ID FROM task ORDER BY ID DESC LIMIT 1")
        row = mycursor.fetchone()[0]
        s = "[TASK BERHASIL DICATAT]\n(ID: "+str(row)+") "+ u.dateDDMMYYYY(tanggal[0])+" - "+\
            str(matkul[0])+" - "+str(jenis[0])+" - "+str(topik)
        return s
    except:
        return 0

def selesaiCommand(input):
    # mengembalikan string yang ditampilkan bot jika input merupakan command untuk menghapus task yang sudah selesai
    # asumsi sudah diperiksa dengan isSelesaiCommand(input)
    id = u.getID(input)
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
    id = u.getID(input)
    tanggal = u.getDate(input)
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


if __name__ == '__main__':
    print(todayDeadline())
    print(weeksDeadline(0))
    #print(periodType('uas','2021-04-02','2021-05-22')
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

    # while True:
    #     # dapatkan masukan command
    #     command = input("Masukkan command: ")
    #
    #     # proses command
    #     if (u.isInputCommand(command)):
    #         s = inputCommand(command)
    #     elif (u.isUpdateCommand(command)):
    #         s = updateCommand(command)
    #     elif (u.isSelesaiCommand(command)):
    #         s = selesaiCommand(command)
    #     else:
    #         s = nothingCommand()

        # tampilkan hasil proses ke layar



