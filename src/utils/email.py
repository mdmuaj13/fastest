import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None

    token_path = os.path.join(os.path.dirname(__file__), "token.json")
    credentials_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "credentials.json")
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                print(f"[EMAIL] Application credentials not found at {credentials_path}. Email will not be sent.")
                return None
                
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        print(f"[EMAIL] An error occurred building service: {error}")
        return None

def send_welcome_email(to_email: str) -> bool:
    """
    Send a welcome email to newly registered user using Gmail API.
    """
    subject = "Welcome to Registro!"
    html_content = f"""
    <html>
        <body>
            <h1>Welcome to Registro!</h1>
            <p>Thank you for registering with us.</p>
            <p>Your account has been created successfully with email: <strong>{to_email}</strong></p>
            <p>Best regards,<br>The Registro Team</p>
        </body>
    </html>
    """
    
    service = get_gmail_service()
    
    if not service:
        print(f"[EMAIL] Gmail service not available. simulating email to: {to_email}")
        return True

    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = "me"
        message["To"] = to_email
        
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Check if we need to encode, Gmail API expects base64url encoded string
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        create_message = {"raw": encoded_message}
        
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        
        print(f"[EMAIL] Welcome email sent successfully to: {to_email}. Message Id: {send_message['id']}")
        return True
        
    except HttpError as error:
        print(f"[EMAIL] An error occurred: {error}")
        return False
    except Exception as e:
        print(f"[EMAIL] Failed to send welcome email to {to_email}: {str(e)}")
        return False
