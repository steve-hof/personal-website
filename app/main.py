from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr

from .emailer import send_contact_email
from .schemas import ContactForm
from .settings import settings

app = FastAPI(title=settings.project_name)

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


# ----------------------------
# Contact form (HTML POST)
# ----------------------------
@app.post("/contact", response_class=HTMLResponse)
async def contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
):
    """
    Handles a simple HTML contact form submission.
    Expects form fields: name, email, message
    """
    data = ContactForm(name=name, email=email, message=message)

    success = await send_contact_email(data.name, data.email, data.message)

    # These template names assume you already have these files in app/templates/...
    template = "partials/contact_success.html" if success else "components/flash.html"
    context = {"request": request, "success": success, "name": data.name}

    return templates.TemplateResponse(template, context)


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


@app.post("/api/lead")
async def create_lead(lead: Lead):
    """
    Optional JSON endpoint if you want to submit the form via fetch()
    instead of a normal HTML form POST.
    """
    message = (
        "New tutoring request:\n\n"
        f"Name: {lead.name}\n"
        f"Email: {lead.email}\n"
        f"Subject: {lead.subject}\n"
        f"Grade level: {lead.grade_level}\n"
        f"Notes: {lead.notes or ''}\n"
        f"Submitted: {lead.submitted_at or ''}\n"
        f"Source: {lead.source or ''}\n"
    )

    ok = await send_contact_email(lead.name, str(lead.email), message)

    return {"ok": ok, "received_at": datetime.utcnow().isoformat() + "Z"}
