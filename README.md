# 📌 Email Automation Tool — Python Internship Major Project

This project sends personalized bulk emails to multiple recipients using CSV input, with dynamic sender name, subject, message body, attachments & Gmail App Password authentication.

Useful for internship/job outreach, HR communication, invitations and announcements.

---
# 🚀 Features
| Feature                                  | Status |
| ---------------------------------------- | ------ |
| Dynamic sender name & Gmail              | ✅      |
| Reads CSV (name + email)                 | ✅      |
| Sends bulk personalized emails           | ✅      |
| Password masking modes                   | ✅      |
| Attachment support (PDF / images / docs) | ✅      |
| Dry-run (preview without sending)        | ✅      |
| Logs of successes & failures             | ✅      |
| Professional HTML email format           | ✅      |

  
---

# 📂 Sample CSV (sample_students.csv) 

name,email <br>
Rahul Sharma,rahul@example.com<br>
Sneha Verma,sneha@example.com<br>
Aman Gupta,aman@example.com<br>


# 🔧 Installation
pip install pwinput

# ▶️ How to Run
python Sender.py**

---
## 📸 Output Preview

> Sample execution of the Email Automation Tool in terminal

![Screenshot](images/capture1.jpg)
![Screenshot](images/capture2.jpg)

---
# 🧠 Tech Used
| Module / Concept  | Purpose                 |
| ----------------- | ----------------------- |
| `smtplib`         | Email sending           |
| `email.message`   | Email template          |
| `pwinput`         | Secure password masking |
| `csv`             | Read recipient list     |
| `os` + `datetime` | Logging system          |

---
# ⚠️ Important Notes
| Requirement                                          | Reason                              |
| ---------------------------------------------------- | ----------------------------------- |
| Gmail App Password required                          | Normal Gmail password won't work    |
| 2-Step Verification must be ON                       | Required to get App Password        |
| Sending many emails too fast may trigger spam filter | Tool already includes polite delays |

---
## 📌 Project Use Case Example (Internships)

This tool can be used for sending **professional internship request emails** to multiple HRs / companies with:

- Personalized greeting  
- Your resume attached  
- Professional subject + body  
- Company-wise tracking via logs  

---

## ⭐ Author

**Vanshika Gupta**  
_ Python Internship Major Project — Axcentra _
