import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    creds = None

    # Load existing token
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def delete_large_emails(service, size_in_mb=2000):
    # Gmail search query for large emails
    query = f"larger:{size_in_mb}M"

    results = service.users().messages().list(
        userId='me',
        q=query
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print("No large emails found.")
        return

    print(f"Found {len(messages)} large emails.")

    for msg in messages:
        service.users().messages().trash(
            userId='me',
            id=msg['id']
        ).execute()

    print("Large emails moved to Trash successfully!")


if __name__ == '__main__':
    service = authenticate_gmail()
    delete_large_emails(service, size_in_mb=20)



    


