# pyright: ignore[reportMissingImports]
import streamlit as st # type: ignore
import pandas as pd # type: ignore
from PADataGenerator import Database, Filters, Students, Placements, Programming, Softskills

st.write("""# Placement Assistance App""")
st.write("## Welcome to the Placement Assistance App")

# This is a simple Streamlit app that allows users to select a batch and view the students in that batch.
class Templates:
    def __init__(self):
        pass


    def get_batch_names(self):
        filters = Filters(Database())
        #st.write(f"### Batch: {self.batch_name}")
        st.sidebar.write("## Select Filters")
        st.sidebar.write("### Batch Names")
        my_tuple = filters.get_batch_names()
        return my_tuple
        # batchNamesarr = [name[0] for name in batchNames]  # Extracting
        # batch = st.sidebar.selectbox("Select Course", batchNamesarr, index=0)
        # self.batch_name = str(batch)


    def get_programming_languages(self):
        filters = Filters(Database())
        programming_languages = filters.get_programming_languages()
        return programming_languages
        
    # def Show_batchwise_students(self, batch):
    #     # db = Database()
    #     # print(f"Selected batch: {batch}")
    #     # strquery = f"SELECT * FROM students WHERE course_batch in ({placehoders})"
    #     # print(f"Executing query: {strquery}")
    #     # db.cursor.execute(strquery, batch)
    #     filters = Filters(Database())
        
    #     students_batch = filters.get_students_by_filter(batch)
    #     students_df = pd.DataFrame(students_batch, columns=["student_id", "name", "age",
    #                                                         "gender", "email", "phone", "enrollment_year",
    #                                                         "course_batch", "city", "graduation_year"])
    #     st.write("### Students Data")
    #     st.dataframe(students_df)
    
    def show_filtered_students(self, batch, selected_language, programming=None, softskills=None, placements=None):
        filters = Filters(Database())
        students_batch = filters.get_students_by_filter(batch, selected_language, programming, softskills, placements)
        students_df = pd.DataFrame(students_batch, columns=["student_id", "name", "age",
                                                            "gender", "email", "phone", "enrollment_year",
                                                            "course_batch", "city", "graduation_year"])
        st.write("### Filtered Students Data")
        st.dataframe(students_df)




filterz = Templates()
DB = Filters(Database())

students = Students()
programming = Programming()
softskills = Softskills()
placements = Placements()
batches = filterz.get_batch_names()
if batches:
    st.sidebar.write("### Batches")
    # Create a multiselect widget for batch selection
    selected_batches = st.sidebar.multiselect("Select Batches", batches)
    # Convert the selected batches to a tuple
    selected_batches = ", ".join(f"'{item}' " for item in selected_batches)  # Convert list to tuple
print(f"Selected batches: {selected_batches}")

gender = st.sidebar.selectbox("Select", ("Select", "Male", "Female", "Other"))
match gender:
    case "Male":
        gender = "M"
    case "Female":
        gender = "F"
    case "Other":
        gender = "O"
    case _:
        gender = None

selected_languages = None
programminglang = filterz.get_programming_languages()
if programminglang:
    st.sidebar.write("### Programming Languages")
    lang = st.sidebar.multiselect("Select Programming Languages", programminglang)
    selected_languages = ", ".join(f"'{item}' " for item in lang) # Convert list to tuple
print(f"Selected programming languages: {selected_languages}")  

programming.problems_solved  = st.sidebar.slider("Number of Problems Solved", 0, 100)
if programming.problems_solved == 0:
    programming.problems_solved = None 
print(f"Problems Solved: {programming.problems_solved}")


programming.assessments_completed = st.sidebar.slider("Assessment Completed", 0, 12)
if programming.assessments_completed == 0:  
    programming.assessments_completed = None
print(f"Assessment Completed: {programming.assessments_completed}")

if not (programminglang 
        or (programming.problems_solved is not None and programming.problems_solved > 0) 
        or (programming.assessments_completed is not None and programming.assessments_completed > 0)):
    programming = None
    print(f"Programming object: {programming}")

softskills.communication_skills = st.sidebar.slider("Communication Skills", 0, 100)
if softskills.communication_skills == 0:
    softskills.communication_skills = None
print(f"Communication Skills: {softskills.communication_skills}")

softskills.teamwork_skills = st.sidebar.slider("Teamwork Skills", 0, 100)
if softskills.teamwork_skills == 0:
    softskills.teamwork_skills = None
print(f"Teamwork Skills: {softskills.teamwork_skills}")

softskills.presentation_skills = st.sidebar.slider("Presentation Skills", 0, 100)
if softskills.presentation_skills == 0: 
    softskills.presentation_skills = None
print(f"Presentation Skills: {softskills.presentation_skills}")

softskills.leadership_skills = st.sidebar.slider("Leadership Skills", 0, 100)
if softskills.leadership_skills == 0 :
    softskills.leadership_skills = None
print(f"Leadership Skills: {softskills.leadership_skills}")

softskills.critical_thinking_skills = st.sidebar.slider("Critical Thinking Skills", 0, 100)
if softskills.critical_thinking_skills == 0:
    softskills.critical_thinking_skills = None
print(f"Critical Thinking Skills: {softskills.critical_thinking_skills}")

softskills.interpersonal_skills = st.sidebar.slider("Interpersonal Skills", 0, 100)
if softskills.interpersonal_skills == 0:
    softskills.interpersonal_skills = None
print(f"Interpersonal Skills: {softskills.interpersonal_skills}")

if not ((softskills.communication_skills  is not None and softskills.communication_skills > 0)
        or (softskills.teamwork_skills is not None and  softskills.teamwork_skills > 0) 
        or (softskills.presentation_skills is not None and softskills.presentation_skills > 0)
        or (softskills.leadership_skills is not None and softskills.leadership_skills > 0)
        or (softskills.critical_thinking_skills is not None and  softskills.critical_thinking_skills > 0) 
        or (softskills.interpersonal_skills is not None and  softskills.interpersonal_skills > 0)):
    softskills = None
    print(f"Softskills object: {softskills}")


placements.mock_interview_score = st.sidebar.slider("Mock Interview", 0, 10)
if placements.mock_interview_score == 0:
    placements.mock_interview_score = None
print(f"Mock Interview Score: {placements.mock_interview_score}")

placements.internships_completed = st.sidebar.slider("Internships Completed", 0, 5)
if placements.internships_completed > 0:
    placements.internships_completed = None
print(f"Internships Completed: {placements.internships_completed}")

placements.placement_status = st.sidebar.selectbox("Placement Selected", ("Select", "Not Ready", "Ready", "Placed"))
if placements.placement_status != "Select":
    placements.placement_status = placements.placement_status
    print(f"Placement Status: {placements.placement_status}")
else:
    placements.placement_status = None
    print("Placement Status: Not Selected")




if selected_batches or selected_languages or programming or softskills or placements:
    st.write("### Filtered Students") 
    # Show filtered students based on selected batches and programming languages
    students_dataset = DB.get_students_by_filter(selected_batches, gender, selected_languages, programming, softskills, placements)

    students_df = pd.DataFrame(students_dataset, columns=["student_id", "name", "age",
                                                        "gender", "email", "phone", "enrollment_year",
                                                        "course_batch", "city", "graduation_year"])
    st.dataframe(students_df)
