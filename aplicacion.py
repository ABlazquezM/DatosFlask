from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import json

app = Flask(__name__)

bd = "datos.db"


# funcion para crear la tabla
def crearTabla():
    with sqlite3.connect(bd) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS REGISTROS(ID INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE VARCHAR(30),  SLOGAN VARCHAR(200), DESCRIPCION TEXT,IMAGEN TEXT )"
        )
        conexion.commit()


crearTabla()


# Creamos la ruta base, es una funcion decoradora, son las que llaman por una palabra
@app.route("/")
def index():
    with sqlite3.connect(bd) as conexion:
        cursor = conexion.cursor()
        cursor.execute("PRAGMA table_info(REGISTROS)")
        datos = cursor.fetchall()
    return render_template("index.html", data=datos)


@app.route("/insertar", methods=["POST"])
def insertar():
    try:
        if request.method == "POST":
            nombre = request.form["nombre"]
            slogan = request.form["slogan"]
            descripcion = request.form["descripcion"]
            imagen = request.form["imagen"]
            with sqlite3.connect(bd) as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO REGISTROS (NOMBRE,SLOGAN,DESCRIPCION,IMAGEN) VALUES (?,?,?,?)",
                    (
                        nombre,
                        slogan,
                        descripcion,
                        imagen,
                    ),
                )
                conexion.commit()
        return redirect(url_for("index", success="true"))
    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/muestra")
def muestra():
    with sqlite3.connect(bd) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM REGISTROS")
        datos = cursor.fetchall()
    return render_template("muestra.htm", data=datos)


@app.route("/api", methods=["GET"])
def contenido_api():
    connection = sqlite3.connect(bd)
    cursor = connection.cursor()
    cursor.execute("SELECT NOMBRE, SLOGAN, IMAGEN FROM REGISTROS")
    registros = cursor.fetchall()
    connection.close()
    datos = jsonify(registros)

    return render_template("api.html", data=datos)


if (__name__) == "__main__":
    app.run(debug=True)
