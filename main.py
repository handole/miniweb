from flask import Flask
from flask import request
from flask import render_template


app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)