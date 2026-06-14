import os
import pickle
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


# If modifying scopes, delete token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def delete_old_emails(service, years=16):
    query = f"older_than:{years}y"
    print(f"Searching emails with query: {query}")

    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=500
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print("No emails found.")
        return

    print(f"Found {len(messages)} emails. Deleting...")

    for msg in messages:
        service.users().messages().delete(
            userId='me',
            id=msg['id']
        ).execute()

    print("Deletion completed.")




def list_unread_emails(service):
    results = service.users().messages().list(
        userId='me',
        labelIds=['UNREAD']
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print("No unread emails found.")
        return

    print(f"Total unread emails: {len(messages)}\n")

    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me',
            id=msg['id']
        ).execute()

        headers = msg_data['payload']['headers']

        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')

        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print("-" * 50)


def delete_unread_emails(service):
    results = service.users().messages().list(
        userId='me',
        labelIds=['UNREAD']
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print("No unread emails found.")
        return

    print(f"Total unread emails: {len(messages)}\n")

    for msg in messages:
        msg_data = service.users().messages().delete(
            userId='me',
            id=msg['id']
        ).execute()




def get_sent_emails(service, max_results=100):
    results = service.users().messages().list(
        userId='me',
        labelIds=['SENT'],
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])
    email_data = []

    for msg in messages:
        msg_detail = service.users().messages().get(
            userId='me',
            id=msg['id']
        ).execute()

        headers = msg_detail['payload']['headers']

        email_info = {
            'To': '',
            'Subject': '',
            'Date': '',
            'Snippet': msg_detail.get('snippet', '')
        }

        for header in headers:
            if header['name'] == 'To':
                email_info['To'] = header['value']
            elif header['name'] == 'Subject':
                email_info['Subject'] = header['value']
            elif header['name'] == 'Date':
                email_info['Date'] = header['value']

        email_data.append(email_info)

    return email_data


def save_to_excel(email_data, filename='sent_emails.xlsx'):
    df = pd.DataFrame(email_data)
    df.to_excel(filename, index=False)
    print(f"Saved {len(email_data)} emails to {filename}")






        
if __name__ == '__main__':
    service = authenticate_gmail()
    #delete_old_emails(service, years=16)  # Change number of years here
    #list_unread_emails(service)  # List unread emails after deletion
    emails = get_sent_emails(service, max_results=200)
    save_to_excel(emails)