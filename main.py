from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import OpenSSL
import ssl
import smtplib

# Read list of domains from a .txt file
with open("domains.txt", "r") as file:
    domains = file.readlines()

# SMTP server details
smtp_server = "smtp.example.com"
smtp_port = 587
smtp_username = "email@example.com"
smtp_password = "password"
from_email = "email@example.com"
to_email = "email@example.com"


# Create the email message
message = MIMEMultipart("related")
message["Subject"] = "SSL Certificate Expiry for Domains"
message["From"] = from_email
message["To"] = to_email


# Create the HTML table
table = "<table border='1'><tr><th>Domain</th><th>Expiry Date</th></tr>"


# Iterate through the list of domains
for domain in domains:
    domain = domain.strip()  # remove leading/trailing whitespace
    cert = ssl.get_server_certificate((domain, 443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    bytes = x509.get_notAfter()
    timestamp = bytes.decode('utf-8')
    expiry_date = datetime.strptime(timestamp, '%Y%m%d%H%M%S%z').date()

    # Compare the expiration date to the current date
    remaining_days = (expiry_date - datetime.now().date()).days
    if remaining_days <= 5:
        expiry_date = f"<span style='color:red;'>{expiry_date}</span>"
    elif remaining_days <= 7:
        expiry_date = f"<span style='color:yellow;'>{expiry_date}</span>"
    else:
        expiry_date = f"<span style='color:green;'>{expiry_date}</span>"

    # Add a row to the table
    table += f"<tr><td>{domain}</td><td>{expiry_date}</td></tr>"

# Close the table
table += "</table>"

# Add the table to the email message
message.attach(MIMEText(table, "html"))

# Send the email
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(from_email, to_email, message.as_string())
    print("Sent email for all domains")
