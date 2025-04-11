import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.title("Resume Search & Interview Invitation")

# Store search results in session state
if "search_results" not in st.session_state:
    st.session_state["search_results"] = []

# 1) Search by Job Description
st.header("Search Resumes by Job Description")
job_description = st.text_area("Enter job description here", height=150)

if st.button("Search Resumes"):
    try:
        # --- Step A: Search Resumes ---
        search_response = requests.post(
            f"{API_BASE_URL}/search-resumes",
            json={"jd": job_description}
        )
        search_response.raise_for_status()
        data = search_response.json()
        
        results = data.get("results", [])
        
        # --- Step B: For each result, fetch the full resume by SQL ID ---
        #     so that we can display the person's name, etc.
        for result in results:
            sql_id = result.get("sql_id")
            if sql_id is not None:
                resume_detail_response = requests.get(f"{API_BASE_URL}/resume/{sql_id}")
                if resume_detail_response.status_code == 200:
                    full_resume = resume_detail_response.json().get("resume", {})
                    # Attach the full resume to the search result
                    result["full_resume"] = full_resume
                else:
                    result["full_resume"] = None
            else:
                result["full_resume"] = None
        
        # Store in session state
        st.session_state["search_results"] = results
        st.success("Search complete!")
    except Exception as e:
        st.error(f"Error searching resumes: {e}")

# 2) Display results with an invite button
results = st.session_state.get("search_results", [])
if results:
    st.header("Search Results")
    for index, item in enumerate(results):
        score = item.get("score")
        full_resume = item.get("full_resume", {})
        
        # If we got the full resume details, use the name
        candidate_name = full_resume.get("name", "Unknown Name")
        candidate_email = full_resume.get("email", "unknown@example.com")

        with st.expander(f"{candidate_name} (Score: {score})"):
            st.write("**SQL ID**:", item.get("sql_id"))
            st.write("**Resume ID**:", item.get("resume_id"))
            # You can show other fields from full_resume as needed
            st.write("**Phone**:", full_resume.get("phone", ""))

            # Collect user inputs for date/time
            invite_date = st.text_input("Interview Date", "2025-04-15", key=f"date_{index}")
            invite_time = st.text_input("Interview Time", "10:00 AM", key=f"time_{index}")

            # Button to send interview invite
            if st.button("Send Invite", key=f"invite_btn_{index}"):
                try:
                    payload = {
                        "email": candidate_email,
                        "interview_date": invite_date,
                        "interview_time": invite_time
                    }
                    invite_response = requests.post(
                        f"{API_BASE_URL}/send-interview-invite",
                        json=payload
                    )
                    invite_response.raise_for_status()
                    msg = invite_response.json().get("message", "Interview invitation sent successfully!")
                    st.success(msg)
                except Exception as e:
                    st.error(f"Error sending invite: {e}")
