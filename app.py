
from modules.skill_extractor import extract_skills
from modules.job_matcher import match_jobs
from modules.skill_gap import analyze_skill_gap, get_learning_plan
from modules.job_matcher import load_jobs
from modules.auth import register_user, login_user
from modules.profile import save_profile, load_profile
from modules.progress import save_test_attempt, get_test_history
from modules.mock_test import QUESTION_BANK, evaluate_answers
from modules.applications import (
    add_application,
    get_applications,
    update_application_status,
    delete_application,
    ALLOWED_STATUSES
)
from modules.admin import (
    get_admin_statistics,
    get_all_students,
    get_all_applications,
    admin_update_application_status
)
import streamlit as st

st.set_page_config(
    page_title="AI Placement Portal",
    page_icon="🎓",
    layout="wide"
)

if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["user"] is None:
    st.title("🎓 AI Placement Portal")

    auth_mode = st.radio(
        "Choose an option",
        ["Login", "Register"],
        horizontal=True
    )

    if auth_mode == "Register":
        st.subheader("Create Student Account")

        with st.form("register_form"):
            full_name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input(
                "Password (minimum 8 characters)",
                type="password"
            )

            submitted = st.form_submit_button("Register")

        if submitted:
            try:
                success, message = register_user(
                    full_name, email, password
                )

                if success:
                    st.success(message)
                    st.info("Please select Login to continue.")
                else:
                    st.error(message)

            except Exception:
                st.error(
                    "Registration failed. Check the database "
                    "connection and try again."
                )

    else:
        st.subheader("Student Login")

        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input(
                "Password",
                type="password"
            )

            submitted = st.form_submit_button("Login")

        if submitted:
            try:
                user = login_user(email, password)

                if user:
                    st.session_state["user"] = user
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

            except Exception:
                st.error(
                    "Login failed. Check the database "
                    "connection and try again."
                )

    st.stop()


st.title("🎓 AI Placement Preparation & Job Matching Portal")

st.write(
    "Find suitable jobs, analyze your resume, "
    "identify missing skills and prepare for placements."
)


user = st.session_state["user"]


st.sidebar.title("🎓 Placement Portal")
st.sidebar.write(f"Welcome, {user['full_name']}!")

page = st.sidebar.radio(
    "Navigation", 
    [
        "Home",
        "Student Profile",
        "Resume Analyzer",
        "Placement Preparation",
        "Job Matching",
        "Progress Dashboard",
        "Mock Test",
        "Job Application Tracking",
        "Admin Panel"
    ]
)

if st.sidebar.button("Logout"):
    st.session_state["user"] = None
    st.session_state.pop("student_skills", None)
    st.rerun()


