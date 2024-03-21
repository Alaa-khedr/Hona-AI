from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import pyodbc
import hashlib

app = Flask(__name__)
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


class Login(Resource):
    def post(self):
        data = request.json
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT UserID, PasswordHash FROM Users WHERE Email = ?",
                    (data["email"],),
                )
                user = cursor.fetchone()
                if user:
                    password_hash = hashlib.sha256(
                        data["password"].encode()
                    ).hexdigest()
                    if password_hash == user[1]:
                        return {"message": "Login successful", "UserID": user[0]}, 200
                    else:
                        return {"message": "Invalid credentials"}, 401
                else:
                    return {"message": "User not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()


api.add_resource(Login, "/login")


if __name__ == "__main__":
    app.run(debug=True)
