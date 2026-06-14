import os
import base64
import mimetypes
import pandas as pd
import pickle

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


# ---------------------------------------------------
# Authenticate Gmail API
# ---------------------------------------------------
def authenticate_gmail():
    creds = None

    # Load saved token
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Login if token missing/expired
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


# ---------------------------------------------------
# Create Email with Attachment
# ---------------------------------------------------
def create_message_with_attachment(to, subject, body, attachment_path):

    message = MIMEMultipart()

    message['to'] = to
    message['subject'] = subject

    # Email body
    message.attach(MIMEText(body, 'plain'))

    # Attachment
    if attachment_path and os.path.isfile(attachment_path):

        content_type, encoding = mimetypes.guess_type(attachment_path)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'

        main_type, sub_type = content_type.split('/', 1)

        with open(attachment_path, 'rb') as file:
            mime = MIMEBase(main_type, sub_type)
            mime.set_payload(file.read())

        encoders.encode_base64(mime)

        filename = os.path.basename(attachment_path)

        mime.add_header(
            'Content-Disposition',
            f'attachment; filename="{filename}"'
        )

        message.attach(mime)

    # Encode message
    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    return {'raw': raw_message}


# ---------------------------------------------------
# Send Email
# ---------------------------------------------------
def send_email(service, to_email, name, attachment_path):

    organization = to_email.split('@')[1].split('.')[0].capitalize()

    print(organization )
    
    subject = f"Applying for the Job Opportunity QA/Tech LEAD/Architect Resume Submission {organization}"

    body = f"""
Hello {name},


Good Morning,

Hope you doing good .
Would like to express my interest in the job opportunity for esteemed organisation.


First Name : Pallabjyoti
Last Name : Saikia
Total experience 11 + years in IT industry.

Primary Skills : Storage, Embedded Systems, Kubernetes, File Systems, Linux.

Current Role  Tech Lead at Aziro ( formerly MSysTechnologies).
N.P: Immediate joining possible.

Prev. Organizations : Sony, Netapp ( product organisations) 


Base Location: Pune.
DoB: 25/12/1988

Please find my resume attached for your reference.

Regards,
Pallab
9730650615
"""

    message = create_message_with_attachment(
        to_email,
        subject,
        body,
        attachment_path
    )

    try:
        service.users().messages().send(
            userId='me',
            body=message
        ).execute()

        print(f"Email sent to: {to_email}")

    except Exception as e:
        print(f"Failed to send email to {to_email}")
        print(e)


# ---------------------------------------------------
# Main Function
# ---------------------------------------------------
def main():

    # Authenticate Gmail
    service = authenticate_gmail()

    # Read Excel Sheet
    df = pd.read_excel('emails.xlsx')

    # Attachment file
    attachment_path = 'Pallabjyoti Saikia_Resume.docx'

    # Send to all emails
    for index, row in df.iterrows():

        email = row['email']
        name = row.get('name', 'Sir/Madam')

        send_email(
            service,
            email,
            name,
            attachment_path
        )


# ---------------------------------------------------
# Run Program
# ---------------------------------------------------
if __name__ == '__main__':
    main()