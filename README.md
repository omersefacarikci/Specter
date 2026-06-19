# Specter

**Ghost follower hunter — GitHub Bot Cleaner**

Specter is a powerful command-line interface (CLI) tool designed to help you keep your GitHub profile clean.  
It detects spam/bot accounts, identifies users who don't follow you back, and allows you to bulk-star your own repositories.

---

```
 ███████╗██████╗ ███████╗ ██████╗████████╗███████╗██████╗ 
 ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗
 ███████╗██████╔╝█████╗  ██║        ██║   █████╗  ██████╔╝
 ╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██╔══╝  ██╔══██╗
 ███████║██║     ███████╗╚██████╗   ██║   ███████╗██║  ██║
 ╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
```

---

## Features

- 🔎 **Bot Detection**  
  Identifies accounts with spam patterns (e.g., "star for star", "follow for follow") or suspicious follower/following ratios.

- 🚫 **Auto-Block**  
  Blocks detected bot accounts upon your confirmation.

- 🔕 **Follower Management**  
  Identifies users who don't follow you back and allows you to unfollow them.

- ⭐ **Bulk Starring**  
  Quickly star all your own repositories.

- 📋 **Secure Report Mode**  
  Analyzes your account and generates a report without making any changes.

- 🧪 **Dry-Run Support**  
  Preview actions before executing them to ensure accuracy.

---

### Requirements

* **Python 3.10+**
* **GitHub Personal Access Token (Classic):**
  1. Go to your GitHub **Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)**.
  2. Click **Generate new token (classic)**.
  3. Give it a name (e.g., "Specter").
  4. Under **Select scopes**, check the entire **`user`** category (this automatically selects `read:user`, `user:email`, `user:follow`) and the **`repo`** category.
  5. Click **Generate token** and copy the code immediately (you won't be able to see it again!).
---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/omersefacarikci/Specter.git
cd Specter
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit the `.env` file:

```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_USERNAME=your_username
```

⚠️ **IMPORTANT:** Never commit your `.env` file to version control!

---

## Usage

Run the tool:

```bash
python main.py
```

### Menu Options

```
[1] Detect and block bot followers
[2] Unfollow users who don't follow back
[3] Star my own repositories
[4] Generate a report (Safe Mode)
[5] Exit
```

All actions require your confirmation before execution.

---

## License

This project is licensed under the MIT License.  
See the `LICENSE` file for more details.
