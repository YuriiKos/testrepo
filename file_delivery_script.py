#!/usr/bin/env python3
"""
File Delivery Script
===================

This script takes a file from a specified directory and sends it to 
email addresses listed in a delivery list file.

Usage:
    python file_delivery_script.py --file <file_path> --delivery-list <delivery_list_path>

Requirements:
    - A file to send
    - A delivery list file with email addresses (one per line)
    - Email configuration (SMTP settings)
"""

import os
import sys
import argparse
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path
from typing import List, Optional
import configparser


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('file_delivery.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class FileDeliveryService:
    """Service class for handling file delivery via email."""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        """
        Initialize the delivery service.
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP server port
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = None
        self.sender_password = None
        
    def configure_email(self, sender_email: str, sender_password: str):
        """Configure email credentials."""
        self.sender_email = sender_email
        self.sender_password = sender_password
        
    def load_delivery_list(self, delivery_list_path: str) -> List[str]:
        """
        Load email addresses from delivery list file.
        
        Args:
            delivery_list_path: Path to file containing email addresses
            
        Returns:
            List of email addresses
        """
        try:
            with open(delivery_list_path, 'r', encoding='utf-8') as file:
                emails = []
                for line_num, line in enumerate(file, 1):
                    email = line.strip()
                    if email and not email.startswith('#'):  # Skip empty lines and comments
                        if '@' in email:  # Basic email validation
                            emails.append(email)
                        else:
                            logger.warning(f"Invalid email format on line {line_num}: {email}")
                
                logger.info(f"Loaded {len(emails)} email addresses from {delivery_list_path}")
                return emails
                
        except FileNotFoundError:
            logger.error(f"Delivery list file not found: {delivery_list_path}")
            raise
        except Exception as e:
            logger.error(f"Error reading delivery list: {e}")
            raise
    
    def validate_file(self, file_path: str) -> bool:
        """
        Validate that the file exists and can be read.
        
        Args:
            file_path: Path to the file to send
            
        Returns:
            True if file is valid, False otherwise
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
            
        if not os.path.isfile(file_path):
            logger.error(f"Path is not a file: {file_path}")
            return False
            
        try:
            with open(file_path, 'rb'):
                pass
        except PermissionError:
            logger.error(f"Permission denied reading file: {file_path}")
            return False
        except Exception as e:
            logger.error(f"Error accessing file {file_path}: {e}")
            return False
            
        return True
    
    def create_email_message(self, recipient: str, file_path: str, subject: str = None, body: str = None) -> MIMEMultipart:
        """
        Create email message with file attachment.
        
        Args:
            recipient: Recipient email address
            file_path: Path to file to attach
            subject: Email subject (optional)
            body: Email body text (optional)
            
        Returns:
            Email message object
        """
        filename = os.path.basename(file_path)
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient
        msg['Subject'] = subject or f"File Delivery: {filename}"
        
        # Add body
        default_body = f"""
Hello,

Please find the attached file: {filename}

This file was sent automatically by the File Delivery Service.

Best regards,
File Delivery System
        """
        
        msg.attach(MIMEText(body or default_body, 'plain'))
        
        # Add attachment
        try:
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}'
                )
                msg.attach(part)
        except Exception as e:
            logger.error(f"Error creating attachment for {file_path}: {e}")
            raise
            
        return msg
    
    def send_file(self, file_path: str, delivery_list: List[str], subject: str = None, body: str = None) -> dict:
        """
        Send file to all recipients in delivery list.
        
        Args:
            file_path: Path to file to send
            delivery_list: List of recipient email addresses
            subject: Email subject (optional)
            body: Email body text (optional)
            
        Returns:
            Dictionary with delivery results
        """
        results = {
            'successful': [],
            'failed': [],
            'total': len(delivery_list)
        }
        
        if not self.sender_email or not self.sender_password:
            raise ValueError("Email credentials not configured. Use configure_email() method.")
        
        try:
            # Connect to SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            
            logger.info(f"Connected to SMTP server: {self.smtp_server}:{self.smtp_port}")
            
            for recipient in delivery_list:
                try:
                    # Create and send email
                    msg = self.create_email_message(recipient, file_path, subject, body)
                    text = msg.as_string()
                    server.sendmail(self.sender_email, recipient, text)
                    
                    results['successful'].append(recipient)
                    logger.info(f"File sent successfully to: {recipient}")
                    
                except Exception as e:
                    results['failed'].append({'email': recipient, 'error': str(e)})
                    logger.error(f"Failed to send to {recipient}: {e}")
            
            server.quit()
            
        except Exception as e:
            logger.error(f"SMTP connection error: {e}")
            raise
        
        return results


