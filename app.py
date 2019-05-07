from flask import Flask, render_template, request, jsonify, send_from_directory, abort # modul2 pada aplikasi Flask
from pymongo import MongoClient             # modul untuk menghubungkan mongoDB dengan python
from werkzeug.utils import secure_filename  # modul untuk menyimpan hasil upload file
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './storage'

server = MongoClient('mongodb://localhost:27017/')  # membuat server mongo
db = server['nrrdb']                                # menentukan database yang digunakan
col = db['pokemon']                                 # menentukan collection yang digunakan

# membuat route home yang akan menampilkan home.html berisi formulir yang dapat diisi
@app.route('/')
def home():
    return render_template('home.html')

# route untuk mengolah data
@app.route('/data', methods=['POST','GET'])
def data():
    # post data
    if request.method == 'POST':
        nama = request.form['nama']
        usia = int(request.form['usia']) # agar input usia menjadi integer
        upload = request.files['foto']
        
        # menyimpan hasil upload ke folder storage
        namaFile = secure_filename(upload.filename)
        upload.save(os.path.join(app.config['UPLOAD_FOLDER'], namaFile))
        foto = 'http://127.0.0.1:5000/storage/' + namaFile
        
        # memasukan data ke collection
        # poke_id untuk membuat id pokemon yang akan ditampilkan di file json
        data = {'poke_id': len(list(col.find()))+1, 'nama':nama, 'usia':usia, 'foto':foto}
        z = col.insert_one(data)
        for i in col.find({'_id': z.inserted_id}):
            nama_db = i['nama']
            usia_db = i['usia']
            gambar = i['foto']
        # hasil ditampilkan dalam profil.html
        return render_template('profil.html', nama=nama_db, usia=usia_db, foto=gambar)
    
    # get data
    else:
        dataJson = []   # membuat list kosong untuk menampung hasil get
        for data in col.find():
            # buat dictionary yang berisi data yang di-GET
            dataDict = {
                'poke_id' : data['poke_id'],
                'nama' : data['nama'],
                'usia' : data['usia'],
                'foto' : data.get('foto','no data') # menggunakan get agar bila field foto tidak ada tetap dapat ditampilkan
            }
            # memasukan dictionary ke dalam list
            dataJson.append(dataDict)
        return jsonify(dataJson)    # menampilkan hasil berupa json

# route untuk folder storage
@app.route('/storage/<path:z>')
def suksesupload(z):
    return send_from_directory('storage', z)

# dynamic route untuk menampilkan satu data
@app.route('/data/<int:poke_id>', methods=['GET','DELETE','PUT'])
def oneData(poke_id):
    # mengambil satu data berdasarkan poke_id
    if request.method == 'GET':
        dataJson = []
        for data in col.find({'poke_id':poke_id}):
            dataDict = {
                'poke_id' : data['poke_id'],
                'nama' : data['nama'],
                'usia' : data['usia'],
                'foto' : data.get('foto','no data')
            }
            dataJson.append(dataDict)
        if len(dataJson) == 1:
            return render_template('profil_satu.html', nama=dataJson[0]['nama'], usia=dataJson[0]['usia'], foto=dataJson[0]['foto'] )
        else:
            abort(404)
    
    # menghapus id tertentu
    elif request.method == 'DELETE':
        col.delete_many({'poke_id':poke_id})
        return 'Data berhasil dihapus'

    # mengedit data dengan poke_id dari body request
    else:
        body = request.json
        poke_id = poke_id
        usia = body['usia']

        col.update_one(
            {'poke_id':poke_id},
            {'$set': {'usia':usia}}
        )
        return 'Method PUT berhasil!'

# route untuk halaman error
@app.errorhandler(404)
def error(error):
    return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=True)