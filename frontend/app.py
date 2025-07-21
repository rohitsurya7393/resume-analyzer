import streamlit as st
import pdfplumber
import os
import json
from api import compare_resume_jd, ping

st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("📄 Real-Time Resume Analyzer & Job Tracker")

# API Status
with st.expander("🔌 API Status"):
    status = ping()
    st.json(status)

st.subheader("📝 Submit Your Resume & JD")

col1, col2 = st.columns(2)

# Resume Upload
with col1:
    company = st.text_input("Company Name")
    uploaded_file = st.file_uploader("Upload Resume (PDF only)", type="pdf")

    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            resume_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            st.session_state.resume_text = resume_text
            st.success("✅ Resume text extracted successfully!")

# JD Input
with col2:
    jd_text = st.text_area("Paste Job Description", height=300)
    if jd_text:
        st.session_state.jd_text = jd_text

# Analyze Button
if st.button("🔍 Analyze & Submit"):
    if not (company and uploaded_file and jd_text):
        st.warning("Please provide all inputs.")
    else:
        result = compare_resume_jd(st.session_state.resume_text, st.session_state.jd_text)
        st.session_state.result = result
        st.session_state.company = company
        st.success(f"🎯 Overall Match Score: {result['overall_match_percentage']}%")

# Display Results
if "result" in st.session_state:
    result = st.session_state.result

    st.markdown("## ✅ Matched Keywords by Category")
    for category, keywords in result["matched_keywords_by_category"].items():
        if keywords:
            with st.expander(f"🟢 {category.title()} ({len(keywords)})"):
                st.write(", ".join(keywords))
        else:
            st.write(f"🟢 {category.title()}: No matches")

    st.markdown("## ❌ Missing Keywords by Category")
    for category, keywords in result["missing_keywords_by_category"].items():
        if keywords:
            with st.expander(f"🔴 {category.title()} ({len(keywords)})"):
                st.write(", ".join(keywords))
        else:
            st.write(f"✅ {category.title()}: All covered")

    st.markdown("## 🧠 Unrecognized JD Keywords (Human-in-the-Loop)")

    # Set up categories
    categories = ["ignore", "tools", "languages", "platforms", "concepts", "soft_skills", "techniques"]

    # Load skills.json
    skills_path = os.path.join(os.path.dirname(__file__), "..", "backend", "skills.json")
    try:
        with open(skills_path, "r") as f:
            skills = json.load(f)
    except FileNotFoundError:
        skills = {c: [] for c in categories}
        with open(skills_path, "w") as f:
            json.dump(skills, f, indent=2)

    ignored = set(skills.get("ignore", []))
    unrecognized_keywords = [kw for kw in result["unrecognized_jd_terms"] if kw not in ignored]

    if "selected_categories" not in st.session_state:
        st.session_state.selected_categories = {}

    if not unrecognized_keywords:
        st.info("✅ No uncategorized JD keywords found.")
    else:
        for keyword in unrecognized_keywords:
            default = st.session_state.selected_categories.get(keyword, "ignore")
            selected_cat = st.selectbox(
                f"🔹 Select category for: **`{keyword}`**",
                options=categories,
                index=categories.index(default),
                key=f"select_{keyword}"
            )
            st.session_state.selected_categories[keyword] = selected_cat

        # Save button
        if st.button("💾 Add to skills.json"):
            try:
                for keyword, category in st.session_state.selected_categories.items():
                    skills.setdefault(category, [])
                    if keyword not in skills[category]:
                        skills[category].append(keyword)
                with open(skills_path, "w") as f:
                    json.dump(skills, f, indent=2)
                st.success("✅ skills.json updated successfully!")
            except Exception as e:
                st.error(f"❌ Error updating skills.json: {e}")

    # Category Match Progress
    st.markdown("## 📊 Match % by Category")
    for category, percent in result["match_percentage_by_category"].items():
        st.progress(percent / 100)
        st.write(f"**{category.title()}**: {percent}%")
