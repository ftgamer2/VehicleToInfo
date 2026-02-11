#!/usr/bin/env python3
import requests
import json
import time
import sys
from bs4 import BeautifulSoup

# ========== COLOR CODES ==========
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
MAGENTA = "\033[1;95m"
WHITE = "\033[1;37m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ========== ANIMATIONS ==========
def animate_text(text, delay=0.03):
    """Typing animation for welcome message."""
    for char in text:
        print(f"{CYAN}{char}{RESET}", end='', flush=True)
        time.sleep(delay)
    print()

def loading_spinner(duration=1.5):
    """Simple spinner while fetching data."""
    spinner = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{YELLOW}⏳ Fetching vehicle info {spinner[i % 4]}{RESET}", end='', flush=True)
        i += 1
        time.sleep(0.1)
    print("\r" + " " * 40 + "\r", end='', flush=True)

# ========== BEAUTIFUL PRINTER ==========
def print_section(title, data_dict, indent=0):
    """Print a section with emojis and colors."""
    emojis = {
        "Owner Details": "👤",
        "Vehicle Details": "🏍️",
        "Registration Details": "📅",
        "Insurance Details": "🛡️",
        "Compliance Details": "✅",
        "Address Details": "📍",
        "Validity Details": "📆"
    }
    emoji = emojis.get(title, "📌")
    print(f"\n{BOLD}{BLUE}{emoji}  {title.upper()}{RESET}")
    print(f"{WHITE}{'─' * 40}{RESET}")
    for key, value in data_dict.items():
        if value is None or value == "NA":
            val = f"{RED}N/A{RESET}"
        else:
            val = f"{GREEN}{value}{RESET}"
        print(f"  {YELLOW}{key:<22}{RESET}: {val}")

# ========== VEHICLE DETAILS FETCHER ==========
def get_vehicle_details(rc_number):
    rc = rc_number.strip().upper()
    url = f"https://vahanx.in/rc-search/{rc}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        return {"error": f"❌ Network error: {e}"}
    except Exception as e:
        return {"error": f"❌ Unexpected error: {e}"}

    def get_value(label):
        """Extract value by label text."""
        try:
            span = soup.find("span", string=label)
            if not span:
                return None
            parent_div = span.find_parent("div")
            p_tag = parent_div.find("p") if parent_div else None
            return p_tag.get_text(strip=True) if p_tag else None
        except:
            return None

    data = {
        "Owner Details": {
            "Owner Name": get_value("Owner Name"),
            "Father's Name": get_value("Father's Name"),
            "Owner Serial": get_value("Owner Serial No"),
            "Financier": get_value("Financier Name"),
            "Phone": get_value("Phone") or "NA",
        },
        "Vehicle Details": {
            "Model": get_value("Model Name"),
            "Maker Model": get_value("Maker Model"),
            "Class": get_value("Vehicle Class"),
            "Fuel": get_value("Fuel Type"),
            "Fuel Norms": get_value("Fuel Norms"),
        },
        "Registration Details": {
            "RTO": get_value("Registered RTO"),
            "Reg Date": get_value("Registration Date"),
        },
        "Insurance Details": {
            "Company": get_value("Insurance Company"),
            "Valid Upto": get_value("Insurance Upto"),
            "Policy No": get_value("Insurance Number"),
        },
        "Compliance Details": {
            "Fitness Upto": get_value("Fitness Upto"),
            "Tax Upto": get_value("Tax Upto"),
            "PUC Upto": get_value("PUC Upto"),
        },
        "Address Details": {
            "Address": get_value("Address"),
            "City": get_value("City Name"),
        }
    }
    return data

# ========== MAIN ==========
def main():
    # Welcome animation (no credits)
    animate_text("🚀 VEHICLE INFO RETRIEVER", 0.04)
    time.sleep(0.3)

    # Input
    print(f"\n{CYAN}Enter Vehicle number{RESET}")
    rc = input(f"{RED}Vehicle-number:{GREEN}").strip().upper()
    print(f"{YELLOW}Vehicle info of: {WHITE}{rc}{RESET}")

    # Fetch with spinner
    loading_spinner()
    data = get_vehicle_details(rc)

    # Handle errors
    if "error" in data:
        print(f"\n{RED}{data['error']}{RESET}")
        return

    # Display beautiful output
    print(f"\n{BOLD}{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD}{WHITE}📋 RC NUMBER : {GREEN}{rc}{RESET}")
    print(f"{BOLD}{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

    for section, fields in data.items():
        if fields and any(v for v in fields.values()):  # skip empty sections
            print_section(section, fields)

    # ===== DEVELOPER CREDIT (only one) =====
    print(f"\n{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD}{WHITE}   🥷🏿  developer @ftgamer2{RESET}")
    print(f"{BOLD}{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")

if __name__ == "__main__":
    main()
