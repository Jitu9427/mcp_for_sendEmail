# MCP Email Sender Server

This project implements a simple Model Context Protocol (MCP) server that can send emails.
It exposes a `send_email` tool that can be called by an LLM.

## Setup

1.  **Clone/Set up project:**
    ```bash
    # If cloned from git
    # git clone <repository_url>
    # cd mcp_email_server
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    # Install uv if you haven't: pip install uv
    uv init
    uv add "mcp[cli]" python-dotenv
    ```

3.  **Configure Email Credentials:**
    Create a `.env` file in the root of the project and add your email credentials:
    ```env
    SENDER_EMAIL="your_email@example.com"
    SENDER_APP_PASSWORD="your_app_password" # Use an App Password
    SMTP_SERVER="smtp.example.com"
    SMTP_PORT="587" # Or 465, etc.
    ```
    **Important:** Ensure `.env` is listed in your `.gitignore` file.

## Running the Server

To run the server in development mode (which opens the MCP Inspector):
```bash
uv run mcp dev server.py
