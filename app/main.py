from datetime import datetime
from pathlib import Path
from typing import Optional
from fastapi import Response
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr

from .emailer import send_contact_email
from .schemas import ContactForm
from .settings import settings
from app.leads_db import init_db, insert_lead

app = FastAPI(title=settings.project_name)
@app.on_event("startup")
async def _startup():
    init_db()

# Serve static assets (favicon, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates used for partials (success message / flash)
templates = Jinja2Templates(directory="app/templates")

# ----------------------------
# Landing page
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def index():
    """
    Serves the static landing page located at app/static/index.html
    """
    index_path = Path("app/static/index.html")
    return FileResponse(index_path)

@app.head("/")
async def head_root():
    return Response(status_code=200)


from fastapi import HTTPException

@app.get("/{page_name}", response_class=HTMLResponse)
async def static_page(page_name: str):
    """
    Serves static HTML pages from app/static.
    Allows /high-school-math-tutor-victoria to load high-school-math-tutor-victoria.html
    """
    # allow both /foo and /foo.html
    candidates = [
        Path("app/static") / f"{page_name}.html",
        Path("app/static") / page_name,
    ]

    for p in candidates:
        if p.exists() and p.is_file():
            return FileResponse(p)

    raise HTTPException(status_code=404, detail="Not Found")
# ----------------------------
# Stat 252 Landing page
# ----------------------------



@app.get("/stat-252")
async def stat_252_redirect():
    return RedirectResponse(url="/stat-252-tutor-uvic", status_code=301)

@app.get("/stat-252-tutor-uvic")
async def stat252_tutor_uvic():
    return FileResponse(Path("app/static/stat-252-tutor-uvic.html"))

@app.head("/stat-252-tutor-uvic")
async def head_stat252():
    return Response(status_code=200)

# ----------------------------
# Math 151 Landing page
# ----------------------------
@app.get("/math-151-tutor-uvic")
async def math_151_tutor_uvic():
    return FileResponse(Path("app/static/math-151-tutor-uvic.html"))


@app.head("/math-151-tutor-uvic")
async def head_math151():
    return Response(status_code=200)
# ----------------------------
# Psych 300 Landing Page
# ----------------------------
@app.get("/psych-300-statistics-tutor-uvic")
async def psych_300_statistics_tutor_uvic():
    return FileResponse(Path("app/static/psych-300-statistics-tutor-uvic.html"))


@app.head("/psych-300-statistics-tutor-uvic")
async def head_psych300():
    return Response(status_code=200)


# ----------------------------
# Contact form (HTML POST)
# ----------------------------




# ----------------------------
# JSON lead endpoint (optional)
# ----------------------------
class Lead(BaseModel):
    name: str
    email: EmailStr
    subject: str
    grade_level: str
    notes: Optional[str] = None
    submitted_at: Optional[str] = None
    source: Optional[str] = None


@app.post("/contact")
async def contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(""),
    course: str = Form(""),
    message: str = Form(...),
    website: str = Form(""),  # honeypot
):
    # spam trap
    if website.strip():
        return RedirectResponse(url="/?sent=1#contact", status_code=303)

    full_message = (
        f"New tutoring inquiry:\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Subject: {subject}\n"
        f"Course: {course}\n\n"
        f"Message:\n{message}\n"
    )

    ok = await send_contact_email(name, email, full_message)
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")

    insert_lead(
        name=name,
        email=email,
        subject=subject,
        course=course,
        message=message,
        email_sent=ok,
        ip=ip,
        user_agent=ua,
    )
    return RedirectResponse(
        url=f"/?sent={1 if ok else 0}#contact",
        status_code=303,
    )


