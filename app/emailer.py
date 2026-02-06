from .settings import settings

# In production, swap this for Mailgun/SendGrid/Resend/Pipeline
# For now, just log to console; return True/False

async def send_contact_email(name: str, email: str, message: str) -> bool:
    # Replace with an async HTTP call to your provider
    print("CONTACT FORM SUBMISSION")
    print({"name": name, "email": email, "message": message})
    return True
