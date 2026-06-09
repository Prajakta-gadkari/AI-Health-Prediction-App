AI Health Prediction Application

About the Project/ Overview  : This project is a web application developed using Python, Streamlit, SQLite, and Google Gemini AI.The application allows users to store patient information, manage patient records, and generate health-related observations based on blood test values such as glucose, haemoglobin, and cholesterol.

## Features

* Add patient records
* View patient records
* Update patient details
* Delete patient records
* Search patients by name
* Download records as CSV
* Generate AI-based health analysis
* Store data using SQLite database

## Technologies Used

* Python
* Streamlit
* SQLite
* Pandas
* Google Gemini API

## Validation

1 Full Name

* Cannot be empty
* Minimum 2 characters
* Numbers are not allowed

2 Email Address

* Cannot be empty
* Must be in a valid email format

3 Date of Birth

* Required field
* Allowed between 01/01/1950 and the current date

4 Health Parameters

# Glucose = Normal Range: 70–140 mg/dL

# Haemoglobin = Male: 13.5–17.5 g/dL, Female: 12.0–15.5 g/dL

# Cholesterol = Below 200 mg/dL


## Setup

1. Create a virtual environment

   python -m venv venv

2. Activate the environment

   venv\Scripts\activate

3. Install required packages

   pip install -r requirements.txt

4. Create a .env file and add:

   GEMINI_API_KEY=your_api_key

5. Run the database file

   python database.py

6. Start the application

   streamlit run app.py

## Notes = The .env file, database file, and virtual environment folder should not be uploaded to GitHub.


Prajakta Gadkari
