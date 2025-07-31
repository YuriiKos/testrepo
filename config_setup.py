#!/usr/bin/env python3
"""
Configuration Setup Helper

This script helps you configure the email sender with your email credentials.
It provides guidance on setting up app passwords and SMTP settings for different email providers.
"""

import getpass
import os
import sys
from pathlib import Path

def get_smtp_settings():
    """Get SMTP settings for common email providers"""
    providers = {
        '1': {
            'name': 'Gmail',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'instructions': """
Gmail Setup Instructions:
1. Enable 2-Factor Authentication on your Google account
2. Go to Google Account settings > Security > App passwords
3. Generate an app password for 'Mail'
4. Use this app password (not your regular password) in the script
            """
        },
        '2': {
            'name': 'Outlook/Hotmail',
            'smtp_server': 'smtp-mail.outlook.com',
            'smtp_port': 587,
            'instructions': """
Outlook Setup Instructions:
1. Enable 2-Factor Authentication on your Microsoft account
2. Go to Security dashboard > Advanced security options > App passwords
3. Generate an app password for 'Email'
4. Use this app password in the script
            """
        },
        '3': {
            'name': 'Yahoo Mail',
            'smtp_server': 'smtp.mail.yahoo.com',
            'smtp_port': 587,
            'instructions': """
Yahoo Mail Setup Instructions:
1. Go to Account security in your Yahoo account
2. Turn on 2-step verification
3. Generate an app password for 'Mail'
4. Use this app password in the script
            """
        },
        '4': {
            'name': 'Custom SMTP',
            'smtp_server': '',
            'smtp_port': 587,
            'instructions': """
Custom SMTP Setup:
You'll need to provide your own SMTP server details.
Contact your email provider for SMTP configuration.
            """
        }
    }
    
    print("Select your email provider:")
    for key, provider in providers.items():
        print(f"{key}. {provider['name']}")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        if choice in providers:
            return providers[choice]
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

def update_email_script(smtp_server, smtp_port, sender_email, sender_password, sender_name):
    """Update the email_sender.py script with user configuration"""
    script_path = 'email_sender.py'
    
    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found!")
        return False
    
    try:
        with open(script_path, 'r') as f:
            content = f.read()
        
        # Replace configuration values
        content = content.replace("'smtp_server': 'smtp.gmail.com'", f"'smtp_server': '{smtp_server}'")
        content = content.replace("'smtp_port': 587", f"'smtp_port': {smtp_port}")
        content = content.replace("'sender_email': 'your_email@gmail.com'", f"'sender_email': '{sender_email}'")
        content = content.replace("'sender_password': 'your_app_password'", f"'sender_password': '{sender_password}'")
        content = content.replace("'sender_name': 'Your Name'", f"'sender_name': '{sender_name}'")
        
        with open(script_path, 'w') as f:
            f.write(content)
        
        print(f"\n✅ Configuration updated successfully in {script_path}")
        return True
        
    except Exception as e:
        print(f"Error updating configuration: {e}")
        return False

def main():
    """Main configuration setup function"""
    print("=" * 60)
    print("Email Sender Configuration Setup")
    print("=" * 60)
    
    # Get SMTP provider settings
    provider = get_smtp_settings()
    print(f"\nSelected: {provider['name']}")
    print(provider['instructions'])
    
    smtp_server = provider['smtp_server']
    smtp_port = provider['smtp_port']
    
    if provider['name'] == 'Custom SMTP':
        smtp_server = input("Enter SMTP server address: ").strip()
        try:
            smtp_port = int(input("Enter SMTP port (default 587): ").strip() or "587")
        except ValueError:
            smtp_port = 587
    
    print("\n" + "-" * 40)
    
    # Get user credentials
    sender_email = input("Enter your email address: ").strip()
    sender_name = input("Enter your name (optional): ").strip() or "Email Sender"
    
    print("\nEnter your app password (characters won't be displayed for security):")
    sender_password = getpass.getpass("App Password: ")
    
    if not all([smtp_server, sender_email, sender_password]):
        print("Error: Missing required information!")
        return False
    
    # Confirm settings
    print("\n" + "=" * 40)
    print("Configuration Summary:")
    print("=" * 40)
    print(f"SMTP Server: {smtp_server}")
    print(f"SMTP Port: {smtp_port}")
    print(f"Email: {sender_email}")
    print(f"Name: {sender_name}")
    print(f"Password: {'*' * len(sender_password)}")
    
    confirm = input("\nUpdate email_sender.py with these settings? (y/N): ").strip().lower()
    
    if confirm == 'y':
        if update_email_script(smtp_server, smtp_port, sender_email, sender_password, sender_name):
            print("\n🎉 Setup complete!")
            print("\nNext steps:")
            print("1. Add recipient email addresses to 'recipients.txt'")
            print("2. Add files to send in the 'files_to_send' folder")
            print("3. Run: python email_sender.py")
            return True
        else:
            print("\n❌ Setup failed!")
            return False
    else:
        print("\nSetup cancelled.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)