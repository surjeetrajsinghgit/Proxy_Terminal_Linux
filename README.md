# 🌐 The Ultimate Proxy Manager

<div align="center">
  <p><strong>A beautiful, zero-dependency CLI tool to instantly configure or remove system-wide proxy settings on Linux.</strong></p>
</div>

## 🚀 Overview

Configuring a proxy on a fresh Linux installation usually means digging through hidden files and manually setting up `bash`, `apt`, `pip`, and `git` one by one. 

**The Ultimate Proxy Manager** automates this entirely. With a single command, you can route your entire system through a proxy, and with another, completely remove it. 

### ✨ Why this tool?
*   **100% Offline Compatible:** Built entirely using Python's Standard Library. You don't need the internet or `pip install` to set this up—perfect for air-gapped machines that need proxy configuration *before* they can access the web.
*   **All-in-One Configuration:** Automatically configures environment variables, package managers, and version control simultaneously.

---

## ⚙️ What It Does (Under the Hood)

When enabled, the script safely injects your proxy URL into the following locations. When disabled, it cleans up after itself without touching your other configurations.

| Target | File Modified | Purpose |
| :--- | :--- | :--- |
| **System/Bash** | `~/.bashrc` | Sets `http_proxy`, `https_proxy`, `ftp_proxy` for terminal sessions. |
| **APT Packages** | `/etc/apt/apt.conf.d/95proxy` | Allows `sudo apt update` / `install` to work through the proxy. |
| **PIP (Python)** | `~/.config/pip/pip.conf` | Allows Python package installations to route correctly. |
| **Git** | `~/.gitconfig` | Configures `http.proxy` and `https.proxy` globally. |

> **Security Note:** If your proxy requires a username and password, this tool will safely URL-encode special characters. However, be aware that Linux proxy configurations store credentials in plain text within these configuration files.

---

## 🛠️ Installation

Because this tool has **zero external dependencies**, installation is just downloading a single file.

**For Offline Machines:**
1. Download `proxy_set.py` onto a USB drive from an internet-connected computer.
2. Plug the USB into your offline Linux (Debian/Ubuntu) machine.
3. Copy the script to your home directory or run it directly from the drive.

**For Online Machines:**
```bash
git clone [https://github.com/surjeetrajsinghgit/proxy_Terminal_Linux.git](https://github.com/surjeetrajsinghgit/roxy_Terminal_Linux.git)
cd proxy-manager
