
# AI-Powered Placement Preparation & Job Matching Portal

## 1. Project Overview

The AI-Powered Placement Preparation & Job Matching Portal is a
web application built with Python and Streamlit. It helps students
prepare for placements, review their technical skills, find
relevant jobs, practise mock tests, track performance, and manage
job application records.

## 2. Main Features

- Student registration and login
- Student profile management
- Resume upload and skill extraction
- Job matching based on student skills
- Skill gap analysis and learning suggestions
- Placement preparation and mock tests
- Test result storage and progress dashboard
- Job application tracking and status updates
- Role-protected administrator dashboard

## 3. Technology Stack

- Python
- Streamlit
- MySQL
- Pandas
- Scikit-learn
- PyMuPDF
- bcrypt
- mysql-connector-python

## 4. Project Structure

app.py                 Main Streamlit application
modules/               Application modules
data/jobs.csv          Job dataset
requirements.txt       Python dependencies
README.md              Project documentation

## 5. Prerequisites

- Python installed
- MySQL Server and MySQL Workbench
- A MySQL database configured for the application

## 6. Installation

1. Clone or download the project.
2. Open a terminal in the project folder.
3. Create a virtual environment:

   python -m venv venv

4. Activate the environment on Windows:

   .\venv\Scripts\Activate.ps1

5. Install dependencies:

   python -m pip install -r requirements.txt

## 7. Database Setup

1. Create the MySQL database named placement_portal.
2. Create the required tables using the SQL setup scripts.
3. Configure the database connection using the application's
   supported configuration method.
4. Create or register a student account.
5. Assign administrator access only through a trusted,
   authorized process.

Never commit database passwords or private credentials to GitHub.

## 8. Run the Application

Run the following command from the project root:

python -m streamlit run app.py

Open the local URL displayed in the terminal.

## 9. Testing

Verify registration, login, profile management, resume analysis,
job matching, mock tests, progress tracking, application tracking,
and administrator permissions.

## 10. Limitations

Job application statuses are maintained by users or authorized
administrators. The portal does not automatically submit job
applications to external company websites unless such an
integration is separately implemented.

## 11. Future Improvements

- Larger and regularly updated job dataset
- More mock-test questions
- Enhanced analytics and reports
- Job database management
- Additional security and automated tests
