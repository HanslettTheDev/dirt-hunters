import json
import os

import msal
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]
MAIL_USERNAME = os.getenv("MAIL_USERNAME")


def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
    )

    result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result["access_token"]

    else:
        raise Exception(
            "Failed to accquire token",
            result.get("error"),
            result.get("error_description"),
        )


def send_email_via_graph_api(subject, recipient, body):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    email_data = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body,
            },
            "from": {
                "emailAddress": {
                    "address": MAIL_USERNAME,
                }
            },
            "toRecipients": [{"emailAddress": {"address": recipient}}],
        }
    }
    user_endpoint = f"https://graph.microsoft.com/v1.0/users/{MAIL_USERNAME}/sendMail"
    response = requests.post(
        user_endpoint, headers=headers, data=json.dumps(email_data)
    )

    if response.status_code != 202:
        raise Exception(
            f"Error sending Email: {response.status_code} - {response.text}"
        )

    return response.status_code


def send_welcome_email():
    subject = "Welcome"
    recipient = "hanslettthedev@gmail.com"
    body = f"Hi there, \n\nWelcome, we are glad to have you! "
    send_email_via_graph_api(subject, recipient, body)


if __name__ == "__main__":
    print(send_welcome_email())
