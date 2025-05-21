import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP #

# Load environment variables from .env file
load_dotenv()

# Get email configuration from environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_APP_PASSWORD = os.getenv("SENDER_APP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT_STR = os.getenv("SMTP_PORT")

# Validate that SMTP_PORT can be converted to an integer
SMTP_PORT = None
if SMTP_PORT_STR:
    try:
        SMTP_PORT = int(SMTP_PORT_STR)
    except ValueError:
        print(f"Error: SMTP_PORT '{SMTP_PORT_STR}' is not a valid integer. Please check your .env file.")
        exit(1) # Exit if the port is invalid, as the server can't function

# Create an MCP server instance
mcp = FastMCP("EmailSenderServer")

@mcp.tool() #
def send_email(recipient_email: str, subject: str, body: str) -> str:
    """
    Sends an email from the configured sender to the specified recipient.
    This tool can be called by an LLM to send emails.

    Args:
        recipient_email: The email address of the recipient.
        subject: The subject of the email.
        body: The content/body of the email.

    Returns:
        A string indicating the status of the email sending operation.
    """
    if not SENDER_EMAIL or not SENDER_APP_PASSWORD or not SMTP_SERVER or SMTP_PORT is None:
        missing_configs = []
        if not SENDER_EMAIL: missing_configs.append("SENDER_EMAIL")
        if not SENDER_APP_PASSWORD: missing_configs.append("SENDER_APP_PASSWORD")
        if not SMTP_SERVER: missing_configs.append("SMTP_SERVER")
        if SMTP_PORT is None: missing_configs.append("SMTP_PORT")
        return f"Error: Email server not fully configured. Missing: {', '.join(missing_configs)}. Please check your .env file."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()  # Extended Hello
            server.starttls()  # Secure the connection using TLS
            server.ehlo()  # Re-send ehlo after starttls
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        return f"Email successfully sent to {recipient_email} with subject '{subject}'."
    except smtplib.SMTPAuthenticationError:
        return "Error: SMTP Authentication Failed. Check your SENDER_EMAIL or SENDER_APP_PASSWORD in the .env file."
    except smtplib.SMTPConnectError:
        return f"Error: Failed to connect to SMTP server {SMTP_SERVER} on port {SMTP_PORT}."
    except smtplib.SMTPServerDisconnected:
        return "Error: SMTP server disconnected unexpectedly. Please try again."
    except smtplib.SMTPException as e:
        return f"An SMTP error occurred: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# This part allows you to run the server directly using "python server.py"
# or "mcp run server.py" as per the documentation
if __name__ == "__main__":
    if not SENDER_EMAIL or not SENDER_APP_PASSWORD or not SMTP_SERVER or SMTP_PORT is None:
        print("Error: Email server environment variables (SENDER_EMAIL, SENDER_APP_PASSWORD, SMTP_SERVER, SMTP_PORT) are not fully set.")
        print("Please create and configure a .env file with these details.")
    else:
        print("MCP Email Sender Server is starting...")
        print(f"Sender Email: {SENDER_EMAIL}")
        print(f"SMTP Server: {SMTP_SERVER}:{SMTP_PORT}")
        print("To test, you can use 'uv run mcp dev server.py'")
        mcp.run() #