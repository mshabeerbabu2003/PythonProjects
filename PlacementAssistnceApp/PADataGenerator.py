import mysql.connector as mysql
import pandas as pd
from faker import Faker as fk
import logging

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("student_data_generator.log"),
        logging.StreamHandler()
    ]
)


class Database:
    def __init__(self):
        connstring = {}
        self.conn = mysql.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            user="51GXEaMuDfyhKHU.root",
            password='q2Nq0XMq5CK7eHAb',
            database='MDT54Shabeer',
            port=4000)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()



class Students:
    def __init__(self, student_id=0, name="", age=0, gender="", email="", phone="", enrollment_year=0, course_batch="", city="", graduation_year=0):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gender = gender
        self.email = email
        self.phone = phone
        self.enrollment_year = enrollment_year
        self.course_batch = course_batch
        self.city = city
        self.graduation_year = graduation_year
    
    @staticmethod
    def generate_student_data(student_id):



        logging.info(f"Generating data for student ID: {student_id}")
        fake = fk('en_US')
        student = Students()
        student.student_id = student_id
        student.name = fake.name()
        student.age = fake.random_int(min=18, max=25)
        student.gender = fake.random_element(elements=("M", "F"))
        student.email = fake.email()
        phone = fake.random_int(min=1111111111, max=9999999999)
        logging.info(f"Generated phone number: {phone}")
        # Ensure phone number is a string and formatted correctly
        student.phone = phone
        student.enrollment_year = fake.year()   
        student.course_batch = f"MDT_{fake.random_element(elements=('A', 'B', 'C', 'D'))}"
        student.city = fake.city()
        student.graduation_year = fake.year()
        return student

    @staticmethod
    def insert_student(db, student):
        query = """
        INSERT INTO students (student_id, name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (student.student_id, student.name, student.age, student.gender, student.email, student.phone,
                student.enrollment_year, student.course_batch, student.city, student.graduation_year)
        db.cursor.execute(query, values)
        db.conn.commit()

    def generate_and_insert_students(self, num_students):
        db = Database()

        GenerateStudentTable = """CREATE TABLE IF NOT EXISTS students (
            student_id INT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            gender CHAR(1),
            email VARCHAR(100),
            phone VARCHAR(20),
            enrollment_year INT,
            course_batch VARCHAR(10),
            city VARCHAR(50),
            graduation_year INT)"""
        logging.info("Creating students table if it does not exist.")
        db.cursor.execute(GenerateStudentTable)
        logging.info("Students table created successfully.")
        
        for student_id in range(1, num_students + 1):
            student = self.generate_student_data(student_id)
            self.insert_student(db, student)
        db.close()


if __name__ == "__main__":
    logging.info("Starting student generation and insertion...")
    try:
        StudentsInstance = Students()
        StudentsInstance.generate_and_insert_students(10)
        logging.info("Student generation and insertion completed.")
    except Exception as e:
        logging.critical(f"Unhandled exception: {e}")