#Dev >> @SRS
#github.com/surjeetrajsinghgit

import os, sys, subprocess, urllib.parse, getpass

BASHRC     = os.path.expanduser("~/.bashrc")
APT_CONF   = "/etc/apt/apt.conf.d/95proxy"
PIP_CONF   = os.path.expanduser("~/.config/pip/pip.conf")
MARKER     = "# >>> proxy @SRS >>>"
MARKER_END = "# <<< proxy @SRS <<<"


def ask(prompt):
    try:
        return input(f"  {prompt}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print(); sys.exit(0)


def validate_url(url):
    try:
        p = urllib.parse.urlparse(url)
        if not p.scheme: return False, "Missing scheme"
        if not p.hostname: return False, "Missing host"
        if not p.port: return False, "Missing port"
        return True, ""
    except Exception as e:
        return False, str(e)


# ── bashrc ────────────────────────────────────────────────────────────────

def remove_bashrc_block():
    if not os.path.isfile(BASHRC): return
    with open(BASHRC) as f:
        lines = f.readlines()
    inside, new_lines = False, []
    for line in lines:
        if line.strip() == MARKER:   inside = True;  continue
        if line.strip() == MARKER_END: inside = False; continue
        if not inside: new_lines.append(line)
    with open(BASHRC, "w") as f:
        f.writelines(new_lines)

def write_bashrc(url):
    remove_bashrc_block()
    block = (
        f"\n{MARKER}\n"
        f"export http_proxy='{url}'\n"
        f"export https_proxy='{url}'\n"
        f"export HTTP_PROXY='{url}'\n"
        f"export HTTPS_PROXY='{url}'\n"
        f"export ftp_proxy='{url}'\n"
        f"export FTP_PROXY='{url}'\n"
        f"{MARKER_END}\n"
    )
    with open(BASHRC, "a") as f:
        f.write(block)
    print(f"  bashrc          → {BASHRC}")


# ── apt ───────────────────────────────────────────────────────────────────

def write_apt(url):
    content = f'Acquire::http::Proxy "{url}";\nAcquire::https::Proxy "{url}";\n'
    tmp = "/tmp/_proxy_apt_95proxy"
    with open(tmp, "w") as f: f.write(content)
    rc = subprocess.run(f"sudo mv {tmp} {APT_CONF} && sudo chmod 644 {APT_CONF}", shell=True, stderr=subprocess.DEVNULL).returncode
    if rc == 0: print(f"  apt config      → {APT_CONF}")
    else:       print(f"  apt config failed (sudo error)")

def remove_apt():
    if os.path.isfile(APT_CONF):
        rc = subprocess.run(f"sudo rm -f {APT_CONF}", shell=True, stderr=subprocess.DEVNULL).returncode
        if rc == 0: print(f"  apt config removed")
        else:       print(f"  Could not remove apt config (sudo error)")
    else:
        print(f"  (apt config not found — skipped)")


# ── pip ───────────────────────────────────────────────────────────────────

def write_pip(url):
    os.makedirs(os.path.dirname(PIP_CONF), exist_ok=True)
    content = f"[global]\nproxy = {url}\n"
    with open(PIP_CONF, "w") as f: f.write(content)
    print(f"  pip config      → {PIP_CONF}")

def remove_pip():
    if os.path.isfile(PIP_CONF):
        os.remove(PIP_CONF)
        print(f"  pip config removed")
    else:
        print(f"  (pip config not found — skipped)")


# ── git ───────────────────────────────────────────────────────────────────

def write_git(url):
    subprocess.run(f"git config --global http.proxy '{url}'", shell=True)
    subprocess.run(f"git config --global https.proxy '{url}'", shell=True)
    print(f"  git config      → ~/.gitconfig")

def remove_git():
    subprocess.run("git config --global --unset http.proxy", shell=True, stderr=subprocess.DEVNULL)
    subprocess.run("git config --global --unset https.proxy", shell=True, stderr=subprocess.DEVNULL)
    print(f"  git config removed")


# ── main actions ──────────────────────────────────────────────────────────

def proxy_on():
    proxy_terminal_text()
    
    host = ask("Proxy Host/IP (e.g. 192.168.1.1)")
    if not host:
        print("  Cancelled."); sys.exit(1)
    
    host = host.replace("http://", "").replace("https://", "")
        
    port = ask("Port (e.g. 8080)")
    if not port:
        print("  Cancelled."); sys.exit(1)
        
    print("\n  (Leave empty and press Enter if no authentication is required)")
    user = ask("Username")

    password = getpass.getpass("  Password: ")

    # Build the URL and automatically encode special characters in the credentials
    if user or password:
        enc_user = urllib.parse.quote(user, safe="")
        enc_pass = urllib.parse.quote(password, safe="")
        url = f"http://{enc_user}:{enc_pass}@{host}:{port}"
    else:
        url = f"http://{host}:{port}"

    ok, reason = validate_url(url)
    if not ok:
        print(f"\n  Final URL invalid: {reason}")
        print(f"    Generated: {url}\n")
        sys.exit(1)

    #print(f"\n  Generated URL: {url}\n  Writing configs…\n")
    print(f"\n  Proxy_Sucess")

    write_bashrc(url)
    write_apt(url)
    write_pip(url)
    write_git(url)

    print(f"\n  All done. To apply terminal proxy right now run:")
    print(f"    source ~/.bashrc\n")
    done_text("Proxy has been enabled and configured.")


def proxy_off():
    proxy_terminal_text()
    remove_bashrc_block()
    print(f"  bashrc block removed")
    remove_apt()
    remove_pip()
    remove_git()
    print(f"\n  All done. To clear terminal proxy right now run:")
    print(f"    source ~/.bashrc\n")
    done_text("Proxy has been removed successfully.")
# ----- Header ------------------------------------------------------------------
# ANSI Color & Style Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def proxy_terminal_text():
    print(
        f"""
{CYAN}{BOLD}╔════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║   ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗                                       ║
║   ██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝                                       ║
║   ██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝                                        ║
║   ██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝                                         ║
║   ██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║                                          ║
║   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝                                          ║
║                                                                                    ║
║   ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗███████╗██╗     The Ultimate    ║
║   ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔════╝██║     Proxy_Manager   ║
║      ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║█████╗  ██║                     ║
║      ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██║                     ║
║      ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║███████╗███████╗                ║
║      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝                ║
╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}
{RED}{BOLD}  DEV::@SRS {RESET}
        """)

def show_usage():
    print(f"""
{BOLD}  USAGE:{RESET}
    {GREEN}python3 proxy_set.py{RESET} {CYAN}[OPTION]{RESET}

{BOLD}  AVAILABLE OPTIONS:{RESET}
  ┌──────────┬─────────────────────────────────┬────────────────────────────┐
  │ {BOLD}Option{RESET}   │ {BOLD}Action{RESET}                          │ {BOLD}Command{RESET}                    │
  ├──────────┼─────────────────────────────────┼────────────────────────────┤
  │ {GREEN}{BOLD}--on{RESET}     │ Enable & configure proxy        │ {DIM}python3 proxy_set.py --on{RESET}  │
  │ {RED}{BOLD}--off{RESET}    │ Disable & remove proxy          │ {DIM}python3 proxy_set.py --off{RESET} │
  └──────────┴─────────────────────────────────┴────────────────────────────┘
"""
    )
   
def done_text(message):
    title = "        > > S U C C E S S < <"
    divider = "─" * 39
    print(f"""
{CYAN}╭───────────────────────────────────────────────╮
│                                               │
│    {GREEN}{BOLD}{title.ljust(39)}{RESET}{CYAN}    │
│    {DIM}{divider}{RESET}{CYAN}    │
│    {RESET}{message.ljust(39)}{CYAN}    │
│                                               │
╰───────────────────────────────────────────────╯{RESET}
""")

if __name__ == "__main__":
    if "--on"  in sys.argv: proxy_on()
    elif "--off" in sys.argv: proxy_off()
    else:
        proxy_terminal_text()
        show_usage()
