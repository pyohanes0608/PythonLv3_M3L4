# Project Portfolio Discord Bot

A lightweight Discord bot for organizing personal projects, tracking their status, and linking skills using a local SQLite database.

## ✨ Features

- Create projects with a name, link, and status.
- List projects saved by the Discord user.
- Update project details and status.
- Associate predefined skills with a project.
- Delete projects.
- Store project data locally in SQLite.

## 🧰 Tech Stack

- **Language:** Python
- **Bot framework:** `discord.py`
- **Database:** SQLite (`sqlite3`, included with Python)

## 📋 Prerequisites

- Python 3.10 or later (recommended).
- A Discord application and bot token.
- Permission to invite the bot to your Discord server. Enable the **Message Content Intent** for the bot in the Discord Developer Portal so it can receive prefix commands.

## 🚀 Installation & Setup

1. Clone the repository and enter its directory:

   ```bash
   git clone https://github.com/pyohanes0608/PythonLv3_M3L4.git
   cd PythonLv3_M3L4
   ```

2. (Optional but recommended) Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Activate it with `source .venv/bin/activate` on macOS/Linux, or `.venv\\Scripts\\activate` on Windows.

3. Install the bot dependency:

   ```bash
   python -m pip install discord.py
   ```

4. Open `config.py` and replace the placeholder `TOKEN` value with your bot token. The database path defaults to `portfolio.db`:

   ```python
   TOKEN = "YOUR_DISCORD_BOT_TOKEN"
   DATABASE = "portfolio.db"
   ```

   Keep your bot token private and do not commit a real token to the repository.

5. Create and seed the SQLite database:

   ```bash
   python logic.py
   ```

   This creates the tables and inserts the built-in skills and project statuses. Run this once before starting the bot.

## 💻 Usage

Start the bot from the repository directory:

```bash
python bot.py
```

In a server where the bot is present, use these commands:

| Command | Description |
| --- | --- |
| `!start` | Show the welcome message and command help. |
| `!info` | Show the available commands. |
| `!new_project` | Add a project by following the prompts for its name, link, and status. |
| `!projects` | List your saved projects. |
| `!update_projects` | Select a project and update one of its fields. |
| `!skills` | Link one of the predefined skills to a project. |
| `!delete` | Select and delete one of your projects. |

Project statuses and skills are currently predefined in `logic.py`. The bot uses the `!` command prefix.

## 📁 Project Structure

```text
.
├── bot.py       # Discord bot commands and startup
├── config.py    # Bot token and SQLite database path
└── logic.py     # SQLite database operations and initialization
```

## 🤝 Contributing

Contributions are welcome. Fork the repository, create a branch for your change, and open a pull request with a clear description. For larger changes, please open an issue first to discuss the proposal.

## 📄 License

MIT (assumed; no license file is currently included). Add a `LICENSE` file to formally apply this license.
