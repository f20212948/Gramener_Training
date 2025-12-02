
# ------ VERSION 1 - WITHOUT THE DATABASE

# from flask_restful import Resource
# from flask import request
# import json

# # In a real application, this would be a database/service layer.
# # For this example, we use an in-memory list.
# # List structure: [{"id": 1, "title": "Java book"}, ...]
# books = [
#     {"id": 1, "title": "Java book"},
#     {"id": 2, "title": "Python book"}
# ]

# class BooksGETResource(Resource):
#     def get(self):
#         return books

# class BookGETResource(Resource):
#     def get(self, id):
#         for book in books:
#             if book["id"] == id:
#                 return book
#         return None

# class BookPOSTResource(Resource):
#     def post(self):
#         book = json.loads(request.data)
        
#         # Determine the new ID by finding the max existing ID and adding 1
#         new_id = max(b["id"] for b in books) + 1
        
#         book["id"] = new_id
#         books.append(book)
        
#         return book

# class BookPUTResource(Resource):
#     def put(self, id):
#         update_data = json.loads(request.data)
#         for book in books:
#             if book["id"] == id:
#                 book.update(update_data)
#                 return book
#         # If the book ID is not found (implicit 404 handled by Flask-RESTful if None/empty response is not returned,
#         # but the original code structure relies on returning the updated book)
        
# class BookDELETEResource(Resource):
#     def delete(self, id):
#         global books
#         # Use a list comprehension to filter out the book with the given ID
#         books = [book for book in books if book["id"] != id]
#         return "", 204
        


""" 
--- VERSION 2 - WITH SQLITE
"""

# from flask_restful import Resource
# from flask import request
# import sqlite3

# def get_db_connection():
#     try:
#         conn = sqlite3.connect("emp.db") 
#         conn.row_factory = sqlite3.Row 
#         return conn
#     except Exception as e:
#         print(f"Database connection failed: {str(e)}")
#         raise

# def init_db():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS books (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             title TEXT NOT NULL
#         );
#     """)
#     cursor.execute("SELECT COUNT(*) FROM books")
#     if cursor.fetchone()[0] == 0:
#         cursor.execute("INSERT INTO books (title) VALUES ('Java book')")
#         cursor.execute("INSERT INTO books (title) VALUES ('Python book')")
    
#     conn.commit()
#     conn.close()

# init_db()

# class BooksGETResource(Resource):
#     def get(self):
#         conn = get_db_connection()
#         cursor = conn.cursor() 
#         cursor.execute("SELECT * FROM books")
#         result = [dict(row) for row in cursor.fetchall()]
#         conn.close()
#         return result

# class BookGETResource(Resource):
#     def get(self, id):
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         query = "SELECT * FROM books WHERE id = ?" 
#         cursor.execute(query, (id,))
        
#         result = cursor.fetchone()
#         conn.close()

#         if result:
#             return dict(result) 
        
#         return {"message": f"Book with id {id} not found"}, 404

# class BookPOSTResource(Resource):
#     def post(self):
#         try:
#             book_data = request.get_json(force=True)
#             title = book_data.get("title")
#         except:
#             return {"message": "Invalid JSON data provided"}, 400

#         if not title:
#             return {"message": "Missing 'title' field in request body"}, 400

#         conn = get_db_connection()
#         cursor = conn.cursor()

#         query = "INSERT INTO books (title) VALUES (?)"
#         cursor.execute(query, (title,))
        
#         new_id = cursor.lastrowid
#         conn.commit() 
#         conn.close()

#         return {"id": new_id, "title": title}, 201

# class BookPUTResource(Resource):
#     def put(self, id):
#         try:
#             book_data = request.get_json(force=True)
#             title = book_data.get("title")
#         except:
#             return {"message": "Invalid JSON data provided"}, 400
        
#         if not title:
#             return {"message": "Missing 'title' field for update"}, 400

#         conn = get_db_connection()
#         cursor = conn.cursor()
        
#         query = "UPDATE books SET title = ? WHERE id = ?"
#         cursor.execute(query, (title, id))
        
