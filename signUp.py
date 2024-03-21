from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

import pyodbc
import hashlib

app = Flask(__name__)
CORS(app)
api = Api(app)

def get_db_connection():
    conn_str = (
        "Driver={SQL Server};"
        "Server=DESKTOP-C2EETSN;"
        "Database=HunaAI;"
        "Trusted_Connection=yes;"
    )
    conn = pyodbc.connect(conn_str)
    return conn


class SignUp(Resource):
    def post(self):
        data = request.json
        conn = None  
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                password_hash = hashlib.sha256(data["password"].encode()).hexdigest()
                cursor.execute(
                    "INSERT INTO Users (FirstName, LastName, Username, PhoneNumber, Email, PasswordHash, Provider) VALUES (?, ?, ?, ?, ?, ?, 'Local')",
                    (data["firstName"], data["lastName"], data["username"], data["phoneNumber"], data["email"], password_hash)
                )
                conn.commit()
            return {"message": "User registered successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            if conn is not None: 
                conn.close()


api.add_resource(SignUp, "/signup")

if __name__ == "__main__":
    app.run(debug=True)
