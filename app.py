import pyodbc
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)  

def get_db_connection():
    conn_str = (
        "Driver={SQL Server};"
        "Server=DESKTOP-C2EETSN;"  
        "Database=HunaAI;" 
        "Trusted_Connection=yes;"
    )
    conn = pyodbc.connect(conn_str)
    return conn


  
@app.route('/categoryName=<categoryName>')
def index(categoryName):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Tools WHERE Category=?", (categoryName,))
            tools = cursor.fetchall()

            tool_list = []
            for tool in tools:
                tool_data = {
                    "ToolID": tool[0],
                    "Name": tool[1],
                    "Category": tool[2],
                    "Details": tool[3],
                    "InstructionalVideoURL": tool[4],
                    "SupportedLanguages": tool[5],
                    "PricingModel": tool[6],
                    "LinkURL": tool[7],
                    "ImageURL": tool[8],
                }
                tool_list.append(tool_data)

            return {"tools": tool_list}
    except Exception as e:
        return "error", str(e)

@app.route('/Name=<Name>')
def index2(Name):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Tools WHERE Name=?", (Name,))
            tools = cursor.fetchall()

            tool_list = []
            for tool in tools:
                tool_data = {
                    "ToolID": tool[0],
                    "Name": tool[1],
                    "Category": tool[2],
                    "Details": tool[3],
                    "InstructionalVideoURL": tool[4],
                    "SupportedLanguages": tool[5],
                    "PricingModel": tool[6],
                    "LinkURL": tool[7],
                    "ImageURL": tool[8],
                }
                tool_list.append(tool_data)

            return {"tools": tool_list}
    except Exception as e:
        return "error", str(e)

@app.route('/ToolID=<ToolID>')
def index4(ToolID):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Tools WHERE ToolID=?", (ToolID,))
            tools = cursor.fetchall()

            tool_list = []
            for tool in tools:
                tool_data = {
                    "ToolID": tool[0],
                    "Name": tool[1],
                    "Category": tool[2],
                    "Details": tool[3],
                    "InstructionalVideoURL": tool[4],
                    "SupportedLanguages": tool[5],
                    "PricingModel": tool[6],
                    "LinkURL": tool[7],
                    "ImageURL": tool[8],
                }
                tool_list.append(tool_data)

            return {"tools": tool_list}
    except Exception as e:
        return "error", str(e)

@app.route('/tools')
def getAllTools():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Tools")
            tools = cursor.fetchall()

            tool_list = []
            for tool in tools:
                tool_data = {
                    "ToolID": tool[0],
                    "Name": tool[1],
                    "Category": tool[2],
                    "Details": tool[3],
                    "InstructionalVideoURL": tool[4],
                    "SupportedLanguages": tool[5],
                    "PricingModel": tool[6],
                    "LinkURL": tool[7],
                    "ImageURL": tool[8],
                }
                tool_list.append(tool_data)
            return {"tools": tool_list}
    except Exception as e:
        return "error", str(e)
if __name__ == "__main__":
    app.run(debug=True)
