from flask import Flask, render_template, url_for, request, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)

app.secret_key = 'adcæøå'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'

mysql = MySQL(app)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/kontakt")
def kontakt():
    return render_template('kontakt.html')

@app.route("/innlogging", methods = ['GET', 'POST'])
def innlogging():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            message = 'Innlogging vellykket!'
            return render_template('konto.html', message = message)
        else:
            message = 'Vennligst skriv inn riktig E-postadresse og passord'
            return render_template('innlogging.html')

@app.route("/loggut")
def loggut():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('innlogging'))

@app.route("/registrere",methods = ['GET', 'POST'])
def registrere():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email))
        account == cursor.fetchone()
        if account:
            message = 'Brukeren er allerede opprettet'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'E-post er ikke gyldig'
        elif not userName or not password or not email:
            message = 'Vennligst fyll inn all informasjon'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password))
            mysql.connection.commit()
            message = 'Bruker opprettet'
    elif request.method == 'POST':
        message = 'Vennligst fyll inn all informasjon'
    return render_template("/registrere", message = message)

@app.route("/konto")
def konto():
    return render_template('konto.html')

@app.route("/produkter/<type>")
def produkter(type):
    return render_template('produkter.html', type=type)

@app.route("/kategori/<navn>")
def kategori(navn):
    return render_template('kategori.html', kategori=navn)

@app.route("/favoritter")
def favoritter():
    return render_template('favoritter.html')

@app.route("/handlekurv")
def handlekurv():
    return render_template('handlekurv.html')

@app.route("/footer")
def footer():
    return render_template('footer.html')

if __name__ == "__main__":
    app.run(debug=True)

