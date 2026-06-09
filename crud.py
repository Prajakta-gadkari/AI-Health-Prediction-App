import sqlite3

DB = "database.db"


def create_patient(data):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO patients(
        full_name,dob,email,glucose,haemoglobin,cholesterol,remarks) VALUES (?,?,?,?,?,?,?)""", data)

    conn.commit()
    conn.close()


def get_patients():

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM patients"
)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_patient_by_id(patient_id):

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM patients WHERE id=?",
        (patient_id,)
    )
    patient = cursor.fetchone()
    conn.close()
    return patient

def update_patient(
        patient_id,
        full_name,
        dob,
        email,
        glucose,
        haemoglobin,
        cholesterol,
        remarks):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE patients
    SET
        full_name=?,
        dob=?,
        email=?,
        glucose=?,
        haemoglobin=?,
        cholesterol=?,
        remarks=?
    WHERE id=?
    """,
                   (
                       full_name,
                       dob,
                       email,
                       glucose,
                       haemoglobin,
                       cholesterol,
                       remarks,
                       patient_id
                   ))

    conn.commit()
    conn.close()


def delete_patient(patient_id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (patient_id,)
    )
    conn.commit()
    rows_deleted = cursor.rowcount
    conn.close()
    return rows_deleted


def check_email_exists(email):
    """
    Scans the database table to verify if an email registration already exists.
    Returns True if found, False otherwise.
    """
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT 1 FROM patients WHERE LOWER(email) = LOWER(?)", 
        (email.strip(),)
    )
    result = cursor.fetchone()
    
    conn.close()
    return result is not None