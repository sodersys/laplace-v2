from google.auth import default
from google.auth.exceptions import DefaultCredentialsError


# if not hosting on google cloud, load env.
try:
    creds, project = default()
except DefaultCredentialsError:
    from dotenv import load_dotenv
    load_dotenv()
