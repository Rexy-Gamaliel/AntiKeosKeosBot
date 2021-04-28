# AntiKeosKeosBot
>Tugas Besar 3 IF2211 Strategi Algoritma
>
>Membuat aplikasi *web-based* ChatBot untuk penjadwalan tugas, ujian, dan lain-lain.

## Kebutuhan Instalasi
* Python 3.8+
* MariaDB 10.5+
* Install library flask dengan command `pip install flask` 
* Install library mysql-connector dengan command `pip install mysql-connector`

## Persiapan
* Buka command prompt, arahkan ke direktori yang diinginkan
* Clone repository ini dengan command `git clone https://github.com/Rexy-Gamaliel/AntiKeosKeosBot`
* Arahkan direktori ke folder test yang terdapat di dalam folder repository
* Store database ke MariaDB lokal dengan command `mysql -u {username} -p AntiKeosKeosBot < AntiKeosKeosBot.sql`

## Cara Menjalankan
* Pertama-tama, buka file inoutput.py pada IDE, kemudian isi password pada line 7 dengan password MariaDB lokal
* Pada folder tempat penyimpanan repository, buka command prompt, kemudian jalankan program dengan menggunakan command `python src/app.py`
* Tunggu hingga program men-_generate_ link alamat lokal
* Buka link tersebut di browser
* Program AntiKeosKeosBot siap untuk dijalankan

## Cara Menggunakan
* Klik tab **AntiKeosKeosBot** untuk masuk ke halaman utama dan berkomunikasi dengan Bot
   
  Masukkan input ke dalam _chatbox_ yang tersedia kemudian klik tombol send
* Klik tab **How to use** untuk masuk ke halaman yang menampilkan cara penggunaan program
* Klik tab **Credit** untuk melihat _contact person_

## Fitur yang Disediakan
* Menambahkan task baru
* Melihat daftar task yang harus dikerjakan
* Menampilkan deadline dari task tertentu
* Memperbaharui deadline task tertentu
* Menandai bahwa suatu task sudah selesai dikerjakan
* Menampilkan opsi help yang difasilitasi oleh bot

## Kontak
* Rexy Gamaliel Rumahorbo - 13519010@std.stei.itb.ac.id
* Ruhiyah Faradishi Widiaputri - 13519034@std.stei.itb.ac.id
* Sharon Bernadetha Marbun - 13519092@std.stei.itb.ac.id


