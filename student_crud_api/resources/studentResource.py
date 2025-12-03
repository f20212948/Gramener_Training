from flask_restful import Resource
from flask import request
import sqlite3

"""
BASIC SECURITY (Username + Password)
"""
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"

def check_credentials():
    username = request.headers.get("X-USERNAME")
    password = request.headers.get("X-PASSWORD")
    if username != VALID_USERNAME or password != VALID_PASSWORD:
        return False
    return True

def get_db_connection():
    try:
        conn = sqlite3.connect("students.db")
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        raise

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        initial_students = [
            ('Ninad', 21, 'History'),
            ('Dheekshith', 20, 'Mathematics'),
            ('Mouneesh', 22, 'Physics'),
            ('Mahith' , 24,'Chemistry')
        ]
        cursor.executemany("INSERT INTO students (name, age, course) VALUES (?, ?, ?)", initial_students)

    
    conn.commit()
    conn.close()

init_db()

class StudentsGETResource(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result

class StudentGETResource(Resource):
    def get(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM students WHERE id = ?"
        cursor.execute(query, (id,))
        
        result = cursor.fetchone()
        conn.close()

        if result:
            return dict(result) 
        
        return {"message": f"Student with id {id} not found"}, 404

class StudentPOSTResource(Resource):
    def post(self):
        try:
            student_data = request.get_json(force=True)
            name = student_data.get("name")
            age = student_data.get("age")
            course = student_data.get("course")
        except:
            return {"message": "Invalid JSON data provided"}, 400

        if not all([name, age, course]):
            return {"message": "Missing required fields: 'name', 'age', and 'course'"}, 400
        
        try:
            age = int(age)
        except ValueError:
            return {"message": "Field 'age' must be an integer"}, 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO students (name, age, course) VALUES (?, ?, ?)"
        cursor.execute(query, (name, age, course))
        
        new_id = cursor.lastrowid
        conn.commit()
        
        cursor.execute("SELECT * FROM students WHERE id = ?", (new_id,))
        new_student = cursor.fetchone()
        conn.close()

        return dict(new_student), 201

class StudentPUTResource(Resource):
    def put(self, id):
        try:
            student_data = request.get_json(force=True)
            name = student_data.get("name")
            age = student_data.get("age")
            course = student_data.get("course")
        except:
            return {"message": "Invalid JSON data provided"}, 400
        
        if not all([name, age, course]):
            return {"message": "Missing required fields for update: 'name', 'age', and 'course'"}, 400

        try:
            age = int(age)
        except ValueError:
            return {"message": "Field 'age' must be an integer"}, 400

        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "UPDATE students SET name = ?, age = ?, course = ? WHERE id = ?"
        cursor.execute(query, (name, age, course, id))
        
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return {"message": f"Student with id {id} not found"}, 404
        
        cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
        updated_student = cursor.fetchone()
        conn.close()
            
        return dict(updated_student)

class StudentDELETEResource(Resource):
    def delete(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "DELETE FROM students WHERE id = ?"
        cursor.execute(query, (id,))
        
        conn.commit()

        if cursor.rowcount == 0:
            conn.close()
            return {"message": f"Student with id {id} not found"}, 404
            
        conn.close()
        return {"message":f"Student with id {id} deleted"}, 204