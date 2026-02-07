import os
import httpx

def _must_get(name: str) -> str:
    v = os.getenv(name, "").strip()
    if not v:
        raise RuntimeError(f"Missing required env var: {name}")
    return v

async def send_contact_email(name: str, email: str, message: str) -> bool:
    try:
        api_key = _must_get("RESEND_API_KEY")
        to_addr = _must_get("CONTACT_TO")
        from_addr = os.getenv("EMAIL_FROM", "onboarding@resend.dev").strip()

        subject = f"New tutoring inquiry — {name}"
        text = message + f"\n\n---\nReply-To: {email}\n"

        payload = {
            "from": from_addr,
            "to": [to_addr],
            "subject": subject,
            "text": text,
            "reply_to": email,
        }

        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {api_key}"},
                json=payload,
            )
            print(f"RESEND status={r.status_code} body={r.text[:300]}")
            return 200 <= r.status_code < 300

    except Exception as e:
        print(f"RESEND FAILED: {e}")
        return False