def load_config(config_path: str = "config.ini") -> dict:
    """Load configuration from file."""
    config = configparser.ConfigParser()
    
    if os.path.exists(config_path):
        config.read(config_path)
        return {
            'smtp_server': config.get('email', 'smtp_server', fallback='smtp.gmail.com'),
            'smtp_port': config.getint('email', 'smtp_port', fallback=587),
            'sender_email': config.get('email', 'sender_email', fallback=''),
            'sender_password': config.get('email', 'sender_password', fallback='')
        }
    else:
        logger.warning(f"Config file {config_path} not found. Using defaults.")
        return {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': '',
            'sender_password': ''
        }


def main():
    """Main function to handle command line arguments and execute file delivery."""
    parser = argparse.ArgumentParser(
        description="Send a file to multiple recipients via email",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python file_delivery_script.py --file report.pdf --delivery-list emails.txt
    python file_delivery_script.py --file data.csv --delivery-list recipients.txt --subject "Monthly Report"
    python file_delivery_script.py --file document.docx --delivery-list team.txt --config custom_config.ini
        """
    )
    
    parser.add_argument(
        '--file', '-f',
        required=True,
        help='Path to the file to send'
    )
    
    parser.add_argument(
        '--delivery-list', '-d',
        required=True,
        help='Path to file containing delivery email addresses (one per line)'
    )
    
    parser.add_argument(
        '--subject', '-s',
        help='Email subject line'
    )
    
    parser.add_argument(
        '--body', '-b',
        help='Email body text'
    )
    
    parser.add_argument(
        '--config', '-c',
        default='config.ini',
        help='Path to configuration file (default: config.ini)'
    )
    
    parser.add_argument(
        '--sender-email',
        help='Sender email address (overrides config file)'
    )
    
    parser.add_argument(
        '--sender-password',
        help='Sender email password (overrides config file)'
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = load_config(args.config)
        
        # Override with command line arguments if provided
        sender_email = args.sender_email or config['sender_email']
        sender_password = args.sender_password or config['sender_password']
        
        if not sender_email:
            sender_email = input("Enter sender email address: ")
        if not sender_password:
            import getpass
            sender_password = getpass.getpass("Enter sender email password: ")
        
        # Initialize delivery service
        delivery_service = FileDeliveryService(
            smtp_server=config['smtp_server'],
            smtp_port=config['smtp_port']
        )
        delivery_service.configure_email(sender_email, sender_password)
        
        # Validate file
        if not delivery_service.validate_file(args.file):
            sys.exit(1)
        
        # Load delivery list
        delivery_list = delivery_service.load_delivery_list(args.delivery_list)
        
        if not delivery_list:
            logger.error("No valid email addresses found in delivery list")
            sys.exit(1)
        
        # Send file
        logger.info(f"Starting delivery of {args.file} to {len(delivery_list)} recipients")
        results = delivery_service.send_file(
            args.file,
            delivery_list,
            args.subject,
            args.body
        )
        
        # Report results
        logger.info(f"Delivery completed: {len(results['successful'])}/{results['total']} successful")
        
        if results['failed']:
            logger.error("Failed deliveries:")
            for failure in results['failed']:
                logger.error(f"  {failure['email']}: {failure['error']}")
        
        # Exit with appropriate code
        sys.exit(0 if len(results['failed']) == 0 else 1)
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()