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


class Filters:
    def __init__(self, db):
        self.db = db

    def get_batch_names(self):
        db = Database()
        batchNames = db.cursor.execute("SELECT distinct(course_batch) FROM students order by course_batch;")
        batchNames = db.cursor.fetchall()
        my_tuple = tuple(item[0] for item in batchNames)
        print(f"Batch names fetched from database: {my_tuple}", type(my_tuple))
        db.close()
        return my_tuple
    
    def get_students_by_filter(self, batch = None, programming_language=None):
        #db = Database()
        sqlQuery = "SELECT * FROM students stds"
        filterstring = ''
        if programming_language is not None:
            filterstring = f" join programming pgm ON stds.student_id = pgm.student_id and language in ({programming_language}) "

        if batch is not None:
            if( filterstring == ''):
                filterstring += " WHERE "
                filterstring += f"course_batch IN ({batch})"

        print(f"Batch: {batch}, Programming Language: {programming_language} filterstring: {filterstring}")
        if filterstring:
            filterstring = " WHERE " + filterstring if not filterstring.startswith(" WHERE ") else " AND " + filterstring

        print(f"Executing SQL Query: {sqlQuery + filterstring}")
        
        self.db.cursor.execute(sqlQuery + filterstring)
        students_batch = self.db.cursor.fetchall()
        return students_batch
    def get_programming_languages(self):
        db = Database()
        db.cursor.execute("SELECT distinct(language) FROM programming order by language;")
        programming_languages = db.cursor.fetchall()
        my_tuple = tuple(item[0] for item in programming_languages)
        print(f"Programming languages fetched from database: {my_tuple}", type(my_tuple))
        db.close()
        return my_tuple

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
        self.generate_students_table()
    
    @staticmethod
    def generate_student_data(student_id):
        logging.info(f"Generating data for student ID: {student_id}")
        fake = fk('en_US')
        student = Students()
        student.student_id = student_id
        student.name = fake.name()
        student.age = fake.random_int(min=18, max=25)
        student.gender = fake.random_element(elements=("M", "F"))
        student.email = fake.email(student.name)
        phone = fake.random_int(min=1111111111, max=9999999999)
        logging.info(f"Generated phone number: {phone}")
        # Ensure phone number is a string and formatted correctly
        student.phone = phone
        student.enrollment_year = fake.random_int(min=2015, max=2025)   
        student.course_batch = f"MDT_{fake.random_element(elements=('A', 'B', 'C', 'D'))}"
        student.city = fake.city()
        student.graduation_year = fake.random_int(student.enrollment_year + 3, student.enrollment_year + 4)
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

    def generate_students_table(self):
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
        
       

class Programming:
    def __init__(self, programming_id=0, student_id=0, language="", problems_solved="", assessments_completed=""):
        self.programming_id = programming_id
        self.student_id = student_id
        self.language = language
        self.problems_solved = problems_solved
        self.assessments_completed = assessments_completed
        self.generate_programming_table()
        
    @staticmethod
    def generate_programming_data(programming_id, student_id):
        fake = fk('en_US')
        programming = Programming()
        programming.programming_id = programming_id
        programming.student_id = student_id
        programming.language = fake.random_element(elements=("Python", "Java", "C++", "JavaScript", "Ruby","C#.Net", "PHP", "Swift", "Go", "Kotlin"))
        programming.problems_solved = fake.random_int(min=1, max=100) 
        programming.assessments_completed = fake.random_int(min=1, max=12)
        return programming

    @staticmethod
    def insert_programming(db, programming):
        query = """
        INSERT INTO programming (programming_id, student_id, language, problems_solved, assessments_completed)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (programming.programming_id, programming.student_id, programming.language, programming.problems_solved, programming.assessments_completed)
        db.cursor.execute(query, values)
        db.conn.commit()


    def generate_programming_table(self):
        db = Database()
        GenerateProgrammingTable = """CREATE TABLE IF NOT EXISTS programming (
            programming_id INT PRIMARY KEY,
            student_id INT,
            language VARCHAR(50),
            problems_solved INT,
            assessments_completed INT,
            FOREIGN KEY (student_id) REFERENCES students(student_id))"""
        logging.info("Creating programming table if it does not exist.")
        db.cursor.execute(GenerateProgrammingTable)
        logging.info("Programming table created successfully.")
        db.close()

class Softskills:
    def __init__(self, softskills_id=0, student_id=0, communication_skills=0, teamwork_skills=0, presentation_skills=0, leadership_skills=0, critical_thinking_skills= 0, interpersonal_skills = 0):
        self.softskill_id = softskills_id
        self.student_id =student_id
        self.communication_skills  = communication_skills
        self.teamwork_skills =teamwork_skills
        self.presentation_skills = presentation_skills
        self.leadership_skills = leadership_skills
        self.critical_thinking_skills = critical_thinking_skills
        self.interpersonal_skills = interpersonal_skills 
        self.generate_softskills_table()   
        
    @staticmethod
    def generate_softskills_data(softskills_id, student_id):
        fake = fk('en_US')
        softskills = Softskills()
        softskills.softskills_id = softskills_id
        softskills.student_id = student_id
        softskills.communication_skills = fake.random_int(min=1, max=100)
        softskills.teamwork_skills = fake.random_int(min=1, max=100)
        softskills.presentation_skills = fake.random_int(min=1, max=100)
        softskills.leadership_skills = fake.random_int(min=1, max=100)
        softskills.critical_thinking_skills = fake.random_int(min=1, max=100)
        softskills.interpersonal_skills = fake.random_int(min=1, max=100)
        return softskills

    @staticmethod
    def insert_softskills(db, softskills):
        query = """
        INSERT INTO softskills (softskills_id, student_id, communication_skills, teamwork_skills, presentation_skills, leadership_skills, critical_thinking_skills, interpersonal_skills)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (softskills.softskills_id, softskills.student_id, softskills.communication_skills,
                  softskills.teamwork_skills, softskills.presentation_skills,
                  softskills.leadership_skills, softskills.critical_thinking_skills, softskills.interpersonal_skills)
        logging.info(f"Inserting soft skills data for student ID: {softskills.student_id}")
        db.cursor.execute(query, values)
        db.conn.commit()

    def generate_softskills_table(self):
        db = Database()

        GenerateSoftSkillsTable = """CREATE TABLE IF NOT EXISTS softskills (
            softskills_id INT PRIMARY KEY,
            student_id INT,
            communication_skills INT,
            teamwork_skills INT,
            presentation_skills INT,
            leadership_skills INT,
            critical_thinking_skills INT,
            interpersonal_skills INT,
            FOREIGN KEY (student_id) REFERENCES students(student_id))"""
        logging.info("Creating soft skills table if it does not exist.")
        db.cursor.execute(GenerateSoftSkillsTable)
        logging.info("Soft skills table created successfully.")
        db.close()

