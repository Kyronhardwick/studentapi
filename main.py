from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mysql.connector import MySQLConnection
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

app = FastAPI()

# Define the model for the data
class Student(BaseModel):
    id: int
    name: str
    age: int
    grade: float

password=os.environ.get('PASSWORD')
host=os.environ.get('HOST')
user=os.environ.get('USER')
db=os.environ.get('DATABASE')
port=os.environ.get('PORT')


# Define the connection parameters
connection_params = {
    'user': user,
    'password': password,
    'host': host,
    'database': db,
    'port': port
}
# Connect to the database
connection = MySQLConnection(**connection_params)

# Create a student
@app.post("/students/")
def create_student(student: Student):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO students.student (id, name, age, grade) VALUES (%s, %s, %s, %s)", (student.id, student.name, student.age, student.grade))
    connection.commit()
    return student

# Read a student by ID
@app.get("/students/{student_id}")
def read_student(student_id: int):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students.student WHERE id = %s", (student_id,))
    result = cursor.fetchone()
    if result:
        return {
            'id': result[0],
            'name': result[1],
            'age': result[2],
            'grade': result[3]
        }
    else:
        raise HTTPException(status_code=404, detail="Student not found")

# Update a student by ID
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    cursor = connection.cursor()
    cursor.execute("UPDATE students.student SET name = %s, age = %s, grade = %s WHERE id = %s", (student.name, student.age, student.grade, student_id))
    connection.commit()
    return student

# Delete a student by ID
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM students.student WHERE id = %s", (student_id,))
    connection.commit()
    return {"message": "Student deleted"}

# Close the database connection
@app.on_event("shutdown")
async def shutdown_event():
    if connection.is_connected():
        connection.close()