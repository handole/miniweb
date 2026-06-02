from flask import Flask
from flask import request
from flask import render_template
from flask import session

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route('/')
def home():
    return render_template("home.html", active_page='dashboard')

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
                               umur=umur, alamat=alamat, active_page='profile')
    return render_template("input.html", active_page='input-form')

@app.route("/about")
def about():
    return render_template("about.html", active_page='about')

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
        return render_template("calculator.html", result=result, active_page='calculator')
    return render_template("calculator.html", result=None, active_page='calculator')

@app.route("/bentuk", methods=["GET", "POST"])
def operasi():
    if request.method == "POST":
        a = request.form.get("a", default=0, type=int)
        b = request.form.get("b", default=0, type=int)
        bentuk = request.form.get("bentuk")
        if bentuk == "persegi":
            luas = a * b
            keliling = 2 * (a + b)
            return render_template("bentuk.html", luas=luas, keliling=keliling, active_page='bentuk')
        elif bentuk == "segitiga":
            luas = 0.5 * a * b
            keliling = a + b + (a**2 + b**2)**0.5
            return render_template("bentuk.html", luas=luas, keliling=keliling, active_page='bentuk')
        elif bentuk == "lingkaran":
            import math
            luas = math.pi * a ** 2
            keliling = 2 * math.pi * a
            return render_template("bentuk.html", luas=luas, keliling=keliling, active_page='bentuk')
        else:
            return render_template("bentuk.html", error="Bentuk tidak valid", active_page='bentuk')
    return render_template("bentuk.html", luas=None, keliling=None, active_page='bentuk')

@app.route("/konversi-suhu", methods=["GET", "POST"])
def konversi_suhu():
    if request.method == "POST":
        suhu = request.form.get("suhu", default=0, type=float)
        konversi = request.form.get("konversi")
        if konversi == "celcius-fahrenheit":
            hasil = (suhu * 9/5) + 32 # type: ignore
            return render_template("konversi_suhu.html", nilai=hasil, active_page='konversi-suhu')
        elif konversi == "fahrenheit-celcius":
            hasil = (suhu - 32) * 5/9 # type: ignore
            return render_template("konversi_suhu.html", nilai=hasil, active_page='konversi-suhu')
        elif konversi == "celcius-kelvin":
            hasil = suhu + 273.15 # type: ignore
            return render_template("konversi_suhu.html", nilai=hasil, active_page='konversi-suhu')
        elif konversi == "kelvin-celcius":
            hasil = suhu - 273.15 # type: ignore
            return render_template("konversi_suhu.html", nilai=hasil, active_page='konversi-suhu')
        elif konversi == "fahrenheit-kelvin":
            hasil = (suhu - 32) * 5/9 + 273.15 # type: ignore
            return render_template("konversi_suhu.html", nilai=hasil, active_page='konversi-suhu')
        elif konversi == "kelvin-fahrenheit":
            hasil = (suhu - 273.15) * 9/5 + 32 # type: ignore
            return render_template("konversi_suhu.html", nilai=hasil, active_page='konversi-suhu')
        else:
            return render_template("konversi_suhu.html", error="Konversi tidak valid", active_page='konversi-suhu')
    return render_template("konversi_suhu.html", hasil=None, active_page='konversi-suhu')

@app.route("/tebak", methods=["GET", "POST"])
def tebak():
    import random
    if "angka" not in session:
        session["angka"] = random.randint(1, 20)

    pesan = ""

    if request.method == "POST":
        tebakan = request.form.get("tebakan", type=int)
        angka = session["angka"]
        if tebakan < angka:
            return render_template("tebak.html", pesan="Tebakan terlalu rendah!", active_page='tebak')
        elif tebakan > angka:
            return render_template("tebak.html", pesan="Tebakan terlalu tinggi!", active_page='tebak')
        else:
            session.pop("angka", None)  # Reset angka setelah berhasil ditebak
            return render_template("tebak.html", pesan="Selamat! Tebakan benar!", active_page='tebak')
        
    return render_template("tebak.html", pesan=pesan, active_page='tebak')

@app.route("/siswa", methods=["GET", "POST"])
def siswa():
    daftar_siswa = []
    if request.method == "POST":
        nama = request.form.get("nama")
        daftar_siswa.append(nama)
    
    return render_template("siswa.html", daftar_siswa=daftar_siswa, active_page='siswa')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)