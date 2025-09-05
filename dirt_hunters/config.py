import os
from socket import gethostname

from dotenv import load_dotenv

if "liveconsole" in gethostname():
    project_folder = os.path.expanduser("~/dirt-hunters")
    load_dotenv(os.path.join(project_folder, ".env"))
else:
    load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
