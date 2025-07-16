import streamlit as st
import pandas as pd
from PADataGenerator import Database, Filters

st.write("""# Placement Assistance App""")
st.write("## Welcome to the Placement Assistance App")

# This is a simple Streamlit app that allows users to select a batch and view the students in that batch.
class Templates:
    def __init__(self):
        pass


    def get_batch_names(self):
        filters = Filters(Database())
        #st.write(f"### Batch: {self.batch_name}")
        st.write("This is the batch information.")
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
    
    def show_filtered_students(self, batch, selected_options):
        filters = Filters(Database())
        students_batch = filters.get_students_by_filter(batch, selected_options)
        students_df = pd.DataFrame(students_batch, columns=["student_id", "name", "age",
                                                            "gender", "email", "phone", "enrollment_year",
                                                            "course_batch", "city", "graduation_year"])
        st.write("### Filtered Students Data")
        st.dataframe(students_df)




filterz = Templates()
batches = filterz.get_batch_names()
selected_batches_arr = []
selected_batches = tuple()  # Initialize as an empty tuple
# Iterate through the tuple and create a checkbox for each item
for item in batches:
    # st.checkbox returns True if checked, False otherwise
    if st.sidebar.checkbox(item):
        selected_batches_arr.append(item)
        selected_batches = tuple(selected_batches_arr)  # Convert list to tuple

    
if not selected_batches:
        st.write("No batch selected.")
        # filterz.Show_programming_languages(selected_batches)

    

#st.subheader("Selected Options:")
# if selected_options:
#     #placeholders = ', '.join(['%s'] * len(selected_options))
#     filterz.Show_batchwise_students(tuple(selected_options))  # Show students for the all selected batch
        
# else:
#     st.write("No options selected.")
selected_languages = []
programminglang = filterz.get_programming_languages()
if programminglang:
    st.sidebar.write("### Programming Languages")
    selected_languages = st.sidebar.multiselect("Select Programming Languages", programminglang)


problems_solved  = st.sidebar.slider("Number of Problems Solved", 0, 100)

assessment_Completed = st.sidebar.slider("Assessment Completed", 0, 12)

communication_Skills = st.sidebar.slider("Communication Skills", 0, 100)

teamwork_Skills = st.sidebar.slider("Teamwork Skills", 0, 100)

Presentation_Skills = st.sidebar.slider("Presentation Skills", 0, 100)

leadership_Skills = st.sidebar.slider("Leadership Skills", 0, 100)

critical_Thinking_Skills = st.sidebar.slider("Critical Thinking Skills", 0, 100)

interpersonal_Skills = st.sidebar.slider("Interpersonal Skills", 0, 100)

mock_Interview = st.sidebar.slider("Mock Interview", 0, 10)

internships_completed = st.sidebar.slider("Internships Completed", 0, 5)

placement_selected = st.sidebar.selectbox("Placement Selected", ("Not Ready", "Ready", "Placed"))




if selected_batches and selected_languages:
    st.write("### Selected Batches and Programming Languages")
    st.write(f"Selected Batches: {selected_batches}")
    st.write(f"Selected Programming Languages: {selected_languages}")
    
    # Show filtered students based on selected batches and programming languages
    filterz.show_filtered_students(selected_batches, selected_languages)



# batchNamesarr = [name for name in batches]  # Extracting
# batch = st.sidebar.selectbox("Select Course", batchNamesarr, index=0)
# print(f"Selected batch: {batch}")
# filterz.Show_batchwise_students(batch)

# st.sidebar.slidebar("")