#         conn.commit()
        
#         if cursor.rowcount == 0:
#             conn.close()
#             return {"message": f"Book with id {id} not found"}, 404
        
#         conn.close()
#         return {"id": id, "title": title}

# class BookDELETEResource(Resource):
#     def delete(self, id):
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         query = "DELETE FROM books WHERE id = ?"
#         cursor.execute(query, (id,))
        
#         conn.commit()

#         if cursor.rowcount == 0:
#             conn.close()
#             return {"message": f"Book with id {id} not found"}, 404
            
#         conn.close()
#         return "", 204

"""
---- Version - 3 with MongoDB 
"""
from flask_restful import Resource
from flask import request
from pymongo import MongoClient
from bson.objectid import ObjectId

# ================================

# BASIC SECURITY (Username + Password)

# ================================

VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"

def check_credentials():
    username = request.headers.get("X-USERNAME")
    password = request.headers.get("X-PASSWORD")
    if username != VALID_USERNAME or password != VALID_PASSWORD:
        return False
    return True

# Configuration
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "emp"
COLLECTION_NAME = "emp"

def get_mongo_collection():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        return collection
    except Exception as e:
        print(f"MongoDB connection failed: {str(e)}")
        raise

def init_db():
    collection = get_mongo_collection()
    
    # Ensure collection exists and insert initial data if it's empty
    if collection.count_documents({}) == 0:
        initial_books = [
            {"title": "Java book"},
            {"title": "Python book"},
            {"title": "C++ book"},
            {"title": "Solidity book"},
            {"title": "PL/SQL book"},
            
        ]
        collection.insert_many(initial_books)

init_db()

# Helper function to convert MongoDB document (with ObjectId) to a serializable dictionary
def serialize_book(book):
    if book:
        # Convert ObjectId to string for JSON serialization
        book['_id'] = str(book['_id']) 
    return book

class BooksGETResource(Resource):
    def get(self):
        collection = get_mongo_collection()
        # Find all documents, convert them to a list, and serialize
        if check_credentials() == True:
            result = [serialize_book(book) for book in collection.find({})]
            return result
        else:
            return {"message":"Invalid Credentials !!!!!!!"},404

class BookGETResource(Resource):
    def get(self, id):
        collection = get_mongo_collection()
        
        try:
            # Convert string ID to ObjectId for MongoDB lookup
            book_id = ObjectId(id)
        except:
            return {"message": f"Invalid book ID format: {id}"}, 400
        # Find one document by its _id
        result = collection.find_one({"_id": book_id})
        
        if result:
            return serialize_book(result)
        
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

        collection = get_mongo_collection()
        
        new_book = {"title": title}
        # Insert the new document
        result = collection.insert_one(new_book)
        
        # Get the new ID and title from the inserted document
        new_id = str(result.inserted_id)

        return {"_id": new_id, "title": title}, 201

class BookPUTResource(Resource):
    def put(self, id):
        try:
            book_data = request.get_json(force=True)
            title = book_data.get("title")
        except:
            return {"message": "Invalid JSON data provided"}, 400
        
        if not title:
            return {"message": "Missing 'title' field for update"}, 400

        collection = get_mongo_collection()
        
        try:
            book_id = ObjectId(id)
        except:
            return {"message": f"Invalid book ID format: {id}"}, 400
        
        # Update the document
        update_result = collection.update_one(
            {"_id": book_id},
            {"$set": {"title": title}}
        )
        
        if update_result.matched_count == 0:
            return {"message": f"Book with id {id} not found"}, 404
        
        return {"_id": id, "title": title}

class BookDELETEResource(Resource):
    def delete(self, id):
        collection = get_mongo_collection()

        try:
            book_id = ObjectId(id)
        except:
            return {"message": f"Invalid book ID format: {id}"}, 400

        # Delete the document
        delete_result = collection.delete_one({"_id": book_id})

        if delete_result.deleted_count == 0:
            return {"message": f"Book with id {id} not found"}, 404
            
        return "", 204


