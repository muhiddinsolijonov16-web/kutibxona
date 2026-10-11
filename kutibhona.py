import psycopg2

db = psycopg2.connect(
    dbname = "kutibxona",
    user = "postgres",
    password = "Nano2026",
    host = "localhost",
    port = 5432
)
cursor = db.cursor()

cursor.execute("""
            DROP TABLE IF EXISTS books;

            CREATE TABLE IF NOT EXISTS books(
            id SERIAL PRIMARY KEY,
            nomi VARCHAR(70),
            muallif VARCHAR(70),
            yil INT,
            price DECIMAL(10,1));
            
            INSERT INTO books (nomi, muallif, yil, price)
            VALUES
            (%s, %s, %s, %s),
            (%s, %s, %s, %s),
            (%s, %s, %s, %s),
            (%s, %s, %s, %s),
            (%s, %s, %s, %s)
            """, (
            "Atomic Habits", "James Clear", 2018, 45000,
            "O'tkan kunlar", "Abdulla Qodiriy", 1925, 35000,
            "Ikki eshik orasi", "O'tkir Hoshimov", 1986, 40000,
            "Sariq devni minib", "Xudoyberdi To'xtaboyev", 1968, 30000,
            "Alkimyogar", "Paulo Coelho", 1988, 50000
))

db.commit()
while 1:
    try:
        tanlov = int(input("""
    1.Kitob qoshish
    2.Kitob qidirish
    3.Kitoblarni hammasini korish 
    4.kitob ochrishi 
    5.kitob malumotlarini yangilash
    6.kitoblarning umumiy soni
    7.Chiqish
        """))
        match tanlov:
            case 1:
                nomi = input("kitob nomini kiriting: ")
                muallifi = input("muallifini kiriting: ")
                narx = float(input("kitob narxini kiriting: "))
                yil = int(input("yilini kiriting: "))

                cursor.execute("""
            
                INSERT INTO books(nomi,muallifi,yil,price) VALEUS
                (%s,%s,%s,%s);
                """,(nomi ,muallifi,yil,narx))
                db.commit()
                print("kitob muvoffaqiyatli qoshildi")
            case 2:
                qidiruv = int(input("kitob id sini kiriting: "))
                cursor.execute("""
                SELECT * FROM books WHERE id = %s; """,(qidiruv,))
                data = cursor.fetchone()
                if data != None:
                    print(f"kitob nomi {data[1]}\n kitob kuallifi: {data[2]}\nyili: {data[3]}\nkitob narxi:{data[4]}")
                else:
                    print("bunday id da kitob mavjud emas")
            case 3:       
                cursor.execute("SELECT * FROM books")
                data_all = cursor.fetchall()
                for data in data_all:
                        print(f"kitob id:{data[0]}\nkitob nomi {data[1]}\n kitob kuallifi: {data[2]}\nyili: {data[3]}\nkitob narxi:{data[4]}")
                        print("-"*50)
            case 4:
                dead = int(input("qaysi id dagi kitobni ochirmoqchisz: "))
                cursor.execute("SELECT * FROM books WHERE id = %s",(dead,))
                data = cursor.fetchone()
                if data == None:
                    print("bunday kitob mavjud emas")
                else:
                    cursor.execute("DELETE FROM books WHERE id =%s",(dead,))
                    print("kitob muvaffaqiyatli ochirildi")
                db.commit()
            case 5:
                id_book = int(input("qaysi id dagi kitobni ozgartirmoqchisz: "))

                nomi = input("yangi kitob nomini kiriting: ")
                muallifi = input("yangi kitob muallifini kiriting: ")
                narx = float(input("yangi kitob narxini kiriting: "))
                yil = int(input("yangi kitob yilini kiriting: "))

                cursor.execute("SELECT * FROM books WHERE id = %s",(id_book,))
                data = cursor.fetchone()
                if data != None:
                    cursor.execute("""
                    UPDATE books 
                    SET nomi = %s,
                    muallif = %s,
                    yil = %s,
                    price = %s
                    WHERE id = %s
                    """,(nomi,muallifi,narx,yil,id_book))
                    print("kitob muvaffaqiyatli ozgartirildi")
                    db.commit()
                else:
                    print("bunday id da kitob mavjud emas")
            case 6:
                cursor.execute("SELECT COUNT(nomi) FROM books;")
                count_book = cursor.fetchone()
                print("kitoblar soni: ",count_book[0])
            case 7:
                print("dasturdan muvaffaqiyatili chiqildi!!")
                break
            case _:
                print("xato tanlov")
    except Exception as e:
        print(e)
cursor.close()
db.close()