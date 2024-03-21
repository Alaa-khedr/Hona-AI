from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import pyodbc
import hashlib
from flask_cors import CORS


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


class ResetPassword(Resource):
    def post(self):
        data = request.json
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT UserID FROM Users WHERE PasswordResetToken = ? AND PasswordResetTokenExpiry > GETDATE()",
                    (data["token"],),
                )
                user = cursor.fetchone()
                if user:
                    new_password_hash = hashlib.sha256(
                        data["new_password"].encode()
                    ).hexdigest()
                    cursor.execute(
                        "UPDATE Users SET PasswordHash = ?, PasswordResetToken = NULL, PasswordResetTokenExpiry = NULL WHERE UserID = ?",
                        (new_password_hash, user[0]),
                    )
                    conn.commit()
                    return {
                        "message": "Your password has been reset successfully."
                    }, 200
                else:
                    return {"message": "Invalid or expired token"}, 400
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()


api.add_resource(ResetPassword, "/reset-password")

if __name__ == "__main__":
    app.run(debug=True)
