import re
import mysql.connector
import itertools

#LIST PATTERN
task = "task\s\d+"
kodeMatkul = "[a-zA-Z]{2}[\d]{4}"
monthAhead = "[\d]+ bulan ke depan"
weekAhead = "[\d]+ minggu ke depan"
dayAhead = "[\d]+ hari ke depan"
today = "hari ini"
all = "sejauh ini"
when = "kapan"
tanggal = "(((0[1-9]|1\d|2\d|3[0-1])/(0[13578]|1[02])|((0[1-9]|[12]\d|30)/(0[469]|11)))/20\d{2}|" \
          "((0[1-9]|[12]\d)/02/20([02468][048]|[13579][26]))|((0[1-9]|1\d|2[0-8])/02/20([02468]" \
          "[1235679]|[13579][01345789])))"

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="132435", #-----isi dengan password masing-masing
    database="AntiKeosKeosBot"
)
mycursor = mydb.cursor()

def allDeadline():
    mycursor.execute("SELECT * from Task")
    result = mycursor.fetchall()
    return(processOutput(result))

def periodDeadline(tanggal1, tanggal2):
    #mengembalikan string yang berisi daftar task dari tanggal1 hingga tanggal2
    mycursor.execute("SELECT * from Task where tanggal BETWEEN '{0}' AND '{1}'".format(tanggal1,tanggal2))
    result = mycursor.fetchall()
    return(processOutput(result))

def processOutput(result):
    output = "[Daftar Deadline]\n"
    for i in range(len(result)):
        output += str(i + 1) + ". " + "(ID:" + str(result[i][0]) + ") "
        output += result[i][1].strftime("%d/%m/20%y - ")
        output += result[i][2] + " - " + result[i][3] + " - " + result[i][4] + "\n"
    return output

def getMatkul(command):
    return


if __name__ == '__main__':
    print(periodDeadline('2021-04-21','2021-05-20'))
    print(allDeadline())
