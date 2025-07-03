# Telegram AI Assistant Bot

This project is a personal Telegram chatbot AI assistant powered by LLMs. It helps automate daily operations such as reminders, document summarization, daily logs, weekly progress summaries, and integrates with the Canvas API for academic tracking. The project is managed with Taskmaster-AI for structured task management and planning.

## Features
- Set reminders via chat
- Summarize documents
- Log daily activities and generate weekly summaries
- Integrate with Canvas LMS for course and assignment tracking
- Deployable to Cloudflare Workers

## Project Structure
```
/your-project-root
  /src                # Source code
  .env                # Environment variables (not committed)
  requirements.txt    # Python dependencies
  README.md           # Project documentation
  .taskmaster/        # Taskmaster-AI files (auto-managed)
  ...
```

## Setup

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up your environment variables:**
   - Create a `.env` file in the project root:
     ```
     TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
     OPENAI_API_KEY=your-openai-key-here
     ```

5. **Run the bot:**
   ```sh
   python src/main.py
   ```

## Task Management
- Tasks and planning are managed with Taskmaster-AI.
- See `.taskmaster/` for PRD, tasks, and documentation.

## Deployment
- See Taskmaster-AI tasks and documentation for Cloudflare deployment steps.

## Security
- **Never commit your `.env` file or any secrets to version control.**
- The `.gitignore` is set up to exclude sensitive and unnecessary files.

## License
MIT 