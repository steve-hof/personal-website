from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .schemas import ContactForm
from .emailer import send_contact_email
from .settings import settings

app = FastAPI(title=settings.project_name)
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Lead(BaseModel):
    name: str
    email: EmailStr
    subject: str
    grade_level: str
    notes: str | None = None
    submitted_at: str | None = None
    source: str | None = None

@app.post("/api/lead")
async def create_lead(lead: Lead):
    # Reuse your existing email sending function by converting the lead into a message
    message = (
        f"New tutoring request:\n\n"
        f"Name: {lead.name}\n"
        f"Email: {lead.email}\n"
        f"Subject: {lead.subject}\n"
        f"Grade level: {lead.grade_level}\n"
        f"Notes: {lead.notes or ''}\n"
        f"Submitted: {lead.submitted_at or ''}\n"
        f"Source: {lead.source or ''}\n"
    )

    # This uses your existing emailer (already wired for /contact)
    ok = await send_contact_email(lead.name, str(lead.email), message)

    return {"ok": ok, "received_at": datetime.utcnow().isoformat() + "Z"}
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

#@app.get("/", response_class=HTMLResponse)
#async def index(request: Request):
#    return templates.TemplateResponse("index.html", {"request": request, "title": settings.project_name})

@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse("app/static/index.html")

@app.post("/contact", response_class=HTMLResponse)
async def contact(request: Request, name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    data = ContactForm(name=name, email=email, message=message)
    success = await send_contact_email(data.name, data.email, data.message)
    template = "partials/contact_success.html" if success else "components/flash.html"
    context = {"request": request, "success": success, "name": data.name}
    return templates.TemplateResponse(template, context)
