import streamlit as st
import pandas as pd
import re

from datetime import date, datetime

from crud import (
    create_patient,
    get_patients,
    delete_patient,
    update_patient,
    get_patient_by_id
)

from ai_service import (
    generate_prediction
)


# PAGE CONFIG

st.set_page_config(
    page_title="AI Health Prediction",
    page_icon="🩺",
    layout="wide"
)


# CUSTOM CSS

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

h1 {
    color: #9935b8;
    text-align: center;
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg,#9e5cc4,#06b6d4);
    padding: 20px;
    border-radius: 15px;
    color: white;
}

.stButton>button {
    background-color: #9935b8;
    color: white;
    border-radius: 10px;
    height: 50px;
    font-weight: bold;
    width: 100%;
}

.stButton>button:hover {
    background-color: #9935b8;
}

</style>
""", unsafe_allow_html=True)

# TITLE

st.title("🩺 AI Health Prediction Application")
st.markdown("---")



# DASHBOARD

patients = get_patients()
total_patients = len(patients)
high_risk = 0

for patient in patients:
    remarks = str(patient[7]).lower()

    if "low risk" in remarks or "normal" in remarks:
        continue

    if (
        "risk" in remarks
        or "anemia" in remarks
        or "disease" in remarks
        or "elevated" in remarks
        or "diabetic" in remarks
        or "prediabetes" in remarks
    ):
        high_risk += 1

c1, c2, c3 = st.columns(3)
with c1:
    st.metric(
        "Total Patients",
        total_patients
    )

with c2:
    st.metric(
        "High Risk Patients",
        high_risk
    )

with c3:
    st.metric(
        "Healthy Patients",
        total_patients - high_risk
    )

st.markdown("---")


# ADD PATIENT

st.subheader("Add New Patient")
col1, col2 = st.columns(2)
with col1:

    full_name = st.text_input(
        "Full Name"
    )

    dob = st.date_input(
    "Date of Birth",
    value=None,
    min_value=date(1950, 1, 1),
    max_value=date.today(),
    format="DD/MM/YYYY"
)
    email = st.text_input(
        "Email Address"
    )

with col2:

    glucose = st.number_input(
    "Glucose",
    min_value=0.0,
    value=0.0
  )
    haemoglobin = st.number_input(
    "Haemoglobin",
    min_value=0.0,
    value=0.0
 )
    cholesterol = st.number_input(
    "Cholesterol",
    min_value=0.0,
    value=0.0
 )
    

st.info("""
 ** Normal Blood Test Ranges **
 - Glucose(blood sugar): Between 70 - 140 mg/dL
 - Haemoglobin (Blood Iron) : Between 12.0 and 17.5 g/dL
 - Cholesterol: Between 120 and 200 mg/dL""")

    

if st.button("Generate Prediction & Save"):

    if full_name.strip() == "":
     st.error("Name cannot be empty")

    elif len(full_name.strip()) < 2:
     st.error("Name must contain at least 2 characters")

    elif not re.match(r"^[A-Za-z ]+$",full_name):
     st.error("Name should contain only alphabets")

    elif email.strip() == "":
     st.error("Email Address cannot be empty")

    elif dob is None:
     st.error("Date of Birth cannot be empty")

    elif not re.match( r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",email):
      st.error("Invalid Email Address")

    else:
        
        from crud import check_email_exists
        
        if check_email_exists(email.strip()):
            st.error(f"Duplicate Entry: A patient record with the email '{email.strip()}' already exists!")
        else:
            with st.spinner("Generating AI Prediction..."):
                remarks = generate_prediction(
                    glucose,
                    haemoglobin,
                    cholesterol
                )

            create_patient(
                (
                    full_name.strip(),
                    dob.strftime("%d/%m/%Y"),
                    email.strip(),
                    glucose,
                    haemoglobin,
                    cholesterol,
                    remarks
                )
            )

            st.success("Patient Saved Successfully")
            st.markdown("### AI Health Analysis")
            st.warning(remarks) 
st.markdown("---")

# PATIENT RECORDS

st.subheader(" Patient Records")
patients = get_patients()
if patients:

    df = pd.DataFrame(
        patients,
        columns=[
            "ID",
            "Full Name",
            "DOB",
            "Email",
            "Glucose",
            "Haemoglobin",
            "Cholesterol",
            "Remarks"
        ]
    )

    search = st.text_input(
        "🔍 Search Patient by Name"
    )

    if search:

        df = df[
            df["Full Name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        df,
        width="stretch"
    )
    csv = df.to_csv(
        index=False
    )
    st.download_button(
        "Download CSV",
        csv,
        "patients.csv",
        "text/csv"
    )

st.markdown("---")

# UPDATE PATIENT

st.subheader("Update Patient")

update_id = st.number_input(
    "Enter Patient ID To Update",
    min_value=1,
    step=1,
    key="update_id"
)

if st.button("Load Patient"):

    patient = get_patient_by_id(update_id)

    if patient:
        st.session_state.patient = patient

    else:
        st.error(f"Patient ID {update_id} not found" )

if "patient" in st.session_state:
    patient = st.session_state.patient
    updated_name = st.text_input(
        "Update Full Name",
        value=patient[1]
    )
    updated_email = st.text_input(
        "Update Email",
        value=patient[3]
    )
    updated_dob = st.date_input(
      "Update Date of Birth",
       value=datetime.strptime(patient[2],"%d/%m/%Y").date(),
       format="DD/MM/YYYY"
    )
    updated_glucose = st.number_input(
        "Update Glucose",
        value=float(patient[4]),
        key="ug"
    )
    updated_haemoglobin = st.number_input(
        "Update Haemoglobin",
        value=float(patient[5]),
        key="uh"
    )
    updated_cholesterol = st.number_input(
        "Update Cholesterol",
        value=float(patient[6]),
        key="uc"
    )

    if st.button("Update Patient Record"):
     if updated_name.strip() == "":
      st.error("Full Name cannot be empty")

     elif len(updated_name.strip()) < 2:
      st.error("Full Name must contain at least 2 characters")

     elif not re.match(r"^[A-Za-z ]+$",updated_name):
      st.error("Full Name should contain only alphabets")

     elif updated_email.strip() == "":
      st.error("Email Address cannot be empty")

     elif not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",updated_email):
      st.error("Invalid Email Address")

     else:
        remarks = generate_prediction(
            updated_glucose,
            updated_haemoglobin,
            updated_cholesterol
        )
        update_patient(
            update_id,
            updated_name,
            updated_dob.strftime("%d/%m/%Y"),
            updated_email,
            updated_glucose,
            updated_haemoglobin,
            updated_cholesterol,
            remarks
        )
        st.success("Patient Updated Successfully")
        st.markdown("### Updated AI Analysis")
        st.warning(remarks)
        del st.session_state["patient"]
        st.rerun()
st.markdown("---")


# READ PATIENT

st.subheader("Read Patient Details")
read_id = st.number_input(
    "Enter Patient ID To View",
    min_value=1,
    step=1,
    key="read_id"
)

if st.button("View Patient"):

    patient = get_patient_by_id(read_id)

    if patient:
        st.session_state["view_patient"] = patient

    else:
        st.error(f"Patient ID {read_id} not found")

if "view_patient" in st.session_state:

    patient = st.session_state["view_patient"]
    st.success("Patient Found")
    st.write("### Patient Information")

    st.write(f"**ID:** {patient[0]}")
    st.write(f"**Full Name:** {patient[1]}")
    st.write(f"**Date of Birth:** {patient[2]}")
    st.write(f"**Email:** {patient[3]}")
    st.write(f"**Glucose:** {patient[4]}")
    st.write(f"**Haemoglobin:** {patient[5]}")
    st.write(f"**Cholesterol:** {patient[6]}")
    st.write(f"**Remarks:** {patient[7]}")

    if st.button(
        "OK",
        key="ok_read_patient"
    ):
        del st.session_state["view_patient"]
        st.rerun()
st.markdown("---")

# DELETE PATIENT

st.subheader(" Delete Patient")
patient_id = st.number_input(
    "Enter Patient ID To Delete",
    min_value=1,
    step=1,
    key="delete_id"
)

if st.button("Delete Patient"):

    result = delete_patient(patient_id)

    if result > 0:
     st.success(f"Patient ID {patient_id} Deleted Successfully")

    else:
        st.error(f"Patient ID {patient_id} not found")
