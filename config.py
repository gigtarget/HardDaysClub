import os

# Get all sensitive data from Railway variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:CVyBMCpcoDAJJJfOstlYhsggkaouBuTK@yamanote.proxy.rlwy.net:32802/railway"
)

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "your_instagram_username")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "your_instagram_password")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_key")
