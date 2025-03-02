import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../.env")


class Config:
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

    # s3
    S3_BUCKET = "dev-assay-plate-iit"
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID", None)
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", None)
    aws_region = os.getenv("AWS_DEFAULT_REGION", None)

    # Database
    MONGO_CONFIG = {"MONGO_URI": os.getenv("MONGO_URI")}
    MONGO_URI = MONGO_CONFIG["MONGO_URI"]
