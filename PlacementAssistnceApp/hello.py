import streamlit as st
import pandas as pd
from faker import Faker as fk
import mysql.connector as mysql




class database:
    def __init__(self):
        self.conn = mysql.connect(
            host="ggateway01.ap-southeast-1.prod.aws.tidbcloud.com",
                             user="51GXEaMuDfyhKHU.root",
                             password='q2Nq0XMq5CK7eHAb',
                             database='MDT54Shabeer'
                             port=4000
        )

# name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year
class Students:
    def __init__(self, student_id=0, name="", age, gender="", email="", phone="", enrollment_year=0, course_batch="", city="", graduation_year=0):
        self.student_id : int = 0
        self.name :str = ""
        self.age : int = 0
        self.gender : str = ""
        self.email : str = ""
        self.phone : str = ""
        self.enrollment_year : int = 0
        self.course_batch : str = ""
        self.city : str = ""
        self.graduation_year : int = 0
        
    
    def generate_student_data(self, student_id):
        fake = fk('en_US')
        student = None
        #for i in range(500):
        student = Students()
        student.student_id = student_id
        student.name = fake.name()
        student.age = fake.random_int(min=18, max=25)
        student.gender = fake.random_element("M", "F")
        student.email = fake.email()        
        student.phone = fake.phone_number()
        student.enrollment_year = fake.year(2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025)
        student.course_batch = f"MDT_{fake.random_element("A", "B", "C", "D")}"
        student.city = fake.city()
        student.graduation_year = fake.year(2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025)
            #insert_student(self, student)

    def insert_student(self, student):
        # Code to insert student data into the database
        pass
            
    
class Programming:
    def __init__(self):
        self.progrmming_id : int = 0
        self.studentid : int = 0
        self.language : str = ""
        self.problem_solved : int  = 0
        self.assessment_completed : int = 0
        self.mini_project : int = 0
        self.certifications_earned : int = 0
        self.latest_project_score : int = 0
        
    def generate_programming_data(self, studentid):
        fake = fk('en_US')
        programming = None
        #for i in range(500):
        programming = Programming()
        programming.progrmming_id = i + 1
        programming.studentid = i + 1
        programming.language = fake.random_element("Python", "Java", "C++", "JavaScript", "Ruby")
        programming.problem_solved = fake.random_int(min=0, max=100)
        programming.assessment_completed = fake.random_int(min=0, max=10)
        programming.mini_project = fake.random_int(min=0, max=5)
        programming.certifications_earned = fake.random_int(min=0, max=3)
        programming.latest_project_score = fake.random_int(min=0, max=100)
            #insert_programming(self, programming)
        
    def insert_programming(self, programming):
        # Code to insert programming data into the database
        pass

class SoftSkills:
    def __init__(self):
        self.softskill_id : int = 0
        self.studentid : int = 0
        self.communication_skills : int = 0
        self.teamwork_skills : int = 0
        self.presentation_skills : int = 0
        self.leadership_skills : int = 0
        self.critical_thinking_skills : int = 0
        self.interpersonal_skills : int = 0

        
    def generate_softskills_data(self, softskill_id, studentid):
        fake = fk('en_US')
        softskills = None
        #for i in range(500):
        softskills = SoftSkills()
        softskills.softskill_id = softskill_id
        softskills.studentid = studentid
        softskills.communication_skills = fake.random_int(min=0, max=100)
        softskills.teamwork_skills = fake.random_int(min=0, max=100)
        softskills.critical_thinking_skills = fake.random_int(min=0, max=100)
        softskills.interpersonal_skills = fake.random_int(min=0, max=100)
        softskills.leadership_skills = fake.random_int(min=0, max=100)
            #insert_softskills(self, softskills)
        
    def insert_softskills(self, softskills):
        # Code to insert soft skills data into the database
        pass

class Placement:
    def __init__(self):
        self.placement_id : int = 0
        self.studentid : int = 0
        self.mock_interview_score : int = 0
        self.internships_completed : int = 0
        self.placement_status : int = 0
        self.company_name : str = ""
        self.placement_package : float = 0.0
        self.interview_rounds_cleared : int = 0
        self.placement_date : str = ""
        
    def generate_placement_data(self, studentid):
        fake = fk('en_US')
        placement = None
        for i in range(500):
            placement = Placement()
            placement.placement_id = i + 1
            placement.studentid = i + 1
            placement.mock_interview_score = fake.random_int(min=0, max=100)
            placement.internships_completed = fake.random_int(min=0, max=5)
            placement.placement_status = fake.random_element("Ready", "Placed", "Not Ready")
            placement.company_name = fake.company()
            placement.placement_package = fake.random_int(min=300000, max=2000000)
            placement.interview_rounds_cleared = fake.random_int(min=0, max=5)
            placement.placement_date = fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
            #insert_placement(self, placement)
        
    def insert_placement(self, placement):
        # Code to insert placement data into the database
        pass




