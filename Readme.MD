# Latihan menggabungkan Flask & MongoDB

1. Aktivasti server __MongoDB__ di terminal 1:
    
    ```bash
    $ cd C:\Program Files\MongoDB\Server\4.0\bin
    $ mongod

2. Aktivasi database __MongoDB__ di terminal 2:

    ```bash
    $ cd C:\Program Files\MongoDB\Server\4.0\bin
    $ mongo

3. Membuat database sekaligus menggunakannya 

    ```bash
    $ use <nama database>

4. Membuat collection

    ```bash
    $ db.createCollection <nama Collection>
    ```
    pada latihan ini nama _collection_ adalah pokemon.

5. Menampilkan isi _collection_

    ```bash
    $ db.pokemon.find().pretty()
    {
        "_id" : ObjectId("5cd187d951e11bce912885e1"),
        "poke_id" : 1,
        "nama" : "Pikachu",
        "usia" : 23,
        "foto" : "http://127.0.0.1:5000/storage/pikachu.jpg"
    }
    {
            "_id" : ObjectId("5cd1925aa11637e7e1fd2460"),
            "poke_id" : 2,
            "nama" : "Charizard",
            "usia" : 25,
            "foto" : "http://127.0.0.1:5000/storage/charizard.jpg"
    }

6. Jalankan aplikasi app.py di terminal. Pastikan server MongoDB anda masih berjalan.

    ``` bash
    $ python app.py
    ```
    Aplikasi akan berjalan di http://localhost:5000/

7. Berikan request pada server. Bila ingin mencoba metode DELETE dan PUT dapat menggunakan aplikasi __POSTMAN__ app.

    __Menampilkan halaman depan (*home.html*)__
    ```bash
    GET /
    ```

    __Post data ke database:__ 
    ```bash
    POST /data

    ```
    __Get semua data & data tertentu berdasarkan id:__
    ```bash
    GET /data
    GET /data/{:poke_id}
    ```
    __Update data berdasarkan id__:
    ```bash
    PUT /data/{:poke_id}
    body request: {"usia":usia}
    ```
    __Delete a data by id:__
    ```bash
    DELETE /data/{:poke_id}
    ```
8. Semoga bermanfaat!!