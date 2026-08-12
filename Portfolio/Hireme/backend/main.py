import json
import os
from pathlib import Path
from typing import AsyncGenerator, Optional

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader
import docx
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"

app = FastAPI(title="Rishabh's AI Portfolio API", version="2.0.0")

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files (frontend) ───────────────────────────────────────────────────
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
RESUME_PATH  = FRONTEND_DIR / "Rishabh_Shukla_Data_Engineer.pdf"
if not RESUME_PATH.exists():
    RESUME_PATH = Path(__file__).parent / "Rishabh_Shukla_Data_Engineer.pdf"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# ── Resume schema ─────────────────────────────────────────────────────────────
class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = []


class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    total_experience_years: float | None = None
    skills: list[str] = []
    experiences: list[Experience] = []
    education: list[str] = []
    projects: list[str] = []
    certifications: list[str] = []


resume_schema = Resume.model_json_schema()


# ── Request / Response models ──────────────────────────────────────────────────
class ChatRequest(BaseModel):
    qustion: str = Field(..., description="The question to ask the model.")


class MatchJDRequest(BaseModel):
    jd_text: str = Field(..., description="Job Description text to analyze.")


class CompetencyScore(BaseModel):
    category: str
    jd_requirement_score: int
    candidate_score: int


class JDMatchOutput(BaseModel):
    overall_match_percentage: int
    candidate_title: str
    summary: str
    competencies: list[CompetencyScore]
    matched_skills: list[str]
    missing_or_optional_skills: list[str]
    strengths: list[str]
    verdict: str


# ── Helpers ───────────────────────────────────────────────────────────────────
def read_pdf(file_path: str | Path) -> str:
    if not Path(file_path).exists():
        return ""
    reader = PdfReader(str(file_path))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def parse_resume(resume_text: str) -> Resume:
    system_prompt = f"""
    You are an expert resume parser.

    Extract information from the resume based on its meaning,
    not only based on exact section headings.

    Return ONLY valid JSON matching this schema:
    {resume_schema}

    Rules:
    1. Do not invent information.
    2. If a value is not available, return null.
    3. If a list has no information, return an empty list.
    4. Include internships inside experiences.
    5. Extract skills mentioned across the entire resume.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Parse this resume:\n\n{resume_text}"},
            ],
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content)
        return Resume(**data)
    except Exception:
        # Fallback default struct if API parsing fails
        return Resume(
            name="Rishabh Shukla",
            email="rishabshukla445@gmail.com",
            total_experience_years=4.0,
            skills=["Python", "FastAPI", "PyTorch", "Spark", "SQL", "Airflow", "Spatial Data", "LLM", "RAG"],
            experiences=[
                Experience(
                    company="HERE Technologies",
                    role="Spatial Data Specialist II",
                    duration="2022 — Present",
                    description="Spatial data engineering, GIS processing, location intelligence pipelines, automated ETL workflows, and spatial analytics.",
                    skills_used=["Python", "Spatial Data", "GIS", "SQL", "ETL", "Airflow"]
                ),
                Experience(
                    company="The Anon Tech",
                    role="Founder & AI Engineer",
                    duration="2025 — Present",
                    description="Building AI-powered automation solutions, LLM workflows, FastAPI services, and full-stack web applications.",
                    skills_used=["Python", "FastAPI", "Groq API", "LLMs", "RAG", "Vercel"]
                )
            ],
            projects=["Vayunav AI", "AIGnition", "Agent Unveil", "The Anon Tech"],
            certifications=[]
        )


def build_system_prompt(resume: Resume) -> str:
    return f"""
You are an AI assistant representing Rishabh Shukla — an AI/ML Engineer, Spatial Data Specialist, and Data Engineer.

You are being interviewed by an HR professional or tech recruiter. Answer questions confidently, professionally, 
and accurately, based ONLY on the candidate profile below.

=== CANDIDATE PROFILE ===
{resume.model_dump_json(indent=2)}

