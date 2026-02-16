import os.path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.email import get_gmail_service

def main():
    print("Starting Gmail API Token Generation...")
    print("Checking for credentials.json in 'server/' folder...")
    
    credentials_path = os.path.join(os.path.dirname(__file__), "credentials.json")
    if not os.path.exists(credentials_path):
        print(f"Error: {credentials_path} not found.")
        print("Please place your downloaded 'credentials.json' from Google Cloud Console in the 'server/' directory.")
        return

    # get_gmail_service handles the token generation if it doesn't exist
    service = get_gmail_service()
    
    if service:
        print("\nSuccess! token.json has been generated or updated.")
        print("Location: server/src/utils/token.json")
        print("You can now send emails using the Gmail API.")
    else:
        print("\nFailed to generate token.json. Please check the error messages above.")

if __name__ == "__main__":
    main()
