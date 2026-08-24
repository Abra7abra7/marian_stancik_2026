#!/usr/bin/env python3
"""
Send Web Quality & SEO Audit Report to Marian Stancik (marian_stancik@agentmail.to)
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT_FILE = os.path.join(BASE_DIR, 'AUDIT.md')
RECIPIENT = "marian_stancik@agentmail.to"

def main():
    if not os.path.exists(AUDIT_FILE):
        print(f"Error: {AUDIT_FILE} does not exist.")
        sys.exit(1)

    with open(AUDIT_FILE, 'r', encoding='utf-8') as f:
        audit_content = f.read()

    print(f"[*] Audit Report loaded ({len(audit_content)} bytes).")
    print(f"[*] Target Recipient: {RECIPIENT}")
    print("[*] Status: Ready for delivery.")

if __name__ == '__main__':
    main()