=== ADDITIONAL WORK EXPERIENCE & CONTEXT ===
- **HERE Technologies (2022 — Present)**: Spatial Data Specialist II
  • Expert in spatial data processing, GIS engineering, location intelligence pipelines, and automated ETL workflows.
  • Works extensively with Python, SQL, spatial databases, map data validation, and large-scale data pipelines.
- **The Anon Tech (2025 — Present)**: Founder & AI Engineer
  • Co-founded AI startup building intelligent automation solutions, LLM fine-tuning pipelines, and agentic workflows.
- LinkedIn: https://www.linkedin.com/in/rishabh-shukla-619062260/
- GitHub: https://github.com/rishabshukla445-coder
- Startup: https://the-anon-tech-uv5o.vercel.app/ (Co-founded "The Anon Tech")
- Live Projects:
  • Vayunav AI → https://vayunav-ai.onrender.com/
  • AIGnition (Streamlit) → https://aignition-powered-by-the-anon-tech.streamlit.app/
  • Agent Unveil (HuggingFace) → https://huggingface.co/spaces/RishabhCodes/agent-unveil

=== RULES ===
1. Answer ONLY using the provided information + context above.
2. Never hallucinate or invent facts.
3. If information is unavailable, say "I don't have enough information to answer that."
4. Be professional, concise, and enthusiastic about Rishabh's work.
5. If asked about private projects, mention they exist but are under NDA.
6. Respond as if Rishabh himself is answering (first person).
"""


# ── Cached resume (loaded once per process) ───────────────────────────────────
_cached_resume: Resume | None = None


def get_resume() -> Resume:
    global _cached_resume
    if _cached_resume is None:
        resume_text = read_pdf(RESUME_PATH)
        if resume_text:
            _cached_resume = parse_resume(resume_text)
        else:
            _cached_resume = parse_resume("")
    return _cached_resume


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    """Serve the frontend portfolio."""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Rishabh Shukla Portfolio API v2.0 — Frontend not found"}


@app.get("/health")
async def health():
    return {"status": "ok", "name": "Rishabh Shukla Portfolio API"}


@app.get("/resume/download")
async def download_resume():
    """Direct resume download endpoint returning binary PDF file."""
    pdf_file = FRONTEND_DIR / "Rishabh_Shukla_Data_Engineer.pdf"
    if not pdf_file.exists():
        pdf_file = Path(__file__).parent / "Rishabh_Shukla_Data_Engineer.pdf"
    
    if pdf_file.exists():
        return FileResponse(
            path=str(pdf_file),
            media_type="application/pdf",
            filename="Rishabh_Shukla_Resume.pdf",
            headers={"Content-Disposition": "attachment; filename=Rishabh_Shukla_Resume.pdf"},
        )
    return {"error": "Resume file not found on server"}


@app.post("/chatbot🤖")
def chatbot(request: ChatRequest):
    """Standard (non-streaming) chatbot endpoint."""
    resume = get_resume()
    system_prompt = build_system_prompt(resume)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.qustion},
        ],
    )
    return {"answer": response.choices[0].message.content}


@app.post("/stream_chat")
async def stream_chat(request: ChatRequest):
    """
    Streaming chatbot endpoint — yields SSE tokens as they are generated.
    Uses Groq streaming: stream=True
    """
    resume = get_resume()
    system_prompt = build_system_prompt(resume)

    async def event_generator() -> AsyncGenerator[str, None]:
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.qustion},
            ],
            stream=True,
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                # SSE format: data: <json>\n\n
                data = json.dumps({"content": content})
                yield f"data: {data}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/match_jd")
async def match_jd(
    jd_text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    jd_file: Optional[UploadFile] = File(None)
):
    file = file or jd_file
    """
    HR Job Description Matcher endpoint.
    Accepts text or uploaded file (.pdf, .docx, .txt), analyzes against Rishabh Shukla's profile,
    and returns competency comparison scores for rendering dynamic multi-line charts.
    """
    extracted_text = ""
    if file:
        filename = file.filename.lower()
        content = await file.read()
        if filename.endswith(".pdf"):
            import io
            reader = PdfReader(io.BytesIO(content))
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    extracted_text += t + "\n"
        elif filename.endswith(".docx"):
            import io
            doc = docx.Document(io.BytesIO(content))
            extracted_text = "\n".join([p.text for p in doc.paragraphs])
        else:
            extracted_text = content.decode("utf-8", errors="ignore")

    if not extracted_text and jd_text:
        extracted_text = jd_text

    if not extracted_text or not extracted_text.strip():
        raise HTTPException(status_code=400, detail="Please provide a valid Job Description text or document file.")

    resume = get_resume()
    candidate_info = f"""
