from flask import Flask, render_template, request, jsonify, send_from_directory # modul2 pada aplikasi Flask
from pymongo import MongoClient     # modul untuk menghubungkan mongoDB dengan python
from werkzeug.utils import secure_filename # modul untuk menyimpan hasil upload file
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
        usia = request.form['usia']
        upload = request.files['foto']
        
        # menyimpan hasil upload ke folder storage
        namaFile = secure_filename(upload.filename)
        upload.save(os.path.join(app.config['UPLOAD_FOLDER'], namaFile))
        foto = 'http://127.0.0.1:5000/storage/' + namaFile
        
        # memasukan data ke collection
        data = {'nama':nama, 'usia':usia, 'foto':foto}
        z = col.insert_one(data)
        for i in col.find({'_id': z.inserted_id}):
            nama_db = i['nama']
            usia_db = i['usia']
            gambar = i['foto']
        # hasil ditampilkan dalam profil.html
        return render_template('profil.html', nama=nama_db, usia=usia_db, foto=gambar)
    
    # get data
    elif request.method == 'GET':
        dataJson = []   # membuat list kosong untuk menampung hasil get
        for data in col.find():
            # buat dictionary yang berisi data yang di-GET
            dataDict = {
                'id' : str(data['_id']),
                'nama' : data['nama'],
                'usia' : data['usia'],
                'foto' : data.get('foto','no data')
            }
            # memasukan dictionary ke dalam list
            dataJson.append(dataDict)
        return jsonify(dataJson)    # menampilkan hasil berupa json

# route untuk folder storage
@app.route('/storage/<path:z>')
def suksesupload(z):
    return send_from_directory('storage', z)

if __name__ == "__main__":
    app.run(debug=True)