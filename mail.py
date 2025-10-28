import sys

import os
import smtplib
import imghdr
from email.message import EmailMessage
import argparse
import datetime

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')




parser = argparse.ArgumentParser(description="Send HTML cover letter email")
parser.add_argument("--to", default="himanshu17113@gmail.com", help="Recipient email")
parser.add_argument("--company", default="Your Company", help="Company name to inject")
parser.add_argument("--hiring_team", default="Hiring Team", help="Hiring team name to inject")
parser.add_argument("--value", default="App Development", help="Value to inject")

args = parser.parse_args()

msg = EmailMessage()
msg['Subject'] = f"Application for {args.position} Position"
msg['From'] = EMAIL_ADDRESS
msg['To'] = args.to

msg.set_content('This is a plain text email')

# Read the HTML file (assumes mail.html is next to this script)
html_path = os.path.join(os.path.dirname(__file__), 'mail.html')
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Simple placeholder replacements (matches tokens in your mail.html)
replacements = {
    "{{Company Name}}": args.company,
  "{{Hiring Team}}": args.hiring_team,
  "{{Mention a specific app, feature, or company value}}": args.value
}

for key, val in replacements.items():
    html_content = html_content.replace(key, val)
# Insert current date into template (e.g. replaces {{Date}})
date_str = datetime.date.today().strftime("%d %B %Y")
html_content = html_content.replace("{{Date}}", date_str)
msg.add_alternative(html_content, subtype='html')


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)