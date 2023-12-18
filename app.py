from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)

database = "database.db"
import sqlite3

app.secret_key = "jjjjjjjjjjjjjjjjj"
database = "database.db"


def create_table():
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute(
        """
        create table if not exists admin(
         id integer not null primary key,
         email text not null,
         password text not null
        )
        """
    )
    cursor.execute(
        """
        create table if not exists doctor(
         id integer not null primary key,
         email text not null,
         password text not null,
         specialised text not null,
         name text not null,
         fee numerical not null
         )
        """
    )

    cursor.execute(
        """
        create table if not exists patients(
         id integer not null primary key,
         name text not null,
         doctor_id integer not null,
         medicine integer not null,
         FOREIGN KEY (doctor_id) REFERENCES doctor(id)
        )
        """
    )

    connection.commit()
    connection.close()


create_table()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_registration", methods=["GET", "POST"])
def admin_registration():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute(
            "insert into admin (email,password) values(?,?)", (email, password)
        )
        connection.commit()
        connection.close()
        return redirect(url_for("admin_login"))

    return render_template("admin_registration.html")


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["Password"]

        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute(
            "select * from admin where email=? AND password=?", (email, password)
        )
        user = cursor.fetchone()
        connection.close()

        if user:
            session["admin_id"] = user[0]
            return redirect(url_for("admin_dashboard"))
    return render_template("admin_login.html")


@app.route("/admin_dashboard")
def admin_dashboard():
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute("select * from doctor")
    doctor = cursor.fetchall()

    cursor.execute("select * from patients")
    patients = cursor.fetchall()

    connection.close()
    total_amount = 0
    for i in doctor:
        for j in patients:
            if i[0] == j[2]:
                total = 0
                total = i[5] + j[3]
                total_amount = total_amount + total

    return render_template(
        "admin_dashboard.html",
        doctor=doctor,
        patients=patients,
        total_amount=total_amount,
    )


@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    if "admin_id" not in session:
        redirect(url_for("admin_login"))

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        specialised = request.form["specialised"]
        fee = request.form["fee"]

        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute(
            "insert into doctor (name,email,password,specialised,fee) values(?,?,?,?,?)",
            (name, email, password, specialised, fee),
        )
        connection.commit()
        connection.close()

        return redirect(url_for("add_doctor"))
    return render_template("add_doctor.html")


@app.route("/doctor_login", methods=["GET", "POST"])
def doctor_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["Password"]

        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute(
            "select * from doctor where email=? AND password=?", (email, password)
        )
        user = cursor.fetchone()
        connection.close()

        if user:
            session["doctor_id"] = user[0]
            return redirect(url_for("doctor_dashboard"))
    return render_template("doctor_login.html")


@app.route("/doctor_dashboard")
def doctor_dashboard():
    return render_template("doctor_dashboard.html")


@app.route("/add_patients", methods=["GET", "POST"])
def add_patients():
    if "doctor_id" not in session:
        redirect(url_for("doctor_login"))

    doctor_id = session.get("doctor_id")
    if request.method == "POST":
        name = request.form["name"]
        medicine = request.form["medicine"]

        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute(
            "insert into patients (name,medicine,doctor_id) values(?,?,?)",
            (name, medicine, doctor_id),
        )
        connection.commit()
        connection.close()

        return redirect(url_for("add_patients"))
    return render_template("add_patients.html")


if __name__ == "__main__":
    app.run(debug=True)
