
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd 

st.title("Naveen Form")
st.markdown("enter the details of new student below")

conn = st.connection("gsheets",type=GSheetsConnection)

existing_data=conn.read(worksheet="Form",usecols=list(range(6)),ttl=5)
existing_data=existing_data.dropna(how="all")


GENDER_TYPES ={
    "MALE",
    "FEMALE",
}
DEPARTMENT_TYPES={
    "CSE" ,
    "ECE" ,
    "EEE",
    "MECH",
    "CIVIL",
}
with st.form(key="webdevolopment_form"):
    Studentname=st.text_input(label="Student Name*",)
    Rollno=st.text_input(label="rollno*")
    Gender=st.selectbox("Gender",options=GENDER_TYPES,index=None)
    Dept=st.selectbox("Department",options=DEPARTMENT_TYPES)
    Dob=st.text_input(label="DOB")
    description=st.text_area(label="Description")

    st.markdown("**required*")

    submit_button=st.form_submit_button(label="submit")


    if submit_button:
        if not Studentname or not Rollno:
            st.warning("ensure all mandetory field are filled")
            st.stop()
        elif existing_data["Name"].str.contains(Studentname).any():
            st.warning("A student with this name already exist")
            st.stop()
        else:
            student_data=pd.DataFrame(
                [
                    {
                        "Name":Studentname,
                        "Roll No":Rollno,
                        "Gender":Gender,
                        "Dept":Dept,
                        "DOB":Dob,
                        "Description":description,
                    }
                ]
            )

            updated_df=pd.concat([existing_data,student_data],ignore_index=True)

            conn.update(worksheet="Form",data=updated_df)

            st.success("student details successfully submitted")

            
