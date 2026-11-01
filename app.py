
from flask import Flask, render_template, request, redirect, url_for
from database import get_connection

# Create Flask application first
app = Flask(__name__)


@app.route("/")
def home():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("index.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        usn = request.form["usn"]
        course = request.form["course"]
        marks = request.form["marks"]

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO students (name, usn, course, marks)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (name, usn, course, marks))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("home"))

    return render_template("add_student.html")


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["name"]
        usn = request.form["usn"]
        course = request.form["course"]
        marks = request.form["marks"]

        cursor.execute(
            """
            UPDATE students
            SET name=%s, usn=%s, course=%s, marks=%s
            WHERE id=%s
            """,
            (name, usn, course, marks, student_id)
        )

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for("home"))

    cursor.execute(
        "SELECT * FROM students WHERE id=%s",
        (student_id,)
    )

    student = cursor.fetchone()

    cursor.close()
    connection.close()

    if student is None:
        return "Student not found", 404

    return render_template("edit_student.html", student=student)


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=%s",
        (student_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
