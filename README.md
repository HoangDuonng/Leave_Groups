# Telegram Leave Groups

A Python script to view groups inside a Telegram folder and choose which groups to leave.

## 1. Requirements

- Install Python 3.
- Install Telethon:

```bash
pip install telethon
```

- Get your `api_id` and `api_hash` from: https://my.telegram.org/apps

## 2. Configure `leave_groups.py`

Open `leave_groups.py` and update the config lines near the top:

```python
api_id = YOUR_API_ID_HERE
api_hash = "YOUR_API_HASH_HERE"
FOLDER_NAME = "YOUR_TELEGRAM_FOLDER_NAME_HERE"
client = TelegramClient("YOUR_SESSION_NAME_HERE", api_id, api_hash)
```

Example:

```python
api_id = 123456
api_hash = "abcdef123456abcdef123456abcdef12"
FOLDER_NAME = "Work"
client = TelegramClient("my_telegram_session", api_id, api_hash)
```

Note: `api_id` is a number, so do not use quotes. The other values are text, so keep the quotes.

## 3. Run the script

```bash
python3 leave_groups.py
```

On the first run, Telegram will ask for your phone number, login code, and maybe your 2FA password.

The script will show the groups in the selected folder. Tick the groups you want to leave, then click **OUT SELECTED**. If your machine does not support the GUI, enter group numbers in the terminal, for example `1,3,5` or `2-4`.

## 4. Do not push session files to Git

After login, Telethon creates a `.session` file. This file contains login data, so keep it private.

Add this to `.gitignore`:

```gitignore
*.session
*.session-journal
__pycache__/
*.pyc
```
