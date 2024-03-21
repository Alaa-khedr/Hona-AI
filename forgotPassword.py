from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import pyodbc
import uuid
import datetime
from flask_cors import CORS
import traceback

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

class ForgotPassword(Resource):
    def post(self):
        data = request.json
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT Email FROM Users WHERE Email = ?", (data["email"],)
                )
                user = cursor.fetchone()
                if user:
                    reset_token = str(uuid.uuid4())
                    expiry_time = datetime.datetime.now() + datetime.timedelta(hours=1)
                    cursor.execute(
                        "UPDATE Users SET PasswordResetToken = ?, PasswordResetTokenExpiry = ? WHERE Email = ?",
                        (reset_token, expiry_time, data["email"]),
                    )
                    conn.commit()

                    # Send the reset token to the user's email. This is just a placeholder;
                    print(f"Reset token for {data['email']}: {reset_token}")

                    return {
                        "message": "A password reset token has been sent to your email."
                    }, 200
                else:
                    return {"message": "User not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()


api.add_resource(ForgotPassword, "/forgot-password")

if __name__ == "__main__":
    app.run(debug=True)
