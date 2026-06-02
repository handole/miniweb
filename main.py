from flask import Flask
from flask import request
from flask import redirect, url_for
from flask import render_template
from flask import flash


app = Flask(__name__)
app.secret_key = "inirahasiasaja"

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/profile/<nama>")
def profile(nama):

    return render_template("profile.html", nama=nama)

@app.route("/pets")
def pets():
    energy = 5
    happiness = 5
    
    return f"Energy: {energy}, Happiness: {happiness}"
    
@app.route("/pets/<energy>/<happiness>")
def update_pets(energy: int, happiness: int):
    return f"Updated Energy: {energy}, Updated Happiness: {happiness}"

@app.route("/input-form", methods=["GET", "POST"])
def input_form():
    if request.method == "POST":
        nama = request.form.get("nama")
        umur = request.form.get("umur")
        alamat = request.form.get("alamat")
        return render_template("profile.html", nama=nama, 
                               umur=umur, alamat=alamat)
    return render_template("input.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/embed")
def embed():
    return render_template("embed.html")

@app.route("/video")
def video():
    return render_template("video.html")

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        a = request.form.get("a", default=0, type=int)
        b = request.form.get("b", default=0, type=int)
        if request.form.get("operation") == "add":
            result = a + b
        elif request.form.get("operation") == "subtract":
            result = a - b
        elif request.form.get("operation") == "multiply":
            result = a * b
        elif request.form.get("operation") == "divide":
            result = a / b if b != 0 else "Error: Division by zero"
        else:
            result = "Invalid operation"
        return render_template("calculator.html", result=result)
    return render_template("calculator.html", result=None)

@app.route("/bentuk", methods=["GET", "POST"])
def operasi():
    if request.method == "POST":
        a = request.form.get("a", default=0, type=int)
        b = request.form.get("b", default=0, type=int)
        bentuk = request.form.get("bentuk")
        if bentuk == "persegi":
            luas = a * b
            keliling = 2 * (a + b)
            return render_template("bentuk.html", luas=luas, keliling=keliling)
        elif bentuk == "segitiga":
            luas = 0.5 * a * b
            keliling = a + b + (a**2 + b**2)**0.5
            return render_template("bentuk.html", luas=luas, keliling=keliling)
        elif bentuk == "lingkaran":
            import math
            luas = math.pi * a ** 2
            keliling = 2 * math.pi * a
            return render_template("bentuk.html", luas=luas, keliling=keliling)
        else:
            return render_template("bentuk.html", error="Bentuk tidak valid")
    return render_template("bentuk.html", luas=None, keliling=None)


data_siswa = []

@app.route("/siswa", methods=["GET", "POST"])

def siswa():
    global data_siswa

    if request.method == 'POST':
        nama = request.form["nama"]
        umur = request.form["umur"]
        kelas = request.form["kelas"]
        alamat = request.form["alamat"]
        data_siswa.append({
            "nama": nama,
            "umur": umur,
            "kelas": kelas,
            "alamat": alamat
        })
        flash("Data berhasil ditambahkan!")
        return redirect(url_for("siswa"))
    # Pagination
    page = request.args.get('page', default=1, type=int)
    per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    total_data = len(data_siswa)
    
    search = request.args.get("search", default="", type=str)
    if search:
        data_siswa = [s for s in data_siswa if search.lower() in s["nama"].lower()]
        total_data = len(data_siswa)
    total_pages = (total_data + per_page - 1) // per_page
    data_paginated = data_siswa[start:end]
    return render_template("siswa.html", 
        data_siswa=data_paginated, page=page, total_pages=total_pages, search=search)

@app.route("/siswa/<int:index>")
def detail_siswa(index):
    siswa = data_siswa[index]
    return render_template("detail_siswa.html", siswa=siswa, index=index)


@app.route("/hapus-siswa/<int:index>", methods=["GET", "POST"])
def pop_siswa(index):
    data_siswa.pop(index)
    flash(f"Data index {index} berhasil dihapus!")
    return redirect(url_for("siswa"))

@app.route("/sort-siswa", methods=["GET", "POST"])
def sort_siswa():
    data_siswa.sort(key=lambda x: x["nama"])
    flash("Data berhasil diurutkan!")
    return redirect(url_for("siswa"))  

data_copy = []
@app.route("/copy-siswa", methods=["GET", "POST"])
def copy_siswa():
    global data_copy
    data_copy = data_siswa.copy()
    return render_template("copy.html", data=data_copy)

@app.route("/clear-siswa", methods=["GET", "POST"])
def clear_siswa():
    data_siswa.clear()
    flash("Data berhasil dihapus semua!")
    return redirect(url_for("siswa"))

@app.route("/edit-siswa/<int:index>", methods=["GET", "POST"])
def edit_siswa(index):
    if request.method == 'POST':
        data_siswa[index]["nama"] = request.form["nama"]
        data_siswa[index]["umur"] = request.form["umur"]
        data_siswa[index]["kelas"] = request.form["kelas"]
        data_siswa[index]["alamat"] = request.form["alamat"]
        flash(f"Data index {index} berhasil diupdate!")
        return redirect(url_for("siswa"))
    
    return render_template("edit.html", siswa=data_siswa[index], index=index)

@app.route("/import-excel", methods=["GET", "POST"])
def import_excel():
    file = request.files.get("file")
     # cek apakah file ada
    if not file:
        flash("File belum dipilih!")
        return redirect(url_for("siswa"))
    
    if file.filename.endswith(".xlsx"):
        import pandas as pd
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            data_siswa.append({
                "nama": row["nama"],
                "umur": row["umur"],
                "kelas": row["kelas"],
                "alamat": row["alamat"]
            })
        flash("Data berhasil diimpor dari Excel!")
    return redirect(url_for("siswa"))


data_penduduk = []

@app.route("/penduduk")
def penduduk():
    return render_template("penduduk.html", data_penduduk=data_penduduk)

# segitiga *
@app.route("/simbol", methods=["GET", "POST"])
def simbol_segitiga():
    hasil = []
    if request.method == "POST":
        simbol = request.form["simbol"]
        jumlah = request.form["jumlah"]
        for i in range(1, int(jumlah) + 1):
            hasil.append(simbol * i)
    return render_template("simbol.html", hasil=hasil)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)