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

# <-- MODIFIED SECTION START -->

# REMOVED this line:
# parser.add_argument("--value", default="App Development", help="Value to inject")

# ADDED this line:
parser.add_argument("--hook", default="I've been impressed by your innovative approach to mobile development.", help="The full personalized sentence for the company.")

args = parser.parse_args()

msg = EmailMessage()
msg['Subject'] = f"Application for Flutter Developer Position"
msg['From'] = EMAIL_ADDRESS
msg['To'] = args.to
plain_text_template = """Passionate Flutter developer — performance, reliability, and pixel-perfect UI.

Date: {{Date}}
Hiring Team • {{Company Name}}

{{Hiring Team}},

I was excited to see the Flutter Developer opening at {{Company Name}}. It aligns perfectly with my Flutter expertise in building high-quality, performant mobile products where user experience and thoughtful execution are the top priority.

Over the past three years, I've built and shipped production Flutter apps, most recently leading the development of UPrides — taking it from initial concept to a full launch on both the App Store and Play Store.
UPrides: https://www.uprides.eu/
App Store: https://apps.apple.com/pt/app/uprides/id6612036583
Play Store: https://play.google.com/store/apps/details?id=com.bold.customer

I believe that great applications are built on a foundation of clear communication. Before writing code, I focus on in-depth conversations with designers, product owners, and backend engineers to pin down logistics — from data flows and API contracts to edge cases and the precise user interaction. This ensures the implementation stage runs smoothly and predictably.

This approach has led to measurable, high-impact results:
- Cut cold start time by 60% (from 5s to 2s) through targeted profiling and startup optimisations.
- Reduced crash rate by 85% via systematic debugging and strict null-safety practices.
- Maintained ~10ms/frame UI performance to eliminate jank and keep interactions feeling instant.
- Engineered live driver tracking by integrating the Google Maps SDK with WebSocket streams for real-time route updates.

My expertise spans the entire mobile development lifecycle. I translate Figma designs into pixel-perfect, highly responsive UIs (including optimizations for low-end devices), implement clean architectures (MVVM) with state management like Riverpod, and work within agile teams to manage end-to-end deployments.

{{PersonalizedHook}} I am eager to discuss how my experience in performance optimization and scalable architectures can help your team improve reliability and the overall user experience of your mobile products.

My resume is attached for your review, and I am available for an interview at your convenience.

Thank you for your time and consideration.

Best regards,
Himanshu Kumar
91 7037543555 | himanshu17113@gmail.com
LinkedIn: https://www.linkedin.com/in/himanshu17113/ | GitHub: https://github.com/himanshu17113 | Portfolio: https://himanshu17113.github.io/Himanshu/
"""


# Read the HTML file (assumes mail.html is next to this script)
html_path = os.path.join(os.path.dirname(__file__), 'mail.html')
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# prepare replacements
replacements = {
    "{{Company Name}}": args.company,
    "{{Hiring Team}}": args.hiring_team,
    "{{PersonalizedHook}}": args.hook,
    "{{Date}}": datetime.date.today().strftime("%d %B %Y")
}


# apply to both templates in one loop
plain_text = plain_text_template
for key, val in replacements.items():
    html_content = html_content.replace(key, val)
    plain_text = plain_text.replace(key, val)

# attach plain text and HTML
msg.set_content(plain_text)
msg.add_alternative(html_content, subtype='html')


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)