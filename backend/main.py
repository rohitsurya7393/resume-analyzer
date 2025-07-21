

from fastapi import FastAPI,UploadFile,File,HTTPException
from resume_parser import extract_text_from_pdf
from keyword_extractor import extract_entities_ner
from pydantic import BaseModel
from typing import List
from utils.load_skills import load_categorized_skills
from utils.compare_keywords import extract_keywords_by_category, extract_unrecognized_keywords



app = FastAPI()

@app.get("/ping")
def health_check():
    return {"status": "ok", "message": "API is running"}


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        contents = await file.read()
        with open("temp_resume.pdf", "wb") as f:
            f.write(contents)

        text = extract_text_from_pdf("temp_resume.pdf")

        return {"filename": file.filename, "text": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/upload_jd")
async def upload_jd(file: UploadFile = File(...)):
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        contents = await file.read()
        with open("temp_jd.pdf", "wb") as f:
            f.write(contents)

        text = extract_text_from_pdf("temp_jd.pdf")

        return {"filename": file.filename, "text": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
            
            
class TextInput(BaseModel):
    text: str


@app.post("/extract_keywords_ner")

def extract_keywords_using_ner(payload: TextInput):

    try:
        keywords = extract_entities_ner(payload.text)

        return {"status": "success", "keywords": keywords}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

class CompareInput(BaseModel):
    resume_text: str
    jd_text: str


from fastapi import FastAPI, Body
from utils.load_skills import load_categorized_skills
from utils.compare_keywords import extract_keywords_by_category

app = FastAPI()
skills_dict = load_categorized_skills()

@app.post("/compare_keywords")
def compare_keywords(resume_text: str = Body(...), jd_text: str = Body(...)):
    try:
        resume_matches, _ = extract_keywords_by_category(resume_text, skills_dict)
        jd_matches, _ = extract_keywords_by_category(jd_text, skills_dict)

        matched = {}
        missing = {}
        percentage = {}

        for category in skills_dict.keys():
            resume_set = set(resume_matches.get(category, []))
            jd_set = set(jd_matches.get(category, []))
            match = resume_set.intersection(jd_set)
            miss = jd_set.difference(resume_set)

            matched[category] = list(match)
            missing[category] = list(miss)
            percentage[category] = round(len(match) / len(jd_set) * 100, 2) if jd_set else 0.0

        unrecognized = extract_unrecognized_keywords(jd_text, skills_dict, matched)

        return {
            "status": "success",
            "matched_keywords_by_category": matched,
            "missing_keywords_by_category": missing,
            "match_percentage_by_category": percentage,
            "overall_match_percentage": round(
                sum(percentage.values()) / len(percentage) if percentage else 0, 2
            ),
            "unrecognized_jd_terms": unrecognized
        }

    except Exception as e:
        print("❌ ERROR in /compare_keywords:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

from database import init_db

init_db()

from database import insert_application

class ApplicationInput(BaseModel):
    company_name: str
    resume_text: str
    jd_text: str

@app.post("/submit_application")
def submit_application(payload: ApplicationInput):
    try:
        resume_keywords = set(extract_entities_ner(payload.resume_text))
        jd_keywords = set(extract_entities_ner(payload.jd_text))

        matched = sorted(list(resume_keywords & jd_keywords))
        missing = sorted(list(jd_keywords - resume_keywords))

        score = round((len(matched) / len(jd_keywords)) * 100, 2) if jd_keywords else 0.0

        insert_application(payload.company_name, payload.resume_text, payload.jd_text, score, matched, missing)

        return {
            "status": "success",
            "match_score": score,
            "matched_keywords": matched,
            "missing_keywords": missing
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))