Candidate Name: Rishabh Shukla
Current Roles: Spatial Data Specialist II at HERE Technologies (2022-Present) & Founder/AI Engineer at The Anon Tech (2025-Present)
Key Expertise:
- Python, SQL, Spatial Data Engineering, GIS Processing, ETL Pipelines, Apache Airflow, Apache Spark.
- AI/ML Engineering, PyTorch, TensorFlow, LLMs, RAG, Groq API, LangChain, HuggingFace.
- Web & Deployment: FastAPI, Streamlit, Docker, Vercel, Render, REST APIs.
- Experience: 4+ years of data engineering, spatial data analytics, ML model deployment, and product engineering.
    """

    matcher_prompt = f"""
You are an AI HR Specialist & Talent Analyst. Analyze the provided Job Description against candidate Rishabh Shukla's profile.

=== CANDIDATE PROFILE ===
{candidate_info}

=== JOB DESCRIPTION ===
{extracted_text}

=== INSTRUCTIONS ===
Evaluate the candidate's alignment with the Job Description. Produce a structured JSON object strictly matching this JSON schema:
{{
  "overall_match_percentage": <integer 0-100>,
  "candidate_title": <string e.g. "Senior AI & Data Engineer Fit">,
  "summary": <string summary of 2-3 sentences assessing candidate fit>,
  "competencies": [
    {{
      "category": "Python & Core Dev",
      "jd_requirement_score": <integer 0-100 score needed for job>,
      "candidate_score": <integer 0-100 Rishabh's actual proficiency>
    }},
    {{
      "category": "AI / ML & LLMs",
      "jd_requirement_score": <integer 0-100>,
      "candidate_score": <integer 0-100>
    }},
    {{
      "category": "Data & Spatial Engineering",
      "jd_requirement_score": <integer 0-100>,
      "candidate_score": <integer 0-100>
    }},
    {{
      "category": "Backend APIs & Microservices",
      "jd_requirement_score": <integer 0-100>,
      "candidate_score": <integer 0-100>
    }},
    {{
      "category": "Cloud, DevOps & MLOps",
      "jd_requirement_score": <integer 0-100>,
      "candidate_score": <integer 0-100>
    }},
    {{
      "category": "System Design & Leadership",
      "jd_requirement_score": <integer 0-100>,
      "candidate_score": <integer 0-100>
    }}
  ],
  "matched_skills": [<list of key matching technical skills>],
  "missing_or_optional_skills": [<list of secondary/optional missing skills or tools>],
  "strengths": [<list of 3 key strengths Rishabh brings to this role>],
  "verdict": <string e.g. "Excellent Match", "Strong Candidate", or "Moderate Match">
}}

Return ONLY valid JSON.
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": matcher_prompt}],
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze JD: {str(e)}")


# ── Serve frontend static assets ──────────────────────────────────────────────
@app.get("/{file_path:path}")
async def serve_frontend(file_path: str):
    """Serve any frontend static file (CSS, JS, images, fonts, etc.)."""
    full_path = FRONTEND_DIR / file_path
    if full_path.exists() and full_path.is_file():
        return FileResponse(str(full_path))
    # Fallback: return index.html for SPA routing
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"error": "Not found"}

