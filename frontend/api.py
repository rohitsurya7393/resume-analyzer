import requests

API_BASE = "http://localhost:8001"

def ping():
    return requests.get(f"{API_BASE}/ping").json()

def compare_resume_jd(resume, jd):
    payload = {"resume_text": resume, "jd_text": jd}
    response = requests.post(f"{API_BASE}/compare_keywords", json=payload)
    return response.json()

def submit_application(company, resume, jd):
    payload = {"company_name": company, "resume_text": resume, "jd_text": jd}
    return requests.post(f"{API_BASE}/submit_application", json=payload).json()
