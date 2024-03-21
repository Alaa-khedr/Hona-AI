import pyodbc
from flask import Flask, jsonify
from flask_restful import Resource, Api

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

class AllQuestions(Resource):
    def get(self):
        try:
            conn = get_db_connection()
            questions_list = []
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Prompts")
                results = cursor.fetchall()
                for result in results:
                    question_data = {
                        "QuestionID": result[0],
                        "QuestionText": result[1],
                        "Prompts": [result[i] for i in range(2, 12) if result[i] is not None],
                        "Notes": result[12]
                    }
                    questions_list.append(question_data)
            return jsonify(questions_list)
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()

api.add_resource(AllQuestions, '/prompts')


class Prompts(Resource):
    def get(self, question_id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Prompts WHERE QuestionID = ?", (question_id,))
                result = cursor.fetchone()
                if result:
                    prompts_data = {
                        "QuestionID": result[0],
                        "QuestionText": result[1],
                        "Prompts": [result[i] for i in range(2, 12)],
                        "Notes": result[12]
                    }
                    return jsonify(prompts_data)
                else:
                    return {"message": "Question not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()

api.add_resource(Prompts, '/prompts/<int:question_id>')

if __name__ == "__main__":
    app.run(debug=True)