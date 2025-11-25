"""
Email Automation Tool — Internship Major Project
Windows-Compatible, Debug/Preview Mode Included
Features:
- Dynamic sender name, email, subject, body
- CSV reading & multiple recipients
- Gmail App Password authentication
- Multi-line message body
- Logs of successes/failures
- HTML formatting
- Attachments support
- Dry-run / preview mode
- Polite delays between emails
- Password input modes: full mask, last 3 visible, fully visible
- Terminal live debug / step-by-step preview per recipient
"""

import csv
import smtplib
import sys
import os
from email.message import EmailMessage
from datetime import datetime
import time
import pwinput  # Cross-platform password input with mask

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "send_log.txt")
os.makedirs(LOG_DIR, exist_ok=True)

# ----------------- Logging -----------------
def write_log(line: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {line}\n")

# ----------------- CSV Reader -----------------
def read_csv(path):
    rows = []
    try:
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if 'name' not in reader.fieldnames or 'email' not in reader.fieldnames:
                raise ValueError("CSV must contain 'name' and 'email'")
            for row in reader:
                name = row.get('name', '').strip()
                email = row.get('email', '').strip()
                if name and email:
                    rows.append({'name': name, 'email': email})
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR reading CSV: {e}")
        sys.exit(1)
    return rows

# ----------------- Password Input Modes -----------------
def input_password():
    while True:
        print("\nPassword Visibility Mode:")
        print("1 → Hide completely (********)")
        print("2 → Hide except last 3 characters (***********xyz)")
        print("3 → Show full password while typing")
        mode = input("Choose option (1/2/3): ").strip()
        if mode not in ["1", "2", "3"]:
            print("Invalid choice. Try again.")
            continue

        if mode == "3":
            password = input("Enter your App Password: ")
        elif mode == "1":
            password = pwinput.pwinput(prompt="Enter your App Password: ", mask="*")
            print("Password entered: " + "*" * len(password))
        elif mode == "2":
            temp = pwinput.pwinput(prompt="Enter your App Password: ", mask="*")
            if len(temp) > 3:
                print(f"Password entered: {'*'*(len(temp)-3) + temp[-3:]}")
            else:
                print(f"Password entered: {temp}")
            password = temp

        confirm = input("Confirm password? (y/n): ").lower()
        if confirm == "y":
            return password

# ----------------- Build Email -----------------
def build_message(sender_name, sender_email, recipient_name, recipient_email, subject, body_text, attachment_path=None):
    msg = EmailMessage()
    msg['From'] = f"{sender_name} <{sender_email}>"
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # HTML body (simple professional formatting)
    html_body = f"""
    <html>
      <body>
        <p>Dear {recipient_name},</p>
        <p>{body_text.replace('\n','<br>')}</p>
        <p>Regards,<br>{sender_name}</p>
      </body>
    </html>
    """
    msg.add_alternative(html_body, subtype='html')

    # Attachments
    if attachment_path and os.path.isfile(attachment_path):
        with open(attachment_path, 'rb') as f:
            data = f.read()
            filename = os.path.basename(attachment_path)
        msg.add_attachment(data, maintype='application', subtype='octet-stream', filename=filename)

    return msg

# ----------------- Send Emails with Debug -----------------
def send_emails_debug(smtp_host, smtp_port, sender_email, app_password, rows, sender_name, subject, body_text, attachment_path=None, pause_between=1.0, dry_run=False):
    sent_count = 0
    failed_count = 0

    try:
        if not dry_run:
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.ehlo()
            server.starttls()
            server.login(sender_email, app_password)
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed: check your email or app password.")
        write_log("AUTH_FAILED")
        sys.exit(1)
    except Exception as e:
        print(f"SMTP connection/login failed: {e}")
        write_log(f"SMTP_CONN_FAILED: {e}")
        sys.exit(1)

    for i, row in enumerate(rows, start=1):
        rname = row['name']
        remail = row['email']

        # Terminal preview / debug
        print("\n" + "="*60)
        print(f"[{i}/{len(rows)}] Preview Email to: {rname} <{remail}>")
        print(f"Subject: {subject}\n")
        print(f"Body:\nDear {rname},\n{body_text}\nRegards,\n{sender_name}")
        if attachment_path:
            print(f"Attachment: {attachment_path}")
        print("="*60)

        proceed = input("Send this email? (y/n) or skip all remaining (s): ").strip().lower()
        if proceed == 's':
            print("Skipping remaining emails...")
            break
        if proceed != 'y':
            print(f"Skipped: {remail}")
            write_log(f"SKIPPED: {remail}")
            failed_count += 1
            continue

        if dry_run:
            print(f"[DRY-RUN] Email to {remail} not actually sent.")
            sent_count += 1
            time.sleep(pause_between)
            continue

        # Build & send message
        try:
            msg = build_message(sender_name, sender_email, rname, remail, subject, body_text, attachment_path)
            server.send_message(msg)
            print(f"[SENT] Email to {remail}")
            write_log(f"SENT: {remail}")
            sent_count += 1
            time.sleep(pause_between)
        except Exception as e:
            print(f"[FAILED] {remail}: {e}")
            write_log(f"FAILED: {remail} error={e}")
            failed_count += 1

    if not dry_run:
        server.quit()

    print(f"\nDone. Sent: {sent_count}, Skipped/Failed: {failed_count}")
    return sent_count, failed_count

# ----------------- Main -----------------
def main():
    print("\n=== Email Automation Tool — Internship Major Project ===\n")
    csv_path = input("Path to CSV (default: sample_students.csv): ").strip() or "sample_students.csv"
    rows = read_csv(csv_path)
    if not rows:
        print("No valid rows found in CSV. Exiting.")
        sys.exit(0)

    sender_name = input("Enter your (sender) name: ").strip()
    sender_email = input("Enter your sender email (Gmail): ").strip()
    print("NOTE: For Gmail, use an App Password (16 characters).")
    app_password = input_password()

    subject = input("Enter email subject: ").strip()
    print("\nEnter the message body (type 'END' on a new line to finish):\n")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    body_text = "\n".join(lines).strip()
    if not body_text:
        print("Empty message body — exiting.")
        sys.exit(0)

    attachment_path = input("Enter attachment path (optional, press Enter to skip): ").strip() or None
    dry_run_input = input("Do you want to run in dry-run mode (no emails will be sent)? (y/n): ").strip().lower()
    dry_run = dry_run_input == 'y'

    smtp_host = "smtp.gmail.com"
    smtp_port = 587

    print(f"\nStarting send to {len(rows)} recipients...")
    write_log(f"START send by {sender_email} to {len(rows)} recipients; subject={subject}")

    send_emails_debug(smtp_host, smtp_port, sender_email, app_password, rows, sender_name, subject, body_text, attachment_path, pause_between=1.0, dry_run=dry_run)

if __name__ == '__main__':
    main()
