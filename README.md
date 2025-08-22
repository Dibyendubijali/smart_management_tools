# 🛠️ Smart Management Tools

A beginner-friendly **desktop application** to manage, monitor, and access multiple Linux servers from a single interface.

---

## 📌 Features
- Register Linux servers (IP, Port, Username, Password/SSH key)
- SSH access with terminal
- Real-time server monitoring (CPU, Memory, Disk)
- View running processes & server logs
- Execute remote shell commands securely
- Modular codebase (each feature in its own folder)

---

## 📂 Project Structure
smart_management_tools/
│
├── main.py # Entry point
├── requirements.txt # Dependencies
├── README.md # Documentation
│
├── assets/ # Icons, images
│ └── logo.png
│
├── ui/ # UI files (PyQt5/Tkinter)
│ ├── main_window.py
│ ├── server_list_ui.py
│ └── terminal_ui.py
│
├── features/ # Core features
│ ├── server_registration/
│ ├── ssh_access/
│ ├── server_monitoring/
│ ├── process_logs/
│ └── remote_shell/
│
├── utils/ # Helpers
│ ├── config_loader.py
│ └── ssh_helper.py
│
└── logs/
└── app.log


---

## ⚙️ Setup Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt
