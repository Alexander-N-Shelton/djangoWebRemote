# webRemote

A web-based Smart TV remote control built with Django, designed to run locally on a Raspberry Pi or any Linux-based system with ADB installed. This project provides a touchscreen-friendly interface to control Smart TVs over your local network.

---

## 🔧 Features

- Local-only control — no cloud, no data tracking
- Works with any Smart TV that supports ADB (e.g., Google TV, Android TV)
- Customizable button layout and favorites
- Dual remote view: Navigation and Favorite controls
- Admin interface for managing users and settings
- Auto-starts with system via `systemd`
- Accessible from any device on your network

---

## 📦 Requirements

- Python 3.9+
- Django 5.1.3+
- ADB (`android-tools-adb`)

---

## 🚀 Setup (Debian-based systems like Raspberry Pi OS)

Download the _install.sh_ script.

Give the script the proper permissions to execute.

```Bash
chmod +x setup_web_remote.sh
```

After installation, open your browser and go to:

```http://<your-ip>:8000```

## 🛠 Admin Setup

A default superuser is created during setup. You can log in at:

```http://<your-ip>:8000/admin```

## Notes

This app is intended to run inside your local network

Each installation generates its own SECRET_KEY for session security

Admins can reset passwords through the admin panel
