# Email File Sender Script

A Python script to automatically send files from a specified folder to a list of recipients with a customizable email message.

## Features

- ✅ Send files from a defined folder to multiple recipients
- ✅ Recipients list managed in a separate text file
- ✅ Customizable email subject and body text
- ✅ Support for multiple file types and attachments
- ✅ Comprehensive logging and error handling
- ✅ Configuration helper for easy setup
- ✅ Support for Gmail, Outlook, Yahoo, and custom SMTP servers

## Quick Start

### 1. Setup Configuration

Run the configuration helper to set up your email credentials:

```bash
python config_setup.py
```

This will guide you through:
- Selecting your email provider
- Setting up app passwords (for security)
- Configuring SMTP settings
- Updating the main script with your credentials

### 2. Add Recipients

Edit `recipients.txt` and add email addresses (one per line):

```
john.doe@example.com
jane.smith@company.org
team@organization.net
```

### 3. Add Files to Send

Place the files you want to send in the `files_to_send/` folder:

```bash
cp your_document.pdf files_to_send/
cp your_image.jpg files_to_send/
cp your_spreadsheet.xlsx files_to_send/
```

### 4. Run the Script

```bash
python email_sender.py
```

## File Structure

```
.
├── email_sender.py          # Main script
├── config_setup.py          # Configuration helper
├── recipients.txt           # List of email recipients
├── files_to_send/          # Folder containing files to attach
│   └── sample_document.txt  # Example file
└── EMAIL_SENDER_README.md   # This documentation
```

## Configuration

### Email Providers Setup

#### Gmail
1. Enable 2-Factor Authentication
2. Go to Google Account → Security → App passwords
3. Generate an app password for 'Mail'
4. Use the app password (not your regular password)

#### Outlook/Hotmail
1. Enable 2-Factor Authentication
2. Go to Security dashboard → App passwords
3. Generate an app password for 'Email'

#### Yahoo Mail
1. Go to Account security
2. Turn on 2-step verification
3. Generate an app password for 'Mail'

### Manual Configuration

If you prefer to configure manually, edit the `EMAIL_CONFIG` section in `email_sender.py`:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',      # Your SMTP server
    'smtp_port': 587,                     # SMTP port (usually 587 or 465)
    'sender_email': 'your_email@gmail.com',  # Your email address
    'sender_password': 'your_app_password',  # Your app password
    'sender_name': 'Your Name'               # Display name (optional)
}
```

### Customizing Email Content

Edit the email subject and body in `email_sender.py`:

```python
EMAIL_SUBJECT = 'Your Custom Subject'
EMAIL_BODY = """
Your custom email message here.

You can use {sender_name} to include the sender's name.

Best regards,
{sender_name}
"""
```

## Supported File Types

The script can send any file type as an attachment:
- Documents: `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.txt`
- Images: `.jpg`, `.png`, `.gif`, `.bmp`
- Archives: `.zip`, `.rar`, `.tar.gz`
- Any other file type

**Note:** Most email providers have attachment size limits (typically 25MB total per email).

## Command Line Options

### Basic Usage
```bash
python email_sender.py
```

### Check Configuration
The script will validate your configuration before sending emails and provide helpful error messages if something is missing.

## Logging

The script creates detailed logs in `email_sender.log` including:
- Email sending attempts and results
- File attachment status
- Error messages and debugging information
- Summary statistics

## Troubleshooting

### Common Issues

1. **Authentication Error**
   - Make sure you're using an app password, not your regular password
   - Verify 2-Factor Authentication is enabled
   - Check that your email and password are correct

2. **SMTP Connection Error**
   - Verify SMTP server and port settings
   - Check your internet connection
   - Some networks may block SMTP ports

3. **File Not Found Error**
   - Ensure `recipients.txt` exists and contains valid email addresses
   - Check that `files_to_send/` folder exists and contains files
   - Verify file permissions

4. **Large Attachment Error**
   - Check file sizes (most providers limit to 25MB total)
   - Consider using cloud storage links for large files

### Getting Help

Check the log file (`email_sender.log`) for detailed error messages. The script provides informative error messages to help diagnose issues.

## Security Considerations

- ✅ Uses app passwords instead of regular passwords
- ✅ Supports TLS/SSL encryption
- ✅ Passwords are not displayed in terminal output
- ✅ Sensitive information is not logged
- ⚠️ Keep your app password secure and don't share it
- ⚠️ Be cautious when sending sensitive files

## Requirements

- Python 3.6 or higher
- Standard library modules (no additional packages required):
  - `smtplib`
  - `email`
  - `pathlib`
  - `logging`

## License

This script is provided as-is for educational and personal use. Feel free to modify and adapt it to your needs.

## Examples

### Example recipients.txt
```
# Development Team
dev1@company.com
dev2@company.com

# Management
manager@company.com

# External Partners
partner@external.org
```

### Example Usage Scenarios

1. **Weekly Reports**: Send weekly reports to stakeholders
2. **Document Distribution**: Share documents with team members
3. **Backup Delivery**: Send backup files to multiple locations
4. **Newsletter Distribution**: Send newsletters with attachments

---

**Happy emailing! 📧**