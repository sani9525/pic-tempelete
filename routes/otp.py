from fastapi import APIRouter, HTTPException, Form
from pydantic import EmailStr
from datetime import datetime, timedelta
from utils.otp_verification import generate_otp, send_otp_email

router = APIRouter(prefix="/otp", tags=["OTP"])

# In-memory storage for OTPs (for production use Redis or DB)
otp_storage = {}

OTP_EXPIRY_MINUTES = 5

@router.post("/send-otp/")
def send_otp(email: EmailStr = Form(...)):
    otp = generate_otp()
    expiry_time = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)

    # Store OTP and expiry
    otp_storage[email] = {"otp": otp, "expires_at": expiry_time}

    # Send OTP via email
    try:
        send_otp_email(email, otp)
        return {"message": "OTP sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send OTP: {str(e)}")

@router.post("/verify-otp/")
def verify_otp(email: EmailStr = Form(...), otp: str = Form(...)):
    record = otp_storage.get(email)

    if not record:
        raise HTTPException(status_code=400, detail="OTP not sent or expired")

    if datetime.utcnow() > record['expires_at']:
        del otp_storage[email]
        raise HTTPException(status_code=400, detail="OTP expired")

    if record['otp'] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # OTP is valid, remove it
    del otp_storage[email]
    return {"message": "OTP verified successfully"}
