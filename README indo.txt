
# Indonesian Doc.
Doc. 18:35 31/03/2021

    Program ini akan menyimulasikan kejadian epidemik dengan SIRD model, sebuah model yang sedikit dimodifikasi dari 
model standar SIR. Program ini juga menambahkan kegiatan pengendalian epidemik sebagai upaya untuk menekan laju infeksi,
diantaranya: penggunaan masker, social distancing, quarantine, vaksinasi dan lockdown.    
    Anda bisa mengatur simulasi berjalan melalui global parameter. Berikut ini adalah elemen-elemen simulasi dasar yang
bisa anda ubah untuk mengatur jalannya simulasi:
    
    # Elements
    A_DAY = 1
        -> Untuk mengatur seberapa lama hari dalam simulasi. Secara default 1 hari adalah 1 sekon. Nilai harus integer.
    DAY = FPS * A_DAY
        -> Karena pygame berjalan berdasarkan FPS maka hari berjalan seiringan FPS, 1 sekon adalah sama dengan nilai
            FPS.
    SHOW_AS_PLOT = False
        -> Setelah simulasi selesai data simulasi yang telah direkam akan ditampilkan. Jika anda mau menampilkan data 
            kedalam bentuk grafik maka set value ini menjadi True dan data akan ditampilkan melalui format matplotlib.
    SHOW_AS_DATA = False
        -> Data juga bisa ditampilkan secara mentah. Set value ini menjadi True maka data akan ditampilkan pada layar 
            dalam bentuk tabel. Anda juga dapat mengatur dimana data mentah ini ditampilkan menggunakan parameter 
            selanjutnya.
    SMOOTH_PLOT = True
        -> Untuk bentuk grafik yang lebih halus set value ini menjadi True maka data yang ditampilkan oleh matplotlib
            akan terlihat lebih halus. Perlu diketahui x axis pada grafik ini tidak berdasarkan per hari sebagai mana 
            telah yang ditentukan sehingga untuk x axis yang lebih akurat berdasarkan waktu perhari set value ini
            menjadi False maka data akan ditunjukan perhari(1 sekon).
    DATA_TO_EXCEL = False
        -> Set value ini menjadi True jika anda ingin merekam data simulasi kedalam xlsx file. Set value ini menjadi 
            False jika anda ingin menampilkan data pada layar dalam bentuk tabel.
        -> Jika anda ingin menampilkan data dalam bentuk grafik dan juga ingin melihatnya dalam bentuk tabel maka set
            value SHOW_AS_PLOT dan SHOW_AS_DATA menjadi True.

    # Epidemic's Elements
    POPULATION = 500
        -> Jumlah orang dalam simulasi, tidak bertambah dan tetap. Nilai harus integer.
    SIZE = 5
        -> Ukuran orang dalam simulasi, dalam pixel. Nilai harus integer.
    SPEED_x, SPEED_y = -100, 100
        -> Dalam satuan pixel. Untuk mengubah seberapa cepat pergerakan dalam simulasi. Sebagai perbandingan orang 
            dengan ukuran 5 pixel setidaknya begerak sampai kecepatan maksimal 10 pixel. Digunakan pula untuk
            menggerakan gerbang pemisah area.  Nilai harus integer.
    TRANSMISSION_CHANCE = 100
        -> Seberapa efektif penyakit dapat menular dari terinfeksi ke yang rentan. Nilai harus integer antara 0 sampai 
            100 (dalam persen).
    MORTALITY_RATE = 50
        -> Seberapa efektif penyakit dapat menyebabkan kematian bagi yang terinfeksi. Nilai harus integer antara 0 
            sampai 100 (dalam persen).
    RECOVERY_TIME = DAY * 21
        -> Seberapa lama penyakit untuk dapat disembuhkan/menghilang. Nilai harus integer.
    
