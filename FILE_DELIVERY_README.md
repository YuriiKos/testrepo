# File Delivery Script

A Python script that takes a file from a specified directory and sends it to multiple recipients via email using a delivery list.

## Features

- 📧 Send any file type via email
- 📋 Support for delivery lists (multiple recipients)
- ⚙️ Configurable SMTP settings
- 🔒 Secure credential handling
- 📝 Comprehensive logging
- 🛡️ Input validation and error handling
- 🔄 Retry mechanism for failed deliveries

## Requirements

- Python 3.6 or higher
- Email account with SMTP access
- For Gmail: App Password (recommended) or less secure app access

## Setup

1. **Configure Email Settings**: Edit `config.ini` with your email credentials:
   ```ini
   [email]
   smtp_server = smtp.gmail.com
   smtp_port = 587
   sender_email = your_email@gmail.com
   sender_password = your_app_password
   ```

2. **Create Delivery List**: Create a text file with email addresses (one per line):
   ```
   user1@example.com
   user2@example.com
   team@company.com
   ```

## Usage

### Basic Usage
```bash
python file_delivery_script.py --file document.pdf --delivery-list recipients.txt
```

### Advanced Usage
```bash
# With custom subject and body
python file_delivery_script.py \
    --file report.pdf \
    --delivery-list team.txt \
    --subject "Monthly Report - December 2024" \
    --body "Please find attached the monthly report."

# With custom config file
python file_delivery_script.py \
    --file data.csv \
    --delivery-list clients.txt \
    --config production_config.ini

# Override email credentials via command line
python file_delivery_script.py \
    --file presentation.pptx \
    --delivery-list attendees.txt \
    --sender-email myemail@company.com \
    --sender-password mypassword
```

### Command Line Options

| Option | Short | Required | Description |
|--------|--------|----------|-------------|
| `--file` | `-f` | Yes | Path to the file to send |
| `--delivery-list` | `-d` | Yes | Path to file with email addresses |
| `--subject` | `-s` | No | Custom email subject |
| `--body` | `-b` | No | Custom email body text |
| `--config` | `-c` | No | Path to config file (default: config.ini) |
| `--sender-email` | | No | Override sender email from config |
| `--sender-password` | | No | Override sender password from config |

## File Formats

### Delivery List Format
```
# Comments start with #
user1@example.com
user2@domain.com

# Empty lines are ignored
team@company.org
```

### Config File Format
```ini
[email]
smtp_server = smtp.gmail.com
smtp_port = 587
sender_email = your_email@gmail.com
sender_password = your_password
```

## Email Provider Settings

### Gmail
- SMTP Server: `smtp.gmail.com`
- Port: `587`
- Security: Use App Passwords for better security
- Setup: [Google App Passwords Guide](https://support.google.com/accounts/answer/185833)

### Outlook/Hotmail
- SMTP Server: `smtp-mail.outlook.com`
- Port: `587`
- Security: Use your regular password

### Yahoo Mail
- SMTP Server: `smtp.mail.yahoo.com`
- Port: `587` or `465`
- Security: Enable "Less secure app access"

## Logging

The script creates detailed logs in `file_delivery.log` with:
- Timestamp for each operation
- Success/failure status for each email
- Error details for troubleshooting
- Connection and authentication status

## Security Considerations

1. **App Passwords**: Use app-specific passwords instead of your main email password
2. **Config Files**: Don't commit config files with credentials to version control
3. **Environment Variables**: Consider using environment variables for sensitive data
4. **File Permissions**: Restrict access to config files containing credentials

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Check email and password
   - Enable "Less secure app access" or use App Password
   - Verify SMTP server and port settings

2. **File Not Found**
   - Check file path is correct
   - Ensure file permissions allow reading
   - Use absolute paths if relative paths don't work

3. **Invalid Email Addresses**
   - Check delivery list format
   - Ensure one email per line
   - Remove any extra spaces or characters

4. **SMTP Connection Failed**
   - Check internet connection
   - Verify SMTP server and port
   - Check firewall settings

### Debug Mode
Add verbose logging by modifying the logging level in the script:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Examples

### Example 1: Send a PDF Report
```bash
python file_delivery_script.py \
    --file monthly_report.pdf \
    --delivery-list management_team.txt \
    --subject "Monthly Sales Report - Q4 2024"
```

### Example 2: Send Data File to Analysts
```bash
python file_delivery_script.py \
    --file sales_data.csv \
    --delivery-list data_team.txt \
    --subject "Updated Sales Data" \
    --body "Please find the latest sales data for analysis."
```

### Example 3: Automated Daily Reports
```bash
#!/bin/bash
# daily_report.sh
DATE=$(date +%Y-%m-%d)
python file_delivery_script.py \
    --file "reports/daily_report_$DATE.pdf" \
    --delivery-list stakeholders.txt \
    --subject "Daily Report - $DATE"
```

## License

This script is provided as-is for educational and professional use. Modify as needed for your requirements.

## Support

For issues or questions:
1. Check the log file for detailed error messages
2. Verify all file paths and email addresses
3. Test with a single recipient first
4. Ensure email credentials are correct