if page == "Home":
    st.header("Welcome to Your Placement Assistant")

    st.write(
        "This platform helps students prepare for "
        "internships and placement opportunities."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Available Modules", "4")
    col2.metric("Job Recommendations", "Coming Soon")
    col3.metric("Resume Analysis", "Coming Soon")

    st.info(
        "Start by creating your student profile "
        "and uploading your resume."
    )

elif page == "Student Profile":
    st.header("👩‍🎓 Student Profile")

    user = st.session_state["user"]
    profile = load_profile(user["user_id"]) or {}

    with st.form("student_profile_form"):
        branch_options = [
            "Computer Engineering",
            "Information Technology",
            "Electronics",
            "Other"
        ]

        saved_branch = profile.get("branch") or "Computer Engineering"
        branch_index = (
            branch_options.index(saved_branch)
            if saved_branch in branch_options else 0
        )

        branch = st.selectbox(
            "Branch",
            branch_options,
            index=branch_index
        )

        saved_year = profile.get("graduation_year") or 2027
        graduation_year = st.selectbox(
            "Graduation Year",
            [2027, 2028, 2029],
            index=[2027, 2028, 2029].index(
                saved_year if saved_year in [2027, 2028, 2029]
                else 2027
            )
        )

        saved_cgpa = profile.get("cgpa")
        cgpa = st.number_input(
            "CGPA",
            min_value=0.0,
            max_value=10.0,
            value=float(saved_cgpa or 0.0),
            step=0.1
        )

        skills = st.text_input(
            "Technical Skills",
            value=profile.get("technical_skills") or "",
            placeholder="Python, Java, SQL"
        )

        roles = [
            "Software Developer",
            "Data Analyst",
            "Machine Learning Engineer",
            "Web Developer"
        ]

        saved_role = profile.get("preferred_role") or roles[0]
        role_index = roles.index(saved_role) if saved_role in roles else 0

        preferred_role = st.selectbox(
            "Preferred Job Role",
            roles,
            index=role_index
        )

        save_button = st.form_submit_button("Save Profile")

    if save_button:
        try:
            save_profile(
                user["user_id"],
                branch,
                graduation_year,
                cgpa,
                skills,
                preferred_role
            )

            st.session_state["student_skills"] = [
                skill.strip().lower()
                for skill in skills.split(",")
                if skill.strip()
            ]

            st.success("Your profile has been saved!")
        except Exception:
            st.error(
                "Profile could not be saved. "
                "Please check your database connection."
            )       
    if st.button("Preview Profile"):
        st.subheader("Profile Preview")
        st.write("Name:", user.get("full_name", "Not available"))
        st.write("Branch:", branch)
        st.write("Graduation Year:", graduation_year)
        st.write("CGPA:", cgpa)
        st.write("Skills:", skills)
        st.write("Preferred Role:", preferred_role)
   
elif page == "Resume Analyzer":
    st.header("📄 Resume Analyzer")
    st.write("Upload your resume in PDF format.")

    uploaded_file = st.file_uploader(
        "Choose your resume",
        type=["pdf"],
        key="resume_upload"
    )

    if uploaded_file is not None:
        import pymupdf

        document = pymupdf.open(
            stream=uploaded_file.getvalue(),
            filetype="pdf"
        )

        resume_text = "\n".join(
            page.get_text() for page in document
        )

        document.close()

        if resume_text.strip():
            st.success("Resume text extracted successfully!")

            st.text_area(
                "Extracted Resume Text",
                resume_text,
                height=250
            )

            skills = extract_skills(resume_text)
            st.session_state["student_skills"] = skills

            st.subheader("🧠 Skills Detected")

            if skills:
                st.success(
                    f"Found {len(skills)} technical skills."
                )

                for skill in skills:
                    st.write(f"✅ {skill.title()}")
            else:
                st.warning(
                    "No listed skills detected. "
                    "Try a resume containing technical skills."
                )

        else:
            st.warning(
                "No readable text found. "
                "Try a text-based PDF resume."
            )
elif page == "Job Matching":
    st.header("💼 Job Matching & Skill Gap Analysis")

    detected_skills = st.session_state.get(
        "student_skills", []
    )

    default_skills = ", ".join(detected_skills)

    skills_input = st.text_input(
        "Your technical skills",
        value=default_skills,
        placeholder="Python, SQL, Git"
    )

    if st.button("Find Matching Jobs"):
        student_skills = [
            skill.strip().lower()
            for skill in skills_input.split(",")
            if skill.strip()
        ]

        if not student_skills:
            st.warning(
                "Upload a resume or enter your skills first."
            )
        else:
            try:
                results = match_jobs(student_skills)

                st.subheader("🎯 Recommended Jobs")
                st.dataframe(
                    results,
                    use_container_width=True,
                    hide_index=True
                )

                jobs_df = load_jobs()

                job_roles = jobs_df["job_title"].tolist()

                selected_job = st.selectbox(
                    "Choose a job to analyze skill gaps",
                    job_roles
                )

                selected_row = jobs_df[
                    jobs_df["job_title"] == selected_job
                ].iloc[0]

                required_skills = [
                    skill.strip().lower()
                    for skill in str(
                        selected_row["required_skills"]
                    ).split("|")
                    if skill.strip()
                ]

                gap = analyze_skill_gap(
                    student_skills,
                    required_skills
                )

                st.divider()
                st.subheader("📊 Skill Gap Analysis")

                col1, col2 = st.columns(2)

                col1.metric(
                    "Skill Coverage",
                    f"{gap['skill_coverage']}%"
                )

                col2.metric(
                    "Missing Skills",
                    len(gap["missing_skills"])
                )

                st.write("✅ Matched Skills")

                if gap["matched_skills"]:
                    st.write(
                        ", ".join(gap["matched_skills"])
                    )
                else:
                    st.write("No required skills matched yet.")

                st.write("❌ Missing Skills")

                if gap["missing_skills"]:
                    st.write(
                        ", ".join(gap["missing_skills"])
                    )

                    st.subheader(
                        "📚 Personalized Learning Plan"
                    )

                    learning_plan = get_learning_plan(
                        gap["missing_skills"]
                    )

                    for skill, topics in learning_plan.items():
                        with st.expander(
                            f"Learn {skill.title()}"
                        ):
                            for topic in topics:
                                st.write(f"• {topic}")
                else:
                    st.success(
                        "All listed required skills are matched!"
                    )

                st.caption(
                    "Skill coverage measures required-skill "
                    "overlap, not job selection probability."
                )

            except Exception as error:
                st.error(
                    f"Could not analyze jobs: {error}"
                )

elif page == "Placement Preparation":
    st.header("📚 Placement Preparation")

    subject = st.selectbox(
        "Choose a preparation subject",
        ["DSA", "DBMS", "Operating Systems",
         "Computer Networks", "OOP", "Aptitude"]
    )

    topics = {
        "DSA": ["Arrays", "Strings", "Linked Lists",
                "Stacks and Queues", "Trees", "Graphs"],
        "DBMS": ["SQL", "Normalization", "Transactions",
                 "Joins", "Indexing"],
        "Operating Systems": ["Processes", "Threads",
                              "Deadlocks", "Scheduling"],
        "Computer Networks": ["OSI Model", "TCP/IP",
                              "DNS", "HTTP", "Routing"],
        "OOP": ["Classes", "Objects", "Inheritance",
                "Polymorphism", "Encapsulation"],
        "Aptitude": ["Percentages", "Ratio",
                     "Time and Work", "Speed and Distance"]
    }

    st.subheader(f"Topics for {subject}")

    for topic in topics[subject]:
        st.write(f"• {topic}")

    st.caption(
        "These are starter topics. Practice tests "
        "and progress tracking will be added later."
    )
    
elif page == "Progress Dashboard":
    st.title("Student Progress Dashboard")
    st.write("Track your mock test performance.")

    user = st.session_state.get("user")

    if not user:
        st.warning("Please log in to view your progress.")
        st.stop()

    try:
        history = get_test_history(user["user_id"])

    except Exception as error:
        st.error(f"Could not load test history: {error}")
        st.stop()

    if not history:
        st.info(
            "No test attempts found yet. "
            "Complete a Mock Test to see your progress here."
        )

    else:
        import pandas as pd

        df = pd.DataFrame(history)

        df["score_percent"] = pd.to_numeric(
            df["score_percent"],
            errors="coerce"
        )

        df["attempted_at"] = pd.to_datetime(
            df["attempted_at"],
            errors="coerce"
        )

        df = df.dropna(subset=["score_percent"])

        if df.empty:
            st.info("No valid score records are available.")

        else:
            total_tests = len(df)
            average_score = df["score_percent"].mean()
            best_score = df["score_percent"].max()

            latest_score = df.iloc[0]["score_percent"]

            st.subheader("Performance Summary")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Tests Taken", total_tests)
            col2.metric("Average Score", f"{average_score:.2f}%")
            col3.metric("Best Score", f"{best_score:.2f}%")
            col4.metric("Latest Score", f"{latest_score:.2f}%")

            st.divider()
            st.subheader("Subject-wise Average Score")

            subject_scores = (
                df.groupby("subject")["score_percent"]
                .mean()
                .sort_values(ascending=False)
            )

            st.bar_chart(subject_scores)

            st.divider()
            st.subheader("Test Performance Over Time")

            chart_df = (
                df.dropna(subset=["attempted_at"])
                .sort_values("attempted_at")
                .set_index("attempted_at")
            )

            if not chart_df.empty:
                st.line_chart(chart_df["score_percent"])
            else:
                st.info("Test dates are unavailable for the trend chart.")

            st.divider()
            st.subheader("Test Attempt History")

            display_df = df[
                [
                    "attempt_id",
                    "subject",
                    "total_questions",
                    "correct_answers",
                    "score_percent",
                    "attempted_at"
                ]
            ].copy()

            display_df = display_df.rename(
                columns={
                    "attempt_id": "Attempt ID",
                    "subject": "Subject",
                    "total_questions": "Total Questions",
                    "correct_answers": "Correct Answers",
                    "score_percent": "Score (%)",
                    "attempted_at": "Attempted At"
                }
            )

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            st.divider()
            st.subheader("Recommended Focus Area")

            weakest_subject = subject_scores.idxmin()
            weakest_score = subject_scores.min()

            st.info(
                f"Your lowest average score is in {weakest_subject} "
                f"({weakest_score:.2f}%). "
                "Practise this subject next."
            )
            
            
elif page == "Job Application Tracking":
    st.title("Job Application Tracking")
    st.write(
        "Save jobs you have applied to and track their status."
    )

    user = st.session_state.get("user")

    if not user:
        st.warning("Please log in to track your applications.")
        st.stop()

    user_id = user["user_id"]

    st.subheader("Add a Job Application")

    try:
        jobs_df = load_jobs()
    except Exception as error:
        st.error(f"Could not load jobs: {error}")
        st.stop()

    required_columns = {
        "company",
        "job_title",
        "location"
    }

    if jobs_df is None or jobs_df.empty:
        st.warning("No jobs are currently available.")
    elif not required_columns.issubset(jobs_df.columns):
        st.error(
            "The jobs data must contain company, job_title "
            "and location columns."
        )
    else:
        jobs_df = jobs_df.fillna("")

        job_indices = list(range(len(jobs_df)))

        def format_job(index):
            row = jobs_df.iloc[index]
            return (
                f"{row['job_title']} | "
                f"{row['company']} | "
                f"{row['location']}"
            )

        with st.form("add_job_application_form"):
            selected_index = st.selectbox(
                "Choose a job",
                options=job_indices,
                format_func=format_job
            )

            notes = st.text_area(
                "Notes (optional)",
                placeholder="For example: Applied through company website."
            )

            add_clicked = st.form_submit_button(
                "Add to My Applications"
            )

        if add_clicked:
            selected_job = jobs_df.iloc[selected_index]

            try:
                application_id = add_application(
                    user_id=user_id,
                    company=str(selected_job["company"]),
                    job_title=str(selected_job["job_title"]),
                    location=str(selected_job["location"]),
                    notes=notes.strip()
                )

                st.success(
                    f"Application saved successfully! "
                    f"Application ID: {application_id}"
                )

            except Exception as error:
                st.error(f"Could not save application: {error}")

    st.divider()
    st.subheader("My Applications")

    try:
        applications = get_applications(user_id)
    except Exception as error:
        st.error(f"Could not load applications: {error}")
        st.stop()

    if not applications:
        st.info(
            "You have not added any applications yet. "
            "Choose a job above to get started."
        )

    else:
        import pandas as pd

        applications_df = pd.DataFrame(applications)

        total_apps = len(applications_df)
        active_apps = len(
            applications_df[
                applications_df["status"].isin(
                    ["Applied", "Shortlisted", "Interview"]
                )
            ]
        )
        selected_apps = int(
            (applications_df["status"] == "Selected").sum()
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Applications", total_apps)
        col2.metric("In Progress", active_apps)
        col3.metric("Selected", selected_apps)

        st.dataframe(
            applications_df[
                [
                    "application_id",
                    "company",
                    "job_title",
                    "location",
                    "status",
                    "applied_at",
                    "notes"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.divider()
        st.subheader("Update Application Status")

        application_options = {
            (
                f"#{app['application_id']} - "
                f"{app['job_title']} at {app['company']}"
            ): app["application_id"]
            for app in applications
        }

        with st.form("update_application_status_form"):
            selected_label = st.selectbox(
                "Select an application",
                list(application_options.keys()),
                key="status_application_choice"
            )

            new_status = st.selectbox(
                "New status",
                ALLOWED_STATUSES,
                key="new_application_status"
            )

            update_clicked = st.form_submit_button(
                "Update Status"
            )

        if update_clicked:
            application_id = application_options[selected_label]

            try:
                updated_rows = update_application_status(
                    user_id=user_id,
                    application_id=application_id,
                    new_status=new_status
                )

                if updated_rows > 0:
                    st.success("Application status updated successfully.")
                    st.rerun()
                else:
                    st.warning(
                        "No record was updated. Refresh and try again."
                    )

            except Exception as error:
                st.error(f"Could not update status: {error}")

        st.divider()
        st.subheader("Delete an Application")

        delete_options = {
            (
                f"#{app['application_id']} - "
                f"{app['job_title']} at {app['company']}"
            ): app["application_id"]
            for app in applications
        }

        with st.form("delete_application_form"):
            delete_label = st.selectbox(
                "Select an application to delete",
                list(delete_options.keys()),
                key="delete_application_choice"
            )

            confirm_delete = st.checkbox(
                "I confirm that I want to delete this application."
            )

            delete_clicked = st.form_submit_button(
                "Delete Application"
            )

        if delete_clicked:
            if not confirm_delete:
                st.warning("Please confirm before deleting.")
            else:
                application_id = delete_options[delete_label]

                try:
                    deleted_rows = delete_application(
                        user_id=user_id,
                        application_id=application_id
                    )

                    if deleted_rows > 0:
                        st.success("Application deleted successfully.")
                        st.rerun()
                    else:
                        st.warning(
                            "No record was deleted. Refresh and try again."
                        )

                except Exception as error:
                    st.error(
                        f"Could not delete application: {error}"
                    )  
                    
                    
elif page == "Admin Panel":
    user = st.session_state.get("user")

    if not user or user.get("role") != "admin":
        st.error("Admin access required.")
        st.stop()

    st.title("Admin Dashboard")
    st.write("Manage student and placement activity.")

    try:
        stats = get_admin_statistics(user["user_id"])
    except Exception as error:
        st.error(f"Could not load admin statistics: {error}")
        st.stop()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Registered Students",
        stats["total_students"]
    )
    col2.metric(
        "Test Attempts",
        stats["total_attempts"]
    )
    col3.metric(
        "Applications",
        stats["total_applications"]
    )

    st.divider()
    st.subheader("Application Status Summary")

    if stats["application_statuses"]:
        import pandas as pd

        status_df = pd.DataFrame(stats["application_statuses"])
        status_df = status_df.set_index("status")

        st.bar_chart(status_df["total"])
    else:
        st.info("No applications have been recorded yet.")

    st.divider()
    st.subheader("Registered Students")

    try:
        students = get_all_students(user["user_id"])

        if students:
            st.dataframe(
                students,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No student accounts found.")

    except Exception as error:
        st.error(f"Could not load students: {error}")

    st.divider()
    st.subheader("All Job Applications")

    try:
        applications = get_all_applications(user["user_id"])

        if not applications:
            st.info("No job applications found.")

        else:
            st.dataframe(
                applications,
                use_container_width=True,
                hide_index=True
            )

            application_options = {
                (
                    f"#{app['application_id']} - "
                    f"{app['job_title']} at {app['company']} "
                    f"(Student ID: {app['user_id']})"
                ): app["application_id"]
                for app in applications
            }

            with st.form("admin_application_status_form"):
                selected_label = st.selectbox(
                    "Select application",
                    list(application_options.keys())
                )

                new_status = st.selectbox(
                    "Set new status",
                    [
                        "Applied",
                        "Shortlisted",
                        "Interview",
                        "Selected",
                        "Rejected"
                    ]
                )

                update_clicked = st.form_submit_button(
                    "Update Application Status"
                )

            if update_clicked:
                application_id = application_options[selected_label]

                try:
                    updated_rows = admin_update_application_status(
                        user["user_id"],
                        application_id,
                        new_status
                    )

                    if updated_rows > 0:
                        st.success("Application status updated.")
                        st.rerun()
                    else:
                        st.warning(
                            "No status change was made. "
                            "Check the selected application."
                        )

                except Exception as error:
                    st.error(f"Could not update status: {error}")

    except Exception as error:
        st.error(f"Could not load applications: {error}")
         
elif page == "Mock Test":
    st.title("Placement Preparation - Mock Test")
    st.write("Choose a subject and test your placement preparation.")

    subject = st.selectbox(
        "Select Subject",
        list(QUESTION_BANK.keys()),
        key="mock_test_subject"
    )

    questions = QUESTION_BANK[subject]

    st.subheader(f"{subject} Test")
    st.write(f"Total questions: {len(questions)}")

    with st.form(key="mock_test_form"):
        selected_answers = {}

        for index, question in enumerate(questions):
            st.markdown(
                f"**Q{index + 1}. {question['question']}**"
            )

            selected_answers[str(index)] = st.radio(
                "Choose your answer",
                ["Not answered"] + question["options"],
                index=0,
                key=f"mock_{subject}_{index}",
                label_visibility="collapsed"
            )

        submitted = st.form_submit_button("Submit Test")

    if submitted:
        clean_answers = {
            key: value
            for key, value in selected_answers.items()
            if value != "Not answered"
        }

        result = evaluate_answers(subject, clean_answers) 


        try:
            save_test_attempt(
                user_id=st.session_state["user"]["user_id"],
                subject=subject,
                total_questions=result["total_questions"],
                correct_answers=result["correct_answers"]
            )
            st.success("Test result saved successfully!")

        except Exception as error:
            st.error(f"Could not save test result: {error}")

    

        st.session_state["mock_test_result"] = {
            "subject": subject,
            **result
        }
        
    saved_result = st.session_state.get("mock_test_result")

    if saved_result and saved_result["subject"] == subject:
        st.divider()
        st.subheader("Your Test Result")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Score",
            f"{saved_result['score_percent']}%"
        )
        col2.metric(
            "Correct",
            saved_result["correct_answers"]
        )
        col3.metric(
            "Incorrect / Unanswered",
            saved_result["wrong_answers"]
        )

        if saved_result["score_percent"] >= 70:
            st.success("Good work! Keep practising.")
        else:
            st.info("Keep practising this subject to improve.")

        st.subheader("Answer Review")

        for index, item in enumerate(saved_result["results"], start=1):
            st.markdown(f"**Q{index}. {item['question']}**")
            st.write(f"Your answer: {item['selected']}")
            st.write(f"Correct answer: {item['correct']}")

            if item["is_correct"]:
                st.success("Correct")
            else:
                st.error("Incorrect")

            st.caption(item["explanation"])
            
            
            
            


