""" 
# ------ VERSION 1 - WITHOUT THE DATABASE

from flask_restful import Resource
from flask import request
import json

# In a real application, this would be a database/service layer.
# For this example, we use an in-memory list.
# List structure: [{"id": 1, "title": "Java book"}, ...]
books = [
    {"id": 1, "title": "Java book"},
    {"id": 2, "title": "Python book"}
]

class BooksGETResource(Resource):
    def get(self):
        return books

class BookGETResource(Resource):
    def get(self, id):
        for book in books:
            if book["id"] == id:
                return book
        return None

class BookPOSTResource(Resource):
    def post(self):
        book = json.loads(request.data)
        
        # Determine the new ID by finding the max existing ID and adding 1
        new_id = max(b["id"] for b in books) + 1
        
        book["id"] = new_id
        books.append(book)
        
        return book

class BookPUTResource(Resource):
    def put(self, id):
        update_data = json.loads(request.data)
        for book in books:
            if book["id"] == id:
                book.update(update_data)
                return book
        # If the book ID is not found (implicit 404 handled by Flask-RESTful if None/empty response is not returned,
        # but the original code structure relies on returning the updated book)
        
class BookDELETEResource(Resource):
    def delete(self, id):
        global books
        # Use a list comprehension to filter out the book with the given ID
        books = [book for book in books if book["id"] != id]
        return "", 204
        
"""

""" 
--- VERSION 2 - WITH SQLITE
"""

from flask_restful import Resource
from flask import request
import sqlite3

def get_db_connection():
    try:
        conn = sqlite3.connect("emp.db") 
        conn.row_factory = sqlite3.Row 
        return conn
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        raise

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        );
    """)
    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO books (title) VALUES ('Java book')")
        cursor.execute("INSERT INTO books (title) VALUES ('Python book')")
    
    conn.commit()
    conn.close()

init_db()

class BooksGETResource(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM books")
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result

class BookGETResource(Resource):
    def get(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM books WHERE id = ?" 
        cursor.execute(query, (id,))
        
        result = cursor.fetchone()
        conn.close()

        if result:
            return dict(result) 
        
        return {"message": f"Book with id {id} not found"}, 404

class BookPOSTResource(Resource):
    def post(self):
        try:
            book_data = request.get_json(force=True)
            title = book_data.get("title")
        except:
            return {"message": "Invalid JSON data provided"}, 400

        if not title:
            return {"message": "Missing 'title' field in request body"}, 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO books (title) VALUES (?)"
        cursor.execute(query, (title,))
        
        new_id = cursor.lastrowid
        conn.commit() 
        conn.close()

        return {"id": new_id, "title": title}, 201

class BookPUTResource(Resource):
    def put(self, id):
        try:
            book_data = request.get_json(force=True)
            title = book_data.get("title")
        except:
            return {"message": "Invalid JSON data provided"}, 400
        
        if not title:
            return {"message": "Missing 'title' field for update"}, 400

        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "UPDATE books SET title = ? WHERE id = ?"
        cursor.execute(query, (title, id))
        
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return {"message": f"Book with id {id} not found"}, 404
        
        conn.close()
        return {"id": id, "title": title}

class BookDELETEResource(Resource):
    def delete(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "DELETE FROM books WHERE id = ?"
        cursor.execute(query, (id,))
        
        conn.commit()

        if cursor.rowcount == 0:
            conn.close()
            return {"message": f"Book with id {id} not found"}, 404
            
        conn.close()
        return "", 204