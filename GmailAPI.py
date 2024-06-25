import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# getCredentials() function is used to get the credentials of the user to access the gmail account
def getCredentials():
  creds = None

  SCOPES = ['https://mail.google.com/'] # this scope allows us to read, write, send, and delete emails

  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first time.
  if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request()) 
    else:
      flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open('token.json', 'w') as token:
      token.write(creds.to_json())

  return creds

# getEmail() function is used to get the data of the specified mails from the user's gmail account
# it returns a dictionary in the format { 'Subject': subject, 'From': sender, 'Message': text }
def getEmail(service, message):
  msg = service.users().messages().get(userId='me', id=message['id']).execute()
  
  payload = msg.get('payload')
  headers = payload.get('headers')

  for header in headers:
    if header['name'] == 'Subject': 
      subject = header['value'] 
    if header['name'] == 'From': 
      sender = header['value']
  text = ""

  parts = payload.get('parts')
  for part in parts:
    data = part['body'].get('data', '')  # Safely retrieve the value of 'data' key with a default value of an empty string
    byte_code = base64.urlsafe_b64decode(data)
    text = text + byte_code.decode("utf-8")
  email = { 'MessageID': message['id'], 'Subject': subject, 'From': sender, 'Message': text }

  return email
  # msg  = service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()

# readEmails() function is used to read the emails from the user's gmail account
# it returns a list of dictionaries where each dictionary contains the data of an email
# it can be used to filter any label or state of the emails, that is, read or unread emails
def getEmails(labels=[], state=None):
  # Call the Gmail API
  creds = getCredentials() # this line gets the credentials of the user to access the gmail account
  service = build('gmail', 'v1', credentials=creds) # this line creates a service object that interacts with the Gmail API
  if not labels and not state:
    results = service.users().messages().list(userId='me').execute
  elif not state:
    results = service.users().messages().list(userId='me', labelIds=labels).execute()
  elif not labels:
    results = service.users().messages().list(userId='me', q=state).execute()
  else:
    results = service.users().messages().list(userId='me', labelIds=labels, q=state).execute()

  messages = results.get('messages', [])

  emails = []
  for message in messages:
    email = getEmail(service, message)
    emails.append(email)

  return emails

def removeLabels(email, labels):
  creds = getCredentials()
  service = build('gmail', 'v1', credentials=creds)
  msg = service.users().messages().modify(userId='me', id=email['MessageID'], body={'removeLabelIds': labels}).execute()
  return msg

def addLabels(email, labels):
  creds = getCredentials()
  service = build('gmail', 'v1', credentials=creds)
  msg = service.users().messages().modify(userId='me', id=email['MessageID'], body={'addLabelIds': labels}).execute()
  return msg

# Driver and Test code
if __name__ == '__main__':
  labels = ['INBOX'] # this line specifies the label of the emails to be read
  state = "is:unread" # this line specifies the state of the emails to be read
  emails = getEmails(labels, state) # this line calls the readEmails() function to read the emails from the user's gmail account
  # print the emails' subject and sender in order
  if not emails:
    print("No emails found.")
  else:
    for email in emails:
      # print(email)
      # print(email['Subject'], email['From'], email['Message'])
      # Save the email message as an html file
      with open(str(email['MessageID'])+'.html', 'w', encoding='utf-8') as file:
        file.write(email['Message'])
        print("Email saved as " + str(email['MessageID']) + ".html")
      # save the rest of the email data in a text file
      with open(str(email['MessageID'])+'.txt', 'w', encoding='utf-8') as file:
        # save the dictionary in the text file but remove the message key
        email.pop('Message')
        file.write(str(email))
        print("Email data saved in " + str(email['MessageID']) + ".txt")

def fetchAllEmails():
  emails = getEmails()
  return emails

def fetchInbox():
  labels = ['INBOX']
  inbox = getEmails(labels)
  return inbox

def fetchStarred():
  labels = ['STARRED']
  starred = getEmails(labels)
  return starred

def fetchUnread():
  state = "is:unread"
  unread = getEmails(state)
  return unread

def fetchRead():
  state = "is:read"
  read = getEmails(state)
  return read

def markRead(email):
  removeLabels(email, ['UNREAD'])

def markUnread(email):
  addLabels(email, ['UNREAD'])

def markStarred(email):
  addLabels(email, ['STARRED'])

def markUnstarred(email):
  removeLabels(email, ['STARRED'])

def deleteEmail(email):
  creds = getCredentials()
  service = build('gmail', 'v1', credentials=creds)
  msg = service.users().messages().delete(userId='me', id=email['MessageID']).execute()
  return msg

def archiveEmail(email):
  creds = getCredentials()
  service = build('gmail', 'v1', credentials=creds)
  msg = service.users().messages().modify(userId='me', id=email['MessageID'], body={'removeLabelIds': ['INBOX']}).execute()
  return msg