Skenario di bawah ini adalah beberapa contoh yang bisa di jalankan dalam program ini
Untuk menjalankan skenario ini anda perlu mengatur beberapa paramater terlebih dahulu untuk memasukan scenario yang 
akan terjadi pada epidemik ini lalu eksekusi program file melalui terminal. Berikut ini adalah kriteria dalam parameter
untuk berbagai scenario, perlu diingat nilai yang anda bisa masukan harus dalam bentuk integer:
   0. Simulasi SIRD Dasar
    Anda harus memasukkan nilai pada variabel sebagai simulasi epidemik SIRD standar
    Atur ini sebagai variabel tetap jika ada ini menguji tindakan pencegahan
        A_DAY = 1
        POPULATION = 300
        SIZE = 10
        SPEED_x, SPEED_y = -20, 20
        TRANSMISSION_CHANCE = 75
        MORTALITY_RATE = 25 
        RECOVERY_TIME = DAY * 15
    
    1. Tanpa Pencegahan
    Atur semuanya menjadi 0 dan simulasi akan berjalan tanpa tindakan pencegahan
        DAY_START_MASK = 0 
        MASK_APPLICATION = 0 
        DAY_END_MASK = 0  
        DAY_START_DISTANCING = 0  
        SOCIAL_DISTANCING_RATE = 0  
        SOCIAL_DISTANCING_END = 0  
        DAY_START_QUARANTINE = 0  
        DAY_SCHEDULED_QUARANTINE = 0  
        QUARANTINE_RATE = 0  
        QUARANTINE_CHANCE = 0  
        DAY_START_VACCINE = 0  
        DAY_SCHEDULED_VACCINE = 0  
        VACCINATION_RATE = 0  
        VACCINATION_CHANCE = 0 
        DAY_START_LOCKDOWN = 0  
        LOCKDOWN = 0  
        LOCKDOWN_END = 0  

    2.  Efek Menggunakan Masker 25% E fektif untuk Mencegah Terinfeksi 
    Atur nilai ini pada tindakan pencegahan masker dan atur yang lain menjadi 0
        DAY_START_MASK = 15
        MASK_APPLICATION = TRANSMISSION_CHANCE - (25/100 * TRANSMISSION_CHANCE) 
        DAY_END_MASK = 100
        
    3. Efek Menggunakan Masker 50% E fektif untuk Mencegah Terinfeksi
    Atur nilai ini pada tindakan pencegahan masker dan atur yang lain menjadi 0
        DAY_START_MASK = 15
        MASK_APPLICATION = TRANSMISSION_CHANCE - (50/100 * TRANSMISSION_CHANCE) 
        DAY_END_MASK = 100
        
    4. Efek 25% Populasi Melakukan Social Distancing
    Atur nilai ini pada tindakan pencegahan social distancing dan atur yang lain menjadi 0
        DAY_START_DISTANCING = 20
        SOCIAL_DISTANCING_RATE = 25  
        SOCIAL_DISTANCING_END = DAY * 100
        
    5.  Efek 50% Populasi Melakukan Social Distancing
    Atur nilai ini pada tindakan pencegahan social distancing dan atur yang lain menjadi 0
        DAY_START_DISTANCING = 20
        SOCIAL_DISTANCING_RATE = 50  
        SOCIAL_DISTANCING_END = DAY * 100
        
    6.  Efek 25% Populasi Terinfeksi Dikarantina dengan 75% symptomatik
    Atur nilai ini pada tindakan pencegahan karantina dan atur yang lain menjadi 0
        DAY_START_QUARANTINE = 20
        DAY_SCHEDULED_QUARANTINE = 3  
        QUARANTINE_RATE = 25
        QUARANTINE_CHANCE = 75
        
    7. Efek 50% Populasi Terinfeksi Dikarantina dengan 75% symptomatik
    Atur nilai ini pada tindakan pencegahan karantina dan atur yang lain menjadi 0
        DAY_START_QUARANTINE = 20
        DAY_SCHEDULED_QUARANTINE = 3  
        QUARANTINE_RATE = 50
        QUARANTINE_CHANCE = 75
        
    8. Efek 25% Populasi Divaksinasi dengan 95% Sukses Tervaksinasi
    Atur nilai ini pada tindakan pencegahan vaksinasi dan atur yang lain menjadi 0
        DAY_START_VACCINE = 30
        DAY_SCHEDULED_VACCINE = 2  
        VACCINATION_RATE = 25
        VACCINATION_CHANCE = 95
        
    9. Efek 50% Populasi Divaksinasi dengan 95% Sukses Tervaksinasi
    Atur nilai ini pada tindakan pencegahan vaksinasi dan atur yang lain menjadi 0
        DAY_START_VACCINE = 30
        DAY_SCHEDULED_VACCINE = 2  
        VACCINATION_RATE = 50
        VACCINATION_CHANCE = 95
        
    10. 90% lockdown
    Atur nilai ini pada tindakan pencegahan lockdown dan atur yang lain menjadi 0
        DAY_START_LOCKDOWN = 15 
        LOCKDOWN = 90
        LOCKDOWN_END = 50
        
    11. 100% lockdown
    Atur nilai ini pada tindakan pencegahan lockdown dan atur yang lain menjadi 0
        DAY_START_LOCKDOWN = 15 
        LOCKDOWN = 100
        LOCKDOWN_END = 50
        
    12. Kombinasi dari nomor 2, 4, 6, 8, dan 10
        DAY_START_MASK = 15
        MASK_APPLICATION = TRANSMISSION_CHANCE - (25/100 * TRANSMISSION_CHANCE) 
        DAY_END_MASK = 100
        DAY_START_DISTANCING = 20
        SOCIAL_DISTANCING_RATE = 25  
        SOCIAL_DISTANCING_END = DAY * 100
        DAY_START_QUARANTINE = 20
        DAY_SCHEDULED_QUARANTINE = 3  
        QUARANTINE_RATE = 25
        QUARANTINE_CHANCE = 75
        DAY_START_VACCINE = 30
        DAY_SCHEDULED_VACCINE = 2  
        VACCINATION_RATE = 25
        VACCINATION_CHANCE = 95
        DAY_START_LOCKDOWN = 15 
        LOCKDOWN = 90
        LOCKDOWN_END = 50
        
    13. Kombinasi dari nomor 3, 5, 7, 9, dan 11
        DAY_START_MASK = 15
        MASK_APPLICATION = TRANSMISSION_CHANCE - (50/100 * TRANSMISSION_CHANCE) 
        DAY_END_MASK = 100
        DAY_START_DISTANCING = 20
        SOCIAL_DISTANCING_RATE = 50  
        SOCIAL_DISTANCING_END = DAY * 100
        DAY_START_QUARANTINE = 20
        DAY_SCHEDULED_QUARANTINE = 3  
        QUARANTINE_RATE = 50
        QUARANTINE_CHANCE = 75
        DAY_START_VACCINE = 30
        DAY_SCHEDULED_VACCINE = 2  
        VACCINATION_RATE = 50
        VACCINATION_CHANCE = 95
        DAY_START_LOCKDOWN = 15 
        LOCKDOWN = 100
        LOCKDOWN_END = 50