class Placements:
    def __init__(self, placement_id=0, student_id=0, mock_interview_score=0, internships_completed=0,   placement_status="", company_name="", placement_package="", interview_rounds_cleared=0, placement_date=""):
        self.placement_id  = placement_id
        self.student_id = student_id
        self.mock_interview_score = mock_interview_score
        self.internships_completed =internships_completed
        self.placement_status = placement_status
        self.company_name  = company_name
        self.placement_package =placement_package
        self.interview_rounds_cleared =interview_rounds_cleared
        self.placement_date =placement_date
        self.generate_placement_table()
        

    @staticmethod
    def generate_placement_data(placement_id, student_id):
        fake = fk('en_US')
        placement = Placements()
        placement.placement_id = placement_id
        placement.student_id = student_id
        placement.mock_interview_score = fake.random_int(min=0, max=100)
        placement.internships_completed = fake.random_int(min=0, max=5)
        logging.info(f"Generated mock interview score: {placement.mock_interview_score}")
        placement.placement_status = fake.random_element(["Ready",  "Not Ready", "Placed"])
        logging.info(f"Generated placement status: {placement.placement_status}")
        placement.company_name = fake.company()
        placement.placement_package = fake.random_int(min=300000, max=2000000)
        placement.interview_rounds_cleared = fake.random_int(min=0, max=5)
        placement.placement_date = fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d')
        logging.info(f"Placement date : {placement.placement_date}")
        return placement
    
    def insert_placement(db, placement):
        query = """
        INSERT INTO placements (placement_id, student_id, mock_interview_score, internships_completed, placement_status, company_name, placement_package, interview_rounds_cleared, placement_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (placement.placement_id, placement.student_id, placement.mock_interview_score,
                  placement.internships_completed, placement.placement_status,
                  placement.company_name, placement.placement_package,
                  placement.interview_rounds_cleared, placement.placement_date)
        logging.info(f"Insert statement: {query}")
        logging.info(f"Inserting placement data for student ID: {placement.student_id}")
        db.cursor.execute(query, values)
        db.conn.commit()
    
    def generate_placement_table(self):
        db = Database()

        GeneratePlacementTable = """CREATE TABLE IF NOT EXISTS placements (
            placement_id INT PRIMARY KEY,
            student_id INT,
            mock_interview_score INT,
            internships_completed INT,
            placement_status VARCHAR(20),
            company_name VARCHAR(100),
            placement_package FLOAT,
            interview_rounds_cleared INT,
            placement_date DATE,
            FOREIGN KEY (student_id) REFERENCES students(student_id))"""
        logging.info("Creating placement table if it does not exist.")
        db.cursor.execute(GeneratePlacementTable)
        logging.info("Placement table created successfully.")
        db.close()


if __name__ == "__main__":
    logging.info("Starting student generation and insertion...")
    try:
       
        # Create database connection
        StudentsInstance = Students()
        ProgrammingInstance = Programming()
        SoftskillsInstance = Softskills()
        PlacementInstance = Placements()

        db = Database()
        # studentsCountQry = """SELECT * FROM students"""
        db.cursor.execute("SELECT count(*) FROM students")
        count = int(db.cursor.fetchone()[0])
        for index in range(1, 500):
            replaced_index = index + count
            student = StudentsInstance.generate_student_data(replaced_index)
            logging.info(f"Generated student data for ID: {replaced_index}")
            StudentsInstance.insert_student(db, student)
            logging.info(f"Inserted student data for ID: {replaced_index}")
            programming = Programming.generate_programming_data(replaced_index, replaced_index)
            logging.info(f"Generated programming data for student ID: {replaced_index}")
            Programming.insert_programming(db, programming)
            logging.info(f"Inserted programming data for student ID: {replaced_index}")
            softskills = Softskills.generate_softskills_data(replaced_index, replaced_index)
            logging.info(f"Generated soft skills data for student ID: {replaced_index}")
            Softskills.insert_softskills(db, softskills)
            logging.info(f"Inserted soft skills data for student ID: {replaced_index}")
            placement = Placements.generate_placement_data(replaced_index, replaced_index)
            logging.info(f"Generated placement data for student ID: {replaced_index}")
            Placements.insert_placement(db, placement)
            logging.info(f"Inserted placement data for student ID: {replaced_index}")
        db.close()
        logging.info("Student generation and insertion completed.")
    except Exception as e:
        logging.critical(f"Unhandled exception: {e}")