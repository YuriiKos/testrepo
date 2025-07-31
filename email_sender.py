#!/usr/bin/env python3
"""
Email File Sender Script

This script sends files from a specified folder to a list of recipients
with a predefined message. Recipients are read from a text file.

Requirements:
- Python 3.6+
- Valid email credentials
- Recipients file with email addresses (one per line)
- Files folder containing files to send

Usage:
    python email_sender.py

Configuration:
- Update EMAIL_CONFIG with your email settings
- Modify FILES_FOLDER path
- Modify RECIPIENTS_FILE path
- Customize EMAIL_SUBJECT and EMAIL_BODY
"""

import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import logging
from typing import List, Optional

# Configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # Change this for other providers
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',  # Update with your email
    'sender_password': 'your_app_password',   # Use app password for Gmail
    'sender_name': 'Your Name'               # Optional display name
}

# File and folder paths
FILES_FOLDER = './files_to_send'           # Folder containing files to send
RECIPIENTS_FILE = './recipients.txt'       # File containing recipient emails
LOG_FILE = './email_sender.log'            # Log file for tracking

# Email content
EMAIL_SUBJECT = 'Files for Review'
EMAIL_BODY = """
Dear Recipient,

I hope this email finds you well.

Please find the attached files for your review. These documents contain important information that requires your attention.

Key points:
- Please review all attached files carefully
- Feel free to reach out if you have any questions
- Your feedback is greatly appreciated

Thank you for your time and consideration.

Best regards,
{sender_name}
"""

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def load_recipients(file_path: str) -> List[str]:
    """
    Load email recipients from a text file.
    
    Args:
        file_path: Path to the recipients file
        
    Returns:
        List of email addresses
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            recipients = [line.strip() for line in f if line.strip() and '@' in line]
        
        if not recipients:
            raise ValueError("No valid email addresses found in recipients file")
            
        logger.info(f"Loaded {len(recipients)} recipients from {file_path}")
        return recipients
        
    except FileNotFoundError:
        logger.error(f"Recipients file not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading recipients: {e}")
        raise


def get_files_to_send(folder_path: str) -> List[str]:
    """
    Get list of files to send from the specified folder.
    
    Args:
        folder_path: Path to the folder containing files
        
    Returns:
        List of file paths
    """
    try:
        folder = Path(folder_path)
        if not folder.exists():
            raise FileNotFoundError(f"Files folder not found: {folder_path}")
            
        files = [str(f) for f in folder.iterdir() if f.is_file()]
        
        if not files:
            logger.warning(f"No files found in {folder_path}")
            return []
            
        logger.info(f"Found {len(files)} files to send: {[os.path.basename(f) for f in files]}")
        return files
        
    except Exception as e:
        logger.error(f"Error getting files from {folder_path}: {e}")
        raise


def create_email_message(sender_email: str, recipient_email: str, 
                        subject: str, body: str, sender_name: str) -> MIMEMultipart:
    """
    Create an email message with the specified content.
    
    Args:
        sender_email: Sender's email address
        recipient_email: Recipient's email address
        subject: Email subject
        body: Email body text
        sender_name: Sender's display name
        
    Returns:
        MIMEMultipart email message
    """
    msg = MIMEMultipart()
    msg['From'] = f"{sender_name} <{sender_email}>" if sender_name else sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    # Format body with sender name
    formatted_body = body.format(sender_name=sender_name)
    msg.attach(MIMEText(formatted_body, 'plain'))
    
    return msg


def attach_file_to_email(msg: MIMEMultipart, file_path: str) -> bool:
    """
    Attach a file to the email message.
    
    Args:
        msg: Email message to attach file to
        file_path: Path to the file to attach
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            
        encoders.encode_base64(part)
        
        filename = os.path.basename(file_path)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}'
        )
        
        msg.attach(part)
        return True
        
    except Exception as e:
        logger.error(f"Error attaching file {file_path}: {e}")
        return False


def send_email(smtp_server: str, smtp_port: int, sender_email: str, 
               sender_password: str, msg: MIMEMultipart) -> bool:
    """
    Send the email message via SMTP.
    
    Args:
        smtp_server: SMTP server address
        smtp_port: SMTP server port
        sender_email: Sender's email address
        sender_password: Sender's email password/app password
        msg: Email message to send
        
    Returns:
        True if successful, False otherwise
    """
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        server.login(sender_email, sender_password)
        
        text = msg.as_string()
        server.sendmail(sender_email, msg['To'], text)
        server.quit()
        
        return True
        
    except Exception as e:
        logger.error(f"Error sending email to {msg['To']}: {e}")
        return False


def validate_config() -> bool:
    """
    Validate the email configuration.
    
    Returns:
        True if configuration is valid, False otherwise
    """
    required_fields = ['smtp_server', 'smtp_port', 'sender_email', 'sender_password']
    
    for field in required_fields:
        if not EMAIL_CONFIG.get(field):
            logger.error(f"Missing required configuration: {field}")
            return False
            
    if EMAIL_CONFIG['sender_email'] == 'your_email@gmail.com':
        logger.error("Please update sender_email in EMAIL_CONFIG")
        return False
        
    if EMAIL_CONFIG['sender_password'] == 'your_app_password':
        logger.error("Please update sender_password in EMAIL_CONFIG")
        return False
        
    return True


def main():
    """
    Main function to execute the email sending process.
    """
    logger.info("Starting email sender script")
    
    try:
        # Validate configuration
        if not validate_config():
            logger.error("Configuration validation failed")
            return False
            
        # Load recipients
        recipients = load_recipients(RECIPIENTS_FILE)
        
        # Get files to send
        files_to_send = get_files_to_send(FILES_FOLDER)
        
        if not files_to_send:
            logger.warning("No files to send. Exiting.")
            return False
            
        # Send emails to each recipient
        successful_sends = 0
        failed_sends = 0
        
        for recipient in recipients:
            logger.info(f"Preparing email for {recipient}")
            
            # Create email message
            msg = create_email_message(
                EMAIL_CONFIG['sender_email'],
                recipient,
                EMAIL_SUBJECT,
                EMAIL_BODY,
                EMAIL_CONFIG.get('sender_name', '')
            )
            
            # Attach all files
            attachment_success = True
            for file_path in files_to_send:
                if not attach_file_to_email(msg, file_path):
                    attachment_success = False
                    break
                    
            if not attachment_success:
                logger.error(f"Failed to attach files for {recipient}")
                failed_sends += 1
                continue
                
            # Send email
            if send_email(
                EMAIL_CONFIG['smtp_server'],
                EMAIL_CONFIG['smtp_port'],
                EMAIL_CONFIG['sender_email'],
                EMAIL_CONFIG['sender_password'],
                msg
            ):
                logger.info(f"Successfully sent email to {recipient}")
                successful_sends += 1
            else:
                logger.error(f"Failed to send email to {recipient}")
                failed_sends += 1
                
        # Summary
        logger.info(f"Email sending completed:")
        logger.info(f"  Successful: {successful_sends}")
        logger.info(f"  Failed: {failed_sends}")
        logger.info(f"  Total recipients: {len(recipients)}")
        
        return successful_sends > 0
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)