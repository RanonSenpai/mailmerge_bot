# This is a Mailmerge Bot to send multiple Mails with dynamic content to multiple recepient

# Importing Libraries
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

# Variables
CLIENT_SECRET_FILE = "Client/client_secret.json"
API_NAME = "gmail"
API_VERSION = "v1"
SCOPE = ["https://mail.google.com/"]


def get_variable(variable_name, count):
    # Variable Fetching System
    f = open("Variables/" + variable_name + ".txt", "r")
    content = f.readlines()
    return content[count].replace("\n", "")


def load_email_layout_subject():
    # Load Email Layout - Subject
    f = open("Layout/subject.txt", "r")
    content = f.read()
    return content


def load_email_layout_body():
    # Load Email Layout - Body
    f = open("Layout/body.txt", "r")
    content = f.read()
    return content


def send_email(to, subject, content):
    # Logic to send email via Gmail API
    emailMsh = content
    mimeMessage = MIMEMultipart()
    mimeMessage["to"] = to
    mimeMessage["subject"] = subject
    mimeMessage.attach(MIMEText(emailMsh, "html"))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(
        userId='me', body={'raw': raw_string}).execute()

    # Logging
    print("[+] Email : " + to + " Subject : " +
          subject + " - Email Delivered Successfully !")


print("[ --- Gmail Mailmerge Bot --- ]")
print("[*] Initializing API")

# Initializing Google Service
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPE)

# Looping through all the emails
email_list_file = open("variables/email.txt", "r")
count = 0

for email in email_list_file:
    email = email.replace("\n", "")

    # Loading Email Subject
    subject = load_email_layout_subject()
    # Formatting Email Subject with Variables
    subject_formatted = re.sub(
        r'<<([^>]*)>>', lambda m: get_variable(m.group(1), count), subject)

    # Loading Email Body
    body = load_email_layout_body()
    # Formatting Email Body with Variables
    body_formatted = re.sub(
        r'<<([^>]*)>>', lambda m: get_variable(m.group(1), count), body)

    # Sending Email
    send_email(email, subject_formatted, body_formatted)

    count += 1
