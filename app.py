from flask import Flask, app, request, redirect, render_template
import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        database='hodimlar_db',
        user="root",
        password="200909"
    )

def hodimlarni_oqi():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM hodimlar")
            rows = cursor.fetchall()
            return rows
        
def hodimni_oqi(id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM hodimlar WHERE id = %s", (id,))
            rows = cursor.fetchone()
            return rows

def hodimni_ochir(id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM hodimlar WHERE id = %s", (id,))
            conn.commit()

def hodimni_ozgartir(id, ism, familiya, lavozim, yoshi, jinsi):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE hodimlar SET ism=%s, familiya=%s, lavozim=%s, yoshi=%s, jinsi=%s WHERE id=%s",
                (ism, familiya, lavozim, yoshi, jinsi, id)
            )
            conn.commit()


def hodimni_qoshish(ism, familiya, lavozim, yoshi, jinsi):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO hodimlar(ism, familiya, lavozim, yoshi, jinsi) VALUES (%s, %s, %s, %s, %s)", (ism, familiya, lavozim, yoshi, jinsi))
            conn.commit()

app = Flask(__name__)
@app.route('/')
def home_page():
    hodimlar = hodimlarni_oqi()        
    return render_template("index.html", hodimlar=hodimlar)

@app.route('/delete/<int:id>')
def delete_page(id):
    hodimni_ochir(id)
    return redirect('/')

@app.route('/insert', methods=['POST'])
def insert_page():
    ism=request.form['ism']
    fam=request.form['familiya']
    lavozim=request.form['lavozim']
    yosh=request.form['yosh']
    jinsi=request.form['jinsi']
    hodimni_qoshish(ism,fam, lavozim, yosh, jinsi)

    return redirect('/')

@app.route('/update/<int:id>', methods=['GET'])
def update_page(id):
    hodim = hodimni_oqi(id)     
    return render_template("update.html", task=hodim)

@app.route('/edit/<int:id>', methods=['POST'])
def edit_page(id):
    ism=request.form['ism']
    fam=request.form['familiya']
    lavozim=request.form['lavozim']
    yosh=request.form['yosh']
    jinsi=request.form['jinsi']
    hodimni_ozgartir(id, ism, fam, lavozim, yosh, jinsi)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True)
    # hodimni_qoshish("ali", "valiyev", "Dasturchi", 25, True)
    # hodimni_ozgartir(1, "Ali", "Valiyev", "dasturchi", 25, True)
    # hodimni_ochir(1)
