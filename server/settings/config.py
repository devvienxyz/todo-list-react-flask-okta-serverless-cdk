import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../.env")

SECRET_KEY = os.getenv("SECRET_KEY")
IS_PROD = not os.getenv("FLASK_DEBUG", 0)
# EXTRA_CORS_ALLOWED = json.loads(os.getenv("EXTRA_CORS_ALLOWED", "[]"))
# EXTRA_CORS_ALLOWED = ["localhost"]
# CORS_ALLOWED = [
#     "https://devvien.pythonanywhere.com",
#     "devvien.anywhere.com",
#     "https://digital-assay.vercel.app",
# ] + EXTRA_CORS_ALLOWED
# CORS_ALLOWED = "*"
CORS_ORIGINS = (
    []
    if IS_PROD
    else ["http://localhost:3000", "http://127.0.0.1:3000", "http://0.0.0.0"]
)

# plate config
PLATE_ROWS = [chr(ascii_value) for ascii_value in range(ord("A"), ord("H") + 1)]
PLATE_COLS = [index for index in range(1, 13)]

# s3
S3_BUCKET = "dev-assay-plate-iit"
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID", None)
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", None)
aws_region = os.getenv("AWS_DEFAULT_REGION", None)

TWILIO_API_KEY = os.getenv("TWILIO_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_PHONE_NUMBER = "+14422453896"
ORG_ADMIN_EMAIL = "keishalouisevivien.berondo+daaa@g.msuiit.edu.ph"
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
